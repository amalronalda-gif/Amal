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

from marketflow.data import (DEFAULT_SYMBOL, INTERVAL_SECONDS, SPOT_QUOTES,
                             SUPPORTED_MARKETS, SYMBOL_ALIASES, fetch_klines,
                             fetch_tradingview_quote, fx_market_open)

try:
    from zoneinfo import ZoneInfo
    _LONDON = ZoneInfo("Europe/London")
except Exception:
    _LONDON = None
from marketflow.engine import Prediction, engine_for
from marketflow.backtest import run_backtest
from marketflow.indicators import atr as atr_indicator
from marketflow.strategies import Signal
from marketflow import news as news_mod
from marketflow import i18n
from marketflow.i18n import t

_HERE = os.path.dirname(os.path.abspath(__file__))
SUBS_FILE = os.path.join(_HERE, "subscriptions.json")
LANGS_FILE = os.path.join(_HERE, "user_langs.json")
PRED_LOG_FILE = os.path.join(_HERE, "predictions_log.json")
PAPER_FILE = os.path.join(_HERE, "paper_accounts.json")
STATS_HORIZON = 12          # bars ahead a prediction is judged against
MTF_INTERVALS = ("15m", "1h", "4h")
ACCOUNT_USD = 100.0         # reference deposit for position sizing
RISK_PCT = 1.0              # % of the account risked per trade
PAPER_START = 100.0         # paper-trader starting balance
PAPER_GOAL = 1200.0         # paper-trader target balance
PAPER_THRESHOLD = 0.23      # |score| needed to open a paper trade
PAPER_MAX_HOLD = 48         # bars before a paper position is closed at market
PAPER_MIN_BALANCE = 10.0    # stop trading below this (account blown)
ASSET_LABELS = {"PAXGUSDT": "XAU (oz)", "XAUTUSDT": "XAU (oz)",
                "BTCUSDT": "BTC"}


def news_signal(symbol: str) -> dict[str, Signal] | None:
    """Headline sentiment as an extra ensemble input (live only)."""
    resolved = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
    res = news_mod.sentiment_for(resolved)
    if not res:
        return None
    score, pos, total = res
    if score > 0:
        reason = f"headlines lean bullish ({pos}/{total})"
    elif score < 0:
        reason = f"headlines lean bearish ({total - pos}/{total})"
    else:
        return None
    return {"news_sentiment": Signal(score * 0.8, reason)}


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
    """Live spot quote from TradingView for markets we have a feed for."""
    resolved = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
    feed = SPOT_QUOTES.get(resolved)
    if not feed:
        return ""
    tv_symbol, pair = feed
    q = fetch_tradingview_quote(tv_symbol)
    if not q:
        return ""
    digits = 5 if q["close"] < 10 else 2  # FX pairs need more precision
    line = t(lang, "spot_line", pair=pair,
             price=f"{q['close']:.{digits}f}",
             chg=f"{q.get('change', 0):+.2f}",
             high=f"{q.get('high', 0):.{digits}f}",
             low=f"{q.get('low', 0):.{digits}f}")
    if not fx_market_open():
        line += t(lang, "market_closed") + t(lang, "market_closed_crypto")
    return line


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


def trade_plan_line(candles, pred: Prediction, lang: str = "en",
                    symbol: str = "") -> str:
    """ATR-based entry/stop/target suggestion for non-neutral signals.

    Mirrors the backtester's exits (1.5 ATR stop, 3 ATR target = 1:2 R:R)
    so the suggestion matches what the published stats were measured on.
    Position size is computed for a $ACCOUNT_USD account risking RISK_PCT%.
    """
    if pred.direction == "NEUTRAL":
        return ""
    a = atr_indicator(candles, 14)[-1]
    if not a:
        return ""
    entry = candles[-1].close
    side = 1 if pred.direction == "BULLISH" else -1
    stop = entry - side * 1.5 * a
    target = entry + side * 3.0 * a
    digits = 5 if entry < 10 else 2
    line = t(lang, "plan",
             entry=f"{entry:.{digits}f}", stop=f"{stop:.{digits}f}",
             target=f"{target:.{digits}f}",
             sd=f"{(stop / entry - 1) * 100:+.2f}",
             td=f"{(target / entry - 1) * 100:+.2f}")
    risk_usd = ACCOUNT_USD * RISK_PCT / 100.0
    units = risk_usd / abs(entry - stop)
    resolved = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
    line += t(lang, "plan_money",
              account=f"{ACCOUNT_USD:.0f}", risk=f"{risk_usd:.2f}",
              units=f"{units:.4g}",
              asset=ASSET_LABELS.get(resolved, resolved),
              notional=f"{units * entry:.0f}",
              loss=f"{risk_usd:.2f}", win=f"{risk_usd * 2:.2f}")
    return line


