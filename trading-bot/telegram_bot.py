#!/usr/bin/env python3
"""MarketFlow Telegram bot — zero dependencies (Python stdlib only).

Setup:
  1. Talk to @BotFather on Telegram, /newbot, copy the token.
  2. export TELEGRAM_BOT_TOKEN="123456:ABC-your-token"
  3. python3 telegram_bot.py
  4. Open your bot in Telegram and send /start.

Optional:
  export TELEGRAM_ALLOWED_CHATS="12345,67890"   # restrict who can use it
  python3 telegram_bot.py --token <token>        # token via flag instead

Commands:
  /predict [symbol] [interval]          current market-flow reading
  /backtest [symbol] [interval]         walk-forward backtest
  /watch [symbol] [interval] [minutes]  alert me when the flow direction flips
  /unwatch                              stop alerts
  /status                               show my subscription
  /help                                 usage
"""

from __future__ import annotations

import argparse
import html
import json
import os
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from marketflow.data import (DEFAULT_SYMBOL, GOLD_SYMBOLS, INTERVAL_SECONDS,
                             SYMBOL_ALIASES, fetch_klines,
                             fetch_tradingview_quote)
from marketflow.engine import Engine, Prediction
from marketflow.backtest import run_backtest
from marketflow import news as news_mod
from marketflow import i18n
from marketflow.i18n import t

_HERE = os.path.dirname(os.path.abspath(__file__))
SUBS_FILE = os.path.join(_HERE, "subscriptions.json")
LANGS_FILE = os.path.join(_HERE, "user_langs.json")


class TelegramAPI:
    def __init__(self, token: str):
        self.base = f"https://api.telegram.org/bot{token}"

    def call(self, method: str, *, http_timeout: int = 30, **params):
        data = urllib.parse.urlencode(
            {k: v for k, v in params.items() if v is not None}).encode()
        req = urllib.request.Request(f"{self.base}/{method}", data=data)
        with urllib.request.urlopen(req, timeout=http_timeout) as resp:
            payload = json.loads(resp.read().decode())
        if not payload.get("ok"):
            raise RuntimeError(f"telegram {method} failed: {payload}")
        return payload["result"]

    def get_updates(self, offset: int | None):
        # long poll: telegram holds the request up to 50s, so allow 60s http
        return self.call("getUpdates", offset=offset, timeout=50,
                         allowed_updates='["message"]', http_timeout=60)

    def send(self, chat_id: int, text: str):
        # Telegram hard limit is 4096 chars per message
        for chunk_start in range(0, len(text), 4000):
            self.call("sendMessage", chat_id=chat_id,
                      text=text[chunk_start:chunk_start + 4000],
                      parse_mode="HTML", disable_web_page_preview=True)


def spot_quote_line(symbol: str, lang: str = "en") -> str:
    """Live spot XAU/USD from TradingView (OANDA feed) for gold symbols."""
    resolved = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
    if resolved not in GOLD_SYMBOLS:
        return ""
    q = fetch_tradingview_quote("OANDA:XAUUSD")
    if not q:
        return ""
    return t(lang, "spot_line", price=f"{q['close']:.2f}",
             chg=f"{q.get('change', 0):+.2f}", high=f"{q.get('high', 0):.2f}",
             low=f"{q.get('low', 0):.2f}")


def event_risk_line(lang: str = "en") -> str:
    """Warning when a high-impact USD event is inside the danger window."""
    e = news_mod.event_risk(window_hours=8.0)
    if not e:
        return ""
    hrs = e.hours_from_now()
    when = (t(lang, "risk_now") if hrs < 0.5
            else t(lang, "risk_in", h=f"{hrs:.1f}"))
    return t(lang, "risk_line", when=when, title=html.escape(e.title))


def format_news(lang: str = "en") -> str:
    lines = [t(lang, "news_title"), ""]
    try:
        events = news_mod.upcoming_events(hours_ahead=36)
        if events:
            lines.append(t(lang, "news_cal_header"))
            for e in events[:8]:
                hrs = e.hours_from_now()
                when = f"{hrs:+.1f}h" if abs(hrs) < 24 else f"{hrs / 24:+.1f}d"
                badge = "🔴" if e.impact == "High" else "🟠"
                extra = (t(lang, "forecast_prev", f=e.forecast, p=e.previous)
                         if e.forecast else "")
                lines.append(f"{badge} {when}  {html.escape(e.title)}"
                             f"{html.escape(extra)}")
        else:
            lines.append(t(lang, "news_none"))
    except Exception as ex:
        lines.append(t(lang, "news_cal_unavail", error=ex))
    lines.append("")
    try:
        heads = news_mod.gold_headlines()
        if heads:
            net = sum(h.sentiment for h in heads)
            mood = t(lang, "mood_bull" if net > 0
                     else "mood_bear" if net < 0 else "mood_mixed")
            lines.append(t(lang, "news_heads_header", mood=mood))
            for h in heads:
                mark = {1: "🟢", -1: "🔴", 0: "⚪"}[h.sentiment]
                lines.append(f"{mark} <a href=\"{h.link}\">"
                             f"{html.escape(h.title)}</a>")
    except Exception as ex:
        lines.append(t(lang, "news_heads_unavail", error=ex))
    return "\n".join(lines) + t(lang, "disclaimer")


def format_prediction(symbol: str, interval: str, pred: Prediction,
                      close: float, bar_ms: int, lang: str = "en") -> str:
    icon = {"BULLISH": "📈", "BEARISH": "📉", "NEUTRAL": "➖"}[pred.direction]
    ts = datetime.fromtimestamp(bar_ms / 1000, tz=timezone.utc)
    lines = [
        f"{icon} <b>{symbol} {interval}</b> — "
        f"<b>{i18n.direction(lang, pred.direction)}</b>",
        t(lang, "pred_stats", score=f"{pred.score:+.3f}",
          conf=f"{pred.confidence:.0f}", agr=f"{pred.agreement * 100:.0f}"),
        t(lang, "pred_close", close=f"{close:.2f}", ts=f"{ts:%Y-%m-%d %H:%M}"),
        "",
    ]
    ordered = sorted(pred.signals.items(), key=lambda kv: -abs(kv[1].score))
    for name, sig in ordered:
        if sig.score == 0.0:
            continue
        mark = "🟢" if sig.score > 0 else "🔴"
        reason = i18n.translate_reason(sig.reason, lang)
        lines.append(f"{mark} <code>{sig.score:+.2f}</code> "
                     f"<b>{i18n.strategy_name(lang, name)}</b>: "
                     f"{html.escape(reason)}")
    quiet = sum(1 for s in pred.signals.values() if s.score == 0.0)
    if quiet:
        lines.append(t(lang, "neutral_count", n=quiet))
    return "\n".join(lines) + t(lang, "disclaimer")


def parse_args_text(parts: list[str]) -> tuple[str, str, list[str]]:
    """Parse '[symbol] [interval]' in either order; returns (symbol, interval, rest)."""
    symbol, interval = DEFAULT_SYMBOL, "1h"
    rest = []
    for p in parts:
        if p.lower() in INTERVAL_SECONDS:
            interval = p.lower()
        elif p.isdigit():
            rest.append(p)
        else:
            symbol = p.upper()
    return symbol, interval, rest