def format_prediction(symbol: str, interval: str, pred: Prediction,
                      close: float, bar_ms: int, lang: str = "en") -> str:
    icon = {"BULLISH": "📈", "BEARISH": "📉", "NEUTRAL": "➖"}[pred.direction]
    ts = datetime.fromtimestamp(bar_ms / 1000, tz=timezone.utc)
    uk = f"{ts.astimezone(_LONDON):%H:%M}" if _LONDON else "—"
    digits = 5 if close < 10 else 2
    lines = [
        f"{icon} <b>{symbol} {interval}</b> — "
        f"<b>{i18n.direction(lang, pred.direction)}</b>",
        t(lang, "pred_stats", score=f"{pred.score:+.3f}",
          conf=f"{pred.confidence:.0f}", agr=f"{pred.agreement * 100:.0f}"),
        t(lang, "pred_close", close=f"{close:.{digits}f}",
          ts=f"{ts:%Y-%m-%d %H:%M}", uk=uk),
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
        self.lock = threading.Lock()
        self.subs: dict[str, dict] = self._load_json(SUBS_FILE)
        self.langs: dict[str, str] = self._load_json(LANGS_FILE)
        try:
            with open(PRED_LOG_FILE) as f:
                self.pred_log: list[dict] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.pred_log = []
        self.paper: dict[str, dict] = self._load_json(PAPER_FILE)

    def _save_paper(self):
        with open(PAPER_FILE, "w") as f:
            json.dump(self.paper, f, indent=2)

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

    def _log_prediction(self, symbol: str, interval: str, candles, pred):
        """Record non-neutral calls so /stats can grade them later."""
        if pred.direction == "NEUTRAL":
            return
        resolved = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
        with self.lock:
            self.pred_log.append({
                "bar": candles[-1].open_time, "symbol": resolved,
                "interval": interval, "direction": pred.direction,
                "score": round(pred.score, 3), "close": candles[-1].close,
            })
            self.pred_log = self.pred_log[-1000:]
            with open(PRED_LOG_FILE, "w") as f:
                json.dump(self.pred_log, f)

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
        elif cmd == "/mtf":
            self.cmd_mtf(chat_id, args)
        elif cmd == "/stats":
            self.cmd_stats(chat_id)
        elif cmd == "/trade":
            self.cmd_trade(chat_id, args)
        elif cmd == "/account":
            self.cmd_account(chat_id)
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

    def _symbol_ok(self, chat_id: int, symbol: str, lang: str) -> bool:
        resolved = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
        if resolved in SUPPORTED_MARKETS:
            return True
        self.api.send(chat_id, t(lang, "unsupported_symbol"))
        return False

    def cmd_predict(self, chat_id: int, args: list[str]):
        lang = self.lang(chat_id)
        symbol, interval, _ = parse_args_text(args)
        if not self._symbol_ok(chat_id, symbol, lang):
            return
        self.api.send(chat_id, t(lang, "crunching", symbol=symbol,
                                 interval=interval))
        try:
            candles = fetch_klines(symbol, interval, 600)
            pred = engine_for(symbol).predict(candles, news_signal(symbol))
            self._log_prediction(symbol, interval, candles, pred)
            self.api.send(chat_id, format_prediction(
                symbol, interval, pred, candles[-1].close,
                candles[-1].open_time, lang)
                + trade_plan_line(candles, pred, lang, symbol)
                + spot_quote_line(symbol, lang)
                + event_risk_line(lang))
        except Exception as e:
            self.api.send(chat_id, t(lang, "failed", error=e))

    def cmd_mtf(self, chat_id: int, args: list[str]):
        lang = self.lang(chat_id)
        symbol, _, _ = parse_args_text(args)
        if not self._symbol_ok(chat_id, symbol, lang):
            return
        self.api.send(chat_id, t(lang, "crunching", symbol=symbol,
                                 interval="+".join(MTF_INTERVALS)))
        try:
            engine = engine_for(symbol)
            lines = [t(lang, "mtf_header", symbol=symbol), ""]
            directions = []
            for interval in MTF_INTERVALS:
                candles = fetch_klines(symbol, interval, 600)
                pred = engine.predict(candles)
                directions.append(pred.direction)
                icon = {"BULLISH": "📈", "BEARISH": "📉",
                        "NEUTRAL": "➖"}[pred.direction]
                lines.append(f"{icon} <code>{interval:>3}</code> "
                             f"<b>{i18n.direction(lang, pred.direction)}</b> "
                             f"(<code>{pred.score:+.3f}</code>, "
                             f"{pred.confidence:.0f}%)")
            lines.append("")
            non_neutral = [d for d in directions if d != "NEUTRAL"]
            if non_neutral and len(set(directions)) == 1:
                lines.append(t(lang, "mtf_aligned",
                               dir=i18n.direction(lang, directions[0])))
            else:
                lines.append(t(lang, "mtf_mixed"))
            self.api.send(chat_id, "\n".join(lines) + t(lang, "disclaimer"))
        except Exception as e:
            self.api.send(chat_id, t(lang, "failed", error=e))

    def cmd_stats(self, chat_id: int):
        lang = self.lang(chat_id)
        with self.lock:
            entries = list(self.pred_log)
        if not entries:
            self.api.send(chat_id, t(lang, "stats_none"))
            return
        markets = {}
        for e in entries:
            markets.setdefault((e["symbol"], e["interval"]), []).append(e)
        per_market = []
        total_hits = total_eval = pending = 0
        for (symbol, interval), group in markets.items():
            try:
                candles = fetch_klines(symbol, interval, 1000)
            except Exception:
                continue
            index = {c.open_time: i for i, c in enumerate(candles)}
            hits = evaluated = 0
            for e in group:
                i = index.get(e["bar"])
                if i is None:
                    continue  # too old for the fetched window
                j = i + STATS_HORIZON
                if j >= len(candles):
                    pending += 1
                    continue
                fwd = candles[j].close - e["close"]
                if fwd == 0:
                    continue
                evaluated += 1
                if (fwd > 0) == (e["direction"] == "BULLISH"):
                    hits += 1
            if evaluated:
                per_market.append(t(lang, "stats_line", symbol=symbol,
                                    interval=interval, hits=hits,
                                    total=evaluated,
                                    pct=f"{hits / evaluated * 100:.0f}"))
                total_hits += hits
                total_eval += evaluated
        if not total_eval:
            msg = t(lang, "stats_none")
            if pending:
                msg += "\n" + t(lang, "stats_pending", n=pending)
            self.api.send(chat_id, msg)
            return
        lines = [t(lang, "stats_header", h=STATS_HORIZON), ""]
        lines += per_market
        lines.append("")
        lines.append(t(lang, "stats_total", hits=total_hits, total=total_eval,
                       pct=f"{total_hits / total_eval * 100:.0f}"))
        if pending:
            lines.append(t(lang, "stats_pending", n=pending))
        self.api.send(chat_id, "\n".join(lines) + t(lang, "disclaimer"))

    def cmd_backtest(self, chat_id: int, args: list[str]):
        lang = self.lang(chat_id)
        symbol, interval, _ = parse_args_text(args)
        if not self._symbol_ok(chat_id, symbol, lang):
            return
        self.api.send(chat_id, t(lang, "backtesting", symbol=symbol,
                                 interval=interval))
        try:
            candles = fetch_klines(symbol, interval, 1500)
            result = run_backtest(candles, engine=engine_for(symbol),
                                  threshold=0.23)
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
        if not self._symbol_ok(chat_id, symbol, lang):
            return
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

    # ---------- paper trading ----------

    def cmd_trade(self, chat_id: int, args: list[str]):
        lang = self.lang(chat_id)
        key = str(chat_id)
        if any(a.lower() in ("off", "stop") for a in args):
            acct = self.paper.pop(key, None)
            with self.lock:
                self._save_paper()
            bal = f"{acct['balance']:.2f}" if acct else f"{PAPER_START:.0f}"
            self.api.send(chat_id, t(lang, "paper_off", balance=bal))
            return
        args = [a for a in args if a.lower() not in ("on", "start")]
        symbol, interval, rest = parse_args_text(args)
        if not self._symbol_ok(chat_id, symbol, lang):
            return
        risk = 2.0
        if rest:
            try:
                risk = min(5.0, max(0.5, float(rest[0])))
            except ValueError:
                pass
        with self.lock:
            self.paper[key] = {
                "symbol": symbol, "interval": interval, "risk_pct": risk,
                "balance": PAPER_START, "goal": PAPER_GOAL,
                "position": None, "wins": 0, "losses": 0, "trades": 0,
                "next_check": 0,
            }
            self._save_paper()
        self.api.send(chat_id, t(lang, "paper_on", symbol=symbol,
                                 interval=interval, risk=f"{risk:g}",
                                 balance=f"{PAPER_START:.0f}",
                                 goal=f"{PAPER_GOAL:.0f}")
                      + t(lang, "paper_expect"))

    def cmd_account(self, chat_id: int):
        lang = self.lang(chat_id)
        acct = self.paper.get(str(chat_id))
        if not acct:
            self.api.send(chat_id, t(lang, "paper_none"))
            return
        pos = acct.get("position")
        if pos:
            digits = 5 if pos["entry"] < 10 else 2
            pos_line = t(lang, "account_pos",
                         dir=i18n.direction(lang, "BULLISH" if pos["dir"] == 1
                                            else "BEARISH"),
                         symbol=acct["symbol"],
                         entry=f"{pos['entry']:.{digits}f}",
                         stop=f"{pos['stop']:.{digits}f}",
                         target=f"{pos['target']:.{digits}f}")
        else:
            pos_line = t(lang, "account_nopos")
        pct = acct["balance"] / acct["goal"] * 100
        self.api.send(chat_id, t(
            lang, "account", balance=f"{acct['balance']:.2f}",
            goal=f"{acct['goal']:.0f}", pct=f"{pct:.1f}",
            n=acct["trades"], wins=acct["wins"], losses=acct["losses"],
            position=pos_line))

    def _check_paper(self, chat_id: int, acct: dict):
        key = str(chat_id)
        lang = self.lang(chat_id)
        try:
            candles = fetch_klines(acct["symbol"], acct["interval"], 600)
            pos = acct.get("position")
            if pos:
                self._paper_manage_position(chat_id, acct, candles, lang)
            elif acct["balance"] >= PAPER_MIN_BALANCE:
                self._paper_maybe_open(chat_id, acct, candles, lang)
            with self.lock:
                if key in self.paper:
                    self.paper[key] = acct
                    self.paper[key]["next_check"] = time.time() + 300
                    self._save_paper()
        except Exception as e:
            print(f"[paper] check failed for {chat_id}: {e}")
            with self.lock:
                if key in self.paper:
                    self.paper[key]["next_check"] = time.time() + 300
                    self._save_paper()

    def _paper_maybe_open(self, chat_id: int, acct: dict, candles, lang: str):
        pred = engine_for(acct["symbol"]).predict(
            candles, news_signal(acct["symbol"]))
        if abs(pred.score) < PAPER_THRESHOLD:
            return
        a = atr_indicator(candles, 14)[-1]
        if not a:
            return
        direction = 1 if pred.score > 0 else -1
        entry = candles[-1].close
        risk_usd = acct["balance"] * acct["risk_pct"] / 100.0
        acct["position"] = {
            "dir": direction, "entry": entry,
            "stop": entry - direction * 1.5 * a,
            "target": entry + direction * 3.0 * a,
            "risk_usd": risk_usd, "opened": candles[-1].open_time,
        }
        pos = acct["position"]
        digits = 5 if entry < 10 else 2
        self.api.send(chat_id, t(
            lang, "paper_opened",
            dir=i18n.direction(lang, "BULLISH" if direction == 1 else "BEARISH"),
            symbol=acct["symbol"], entry=f"{entry:.{digits}f}",
            stop=f"{pos['stop']:.{digits}f}",
            target=f"{pos['target']:.{digits}f}", risk=f"{risk_usd:.2f}"))

    def _paper_manage_position(self, chat_id: int, acct: dict, candles,
                               lang: str):
        pos = acct["position"]
        since = [c for c in candles if c.open_time > pos["opened"]]
        outcome = None
        exit_px = None
        for c in since:  # conservative: stop checked before target
            if pos["dir"] == 1:
                if c.low <= pos["stop"]:
                    outcome, exit_px = "loss", pos["stop"]
                    break
                if c.high >= pos["target"]:
                    outcome, exit_px = "win", pos["target"]
                    break
            else:
                if c.high >= pos["stop"]:
                    outcome, exit_px = "loss", pos["stop"]
                    break
                if c.low <= pos["target"]:
                    outcome, exit_px = "win", pos["target"]
                    break
        if outcome is None and len(since) >= PAPER_MAX_HOLD:
            outcome, exit_px = "time", since[-1].close
        if outcome is None:
            return
        risk = pos["risk_usd"]
        r_mult = ((exit_px - pos["entry"]) * pos["dir"]
                  / abs(pos["entry"] - pos["stop"]))
        pnl = r_mult * risk
        acct["balance"] = max(0.0, acct["balance"] + pnl)
        acct["trades"] += 1
        acct["wins" if pnl > 0 else "losses"] += 1
        acct["position"] = None
        pct = acct["balance"] / acct["goal"] * 100
        msg_key = {"win": "paper_closed_win", "loss": "paper_closed_loss",
                   "time": "paper_closed_time"}[outcome]
        self.api.send(chat_id, t(
            lang, msg_key, pnl=f"{abs(pnl):.2f}",
            sign="+" if pnl >= 0 else "−",
            balance=f"{acct['balance']:.2f}", goal=f"{acct['goal']:.0f}",
            pct=f"{pct:.1f}"))
        if acct["balance"] >= acct["goal"]:
            self.api.send(chat_id, t(lang, "paper_goal",
                                     balance=f"{acct['balance']:.2f}",
                                     goal=f"{acct['goal']:.0f}"))
        elif acct["balance"] < PAPER_MIN_BALANCE:
            self.api.send(chat_id, t(lang, "paper_blown"))

    # ---------- alert loop (background thread) ----------

    def alert_loop(self):
        while True:
            now = time.time()
            with self.lock:
                due = [(cid, dict(sub)) for cid, sub in self.subs.items()
                       if sub["next_check"] <= now]
                paper_due = [(cid, dict(acct))
                             for cid, acct in self.paper.items()
                             if acct["next_check"] <= now]
            for cid, sub in due:
                self._check_subscription(int(cid), sub)
            for cid, acct in paper_due:
                self._check_paper(int(cid), acct)
            time.sleep(20)

    def _check_subscription(self, chat_id: int, sub: dict):
        key = str(chat_id)
        lang = self.lang(chat_id)
        try:
            candles = fetch_klines(sub["symbol"], sub["interval"], 600)
            pred = engine_for(sub["symbol"]).predict(
                candles, news_signal(sub["symbol"]))
            self._log_prediction(sub["symbol"], sub["interval"], candles, pred)
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
                              + trade_plan_line(candles, pred, lang,
                                                sub["symbol"])
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