class Bot:
    def __init__(self, token: str, allowed: set[int] | None):
        self.api = TelegramAPI(token)
        self.allowed = allowed
        self.engine = Engine()
        self.lock = threading.Lock()
        self.subs: dict[str, dict] = self._load_json(SUBS_FILE)
        self.langs: dict[str, str] = self._load_json(LANGS_FILE)

    # ---------- persistence ----------

    @staticmethod
    def _load_json(path: str) -> dict:
        try:
            with open(path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_subs(self):
        with open(SUBS_FILE, "w") as f:
            json.dump(self.subs, f, indent=2)

    def _save_langs(self):
        with open(LANGS_FILE, "w") as f:
            json.dump(self.langs, f, indent=2)

    def lang(self, chat_id: int) -> str:
        return self.langs.get(str(chat_id), "en")

    # ---------- command handling ----------

    def handle(self, chat_id: int, text: str, tg_lang: str | None = None):
        key = str(chat_id)
        # first contact: adopt the user's Telegram client language if we
        # support it and they haven't chosen one explicitly
        if key not in self.langs and tg_lang:
            code = tg_lang.split("-")[0].lower()
            if code in i18n.LANGS:
                self.langs[key] = code
                self._save_langs()
        lang = self.lang(chat_id)
        if self.allowed and chat_id not in self.allowed:
            self.api.send(chat_id, t(lang, "private"))
            return
        parts = text.split()
        cmd = parts[0].split("@")[0].lower()
        args = parts[1:]
        if cmd == "/start":
            self.api.send(chat_id, t(lang, "intro") + t(lang, "disclaimer"))
        elif cmd == "/help":
            self.api.send(chat_id, t(lang, "help") + t(lang, "disclaimer"))
        elif cmd in ("/lang", "/language"):
            self.cmd_lang(chat_id, args)
        elif cmd == "/predict":
            self.cmd_predict(chat_id, args)
        elif cmd == "/backtest":
            self.cmd_backtest(chat_id, args)
        elif cmd == "/news":
            self.api.send(chat_id, format_news(lang))
        elif cmd == "/watch":
            self.cmd_watch(chat_id, args)
        elif cmd == "/unwatch":
            with self.lock:
                removed = self.subs.pop(key, None)
                self._save_subs()
            self.api.send(chat_id, t(lang, "unwatch_ok") if removed
                          else t(lang, "unwatch_none"))
        elif cmd == "/status":
            sub = self.subs.get(key)
            if sub:
                last = sub.get("last_direction")
                self.api.send(chat_id, t(
                    lang, "status_active", symbol=sub["symbol"],
                    interval=sub["interval"], min=sub["every_min"],
                    dir=i18n.direction(lang, last) if last else "—"))
            else:
                self.api.send(chat_id, t(lang, "status_none"))
        elif cmd.startswith("/"):
            self.api.send(chat_id, t(lang, "unknown_cmd"))

    def cmd_lang(self, chat_id: int, args: list[str]):
        choice = args[0].lower() if args else None
        if choice in i18n.LANGS:
            self.langs[str(chat_id)] = choice
            self._save_langs()
            self.api.send(chat_id, t(choice, "lang_set"))
        else:
            self.api.send(chat_id, t(self.lang(chat_id), "lang_usage"))

    def cmd_predict(self, chat_id: int, args: list[str]):
        lang = self.lang(chat_id)
        symbol, interval, _ = parse_args_text(args)
        self.api.send(chat_id, t(lang, "crunching", symbol=symbol,
                                 interval=interval))
        try:
            candles = fetch_klines(symbol, interval, 600)
            pred = self.engine.predict(candles)
            self.api.send(chat_id, format_prediction(
                symbol, interval, pred, candles[-1].close,
                candles[-1].open_time, lang) + spot_quote_line(symbol, lang)
                + event_risk_line(lang))
        except Exception as e:
            self.api.send(chat_id, t(lang, "failed", error=e))

    def cmd_backtest(self, chat_id: int, args: list[str]):
        lang = self.lang(chat_id)
        symbol, interval, _ = parse_args_text(args)
        self.api.send(chat_id, t(lang, "backtesting", symbol=symbol,
                                 interval=interval))
        try:
            candles = fetch_klines(symbol, interval, 1500)
            result = run_backtest(candles, engine=self.engine, threshold=0.3)
            self.api.send(chat_id, "<pre>" + html.escape(result.summary())
                          + "</pre>" + t(lang, "disclaimer"))
        except Exception as e:
            self.api.send(chat_id, t(lang, "failed", error=e))

    def cmd_watch(self, chat_id: int, args: list[str]):
        lang = self.lang(chat_id)
        send_all = any(a.lower() in ("all", "every", "always") for a in args)
        args = [a for a in args
                if a.lower() not in ("all", "every", "always", "flips")]
        symbol, interval, rest = parse_args_text(args)
        every_min = max(5, int(rest[0])) if rest else 15
        with self.lock:
            self.subs[str(chat_id)] = {
                "symbol": symbol, "interval": interval,
                "every_min": every_min, "next_check": 0,
                "last_direction": None, "mode": "all" if send_all else "flip",
            }
            self._save_subs()
        self.api.send(chat_id, t(
            lang, "watching_all" if send_all else "watching_flip",
            symbol=symbol, interval=interval, min=every_min))

    # ---------- alert loop (background thread) ----------

    def alert_loop(self):
        while True:
            now = time.time()
            with self.lock:
                due = [(cid, dict(sub)) for cid, sub in self.subs.items()
                       if sub["next_check"] <= now]
            for cid, sub in due:
                self._check_subscription(int(cid), sub)
            time.sleep(20)

    def _check_subscription(self, chat_id: int, sub: dict):
        key = str(chat_id)
        lang = self.lang(chat_id)
        try:
            candles = fetch_klines(sub["symbol"], sub["interval"], 600)
            pred = self.engine.predict(candles)
            prev = sub.get("last_direction")
            flipped = prev is not None and pred.direction != prev
            if flipped or sub.get("mode") == "all":
                head = (t(lang, "flow_flipped", symbol=sub["symbol"],
                          interval=sub["interval"],
                          prev=i18n.direction(lang, prev),
                          new=i18n.direction(lang, pred.direction)) + "\n\n"
                        if flipped else "")
                self.api.send(chat_id,
                              head + format_prediction(
                                  sub["symbol"], sub["interval"], pred,
                                  candles[-1].close, candles[-1].open_time,
                                  lang)
                              + spot_quote_line(sub["symbol"], lang)
                              + event_risk_line(lang))
            with self.lock:
                if key in self.subs:
                    self.subs[key]["last_direction"] = pred.direction
                    self.subs[key]["next_check"] = (time.time()
                                                    + sub["every_min"] * 60)
                    self._save_subs()
        except Exception as e:
            print(f"[alert] check failed for {chat_id}: {e}")
            with self.lock:
                if key in self.subs:  # back off 5 min on failure
                    self.subs[key]["next_check"] = time.time() + 300

    # ---------- main loop ----------

    def setup_profile(self):
        """Set the bot's intro screen and command menu (all languages).

        Shown by Telegram before the user presses Start and as the "/"
        command autocomplete. Best-effort: profile cosmetics must never
        prevent the bot from starting.
        """
        for code, profile in i18n.BOT_PROFILE.items():
            scope = {} if code == "en" else {"language_code": code}
            try:
                self.api.call("setMyShortDescription",
                              short_description=profile["short"], **scope)
                self.api.call("setMyDescription",
                              description=profile["full"], **scope)
                self.api.call("setMyCommands", commands=json.dumps(
                    [{"command": c, "description": d}
                     for c, d in profile["commands"]]), **scope)
            except Exception as e:
                print(f"[profile] {code}: {e}")

    def run(self):
        me = self.api.call("getMe")
        self.setup_profile()
        print(f"running as @{me['username']} — press Ctrl-C to stop")
        threading.Thread(target=self.alert_loop, daemon=True).start()
        offset = None
        while True:
            try:
                updates = self.api.get_updates(offset)
            except Exception as e:
                print(f"[poll] {e}; retrying in 5s")
                time.sleep(5)
                continue
            for u in updates:
                offset = u["update_id"] + 1
                msg = u.get("message") or {}
                text = msg.get("text")
                chat = msg.get("chat", {}).get("id")
                tg_lang = (msg.get("from") or {}).get("language_code")
                if text and chat:
                    try:
                        self.handle(chat, text, tg_lang)
                    except Exception as e:
                        print(f"[handle] {e}")


def main():
    p = argparse.ArgumentParser(description="MarketFlow Telegram bot")
    p.add_argument("--token", default=os.environ.get("TELEGRAM_BOT_TOKEN"),
                   help="bot token (or set TELEGRAM_BOT_TOKEN)")
    args = p.parse_args()
    if not args.token:
        p.error("no token: set TELEGRAM_BOT_TOKEN or pass --token "
                "(get one from @BotFather on Telegram)")
    allowed_env = os.environ.get("TELEGRAM_ALLOWED_CHATS", "").strip()
    allowed = ({int(x) for x in allowed_env.split(",") if x.strip()}
               if allowed_env else None)
    Bot(args.token, allowed).run()


if __name__ == "__main__":
    main()
