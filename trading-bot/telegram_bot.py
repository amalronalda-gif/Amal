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

from marketflow.data import DEFAULT_SYMBOL, INTERVAL_SECONDS, fetch_klines
from marketflow.engine import Engine, Prediction
from marketflow.backtest import run_backtest

SUBS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "subscriptions.json")
DISCLAIMER = "\n<i>Educational signals, not financial advice.</i>"

HELP = """<b>MarketFlow bot</b> — multi-strategy market flow reading for gold/USDT

/predict [symbol] [interval] — current prediction with strategy breakdown
/backtest [symbol] [interval] — walk-forward backtest
/watch [symbol] [interval] [minutes] — alert when the flow direction flips
/unwatch — stop alerts
/status — show your watch subscription

Defaults: symbol <code>PAXGUSDT</code> (tokenized gold = XAUUSDT equivalent), \
interval <code>1h</code>, check every 15 min.
Examples:
<code>/predict 4h</code>
<code>/predict BTCUSDT 15m</code>
<code>/watch 1h 30</code>""" + DISCLAIMER


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


def format_prediction(symbol: str, interval: str, pred: Prediction,
                      close: float, bar_ms: int) -> str:
    icon = {"BULLISH": "📈", "BEARISH": "📉", "NEUTRAL": "➖"}[pred.direction]
    ts = datetime.fromtimestamp(bar_ms / 1000, tz=timezone.utc)
    lines = [
        f"{icon} <b>{symbol} {interval}</b> — <b>{pred.direction}</b>",
        f"score <code>{pred.score:+.3f}</code> · confidence "
        f"<code>{pred.confidence:.0f}%</code> · agreement "
        f"<code>{pred.agreement * 100:.0f}%</code>",
        f"close <code>{close:.2f}</code> · bar {ts:%Y-%m-%d %H:%M} UTC",
        "",
    ]
    ordered = sorted(pred.signals.items(), key=lambda kv: -abs(kv[1].score))
    for name, sig in ordered:
        if sig.score == 0.0:
            continue
        mark = "🟢" if sig.score > 0 else "🔴"
        lines.append(f"{mark} <code>{sig.score:+.2f}</code> "
                     f"<b>{name}</b>: {html.escape(sig.reason)}")
    quiet = sum(1 for s in pred.signals.values() if s.score == 0.0)
    if quiet:
        lines.append(f"⚪ {quiet} strategies neutral")
    return "\n".join(lines) + DISCLAIMER


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
        self.subs: dict[str, dict] = self._load_subs()

    # ---------- subscriptions ----------

    def _load_subs(self) -> dict:
        try:
            with open(SUBS_FILE) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_subs(self):
        with open(SUBS_FILE, "w") as f:
            json.dump(self.subs, f, indent=2)

    # ---------- command handling ----------

    def handle(self, chat_id: int, text: str):
        if self.allowed and chat_id not in self.allowed:
            self.api.send(chat_id, "Sorry, this bot is private.")
            return
        parts = text.split()
        cmd = parts[0].split("@")[0].lower()
        args = parts[1:]
        if cmd in ("/start", "/help"):
            self.api.send(chat_id, HELP)
        elif cmd == "/predict":
            self.cmd_predict(chat_id, args)
        elif cmd == "/backtest":
            self.cmd_backtest(chat_id, args)
        elif cmd == "/watch":
            self.cmd_watch(chat_id, args)
        elif cmd == "/unwatch":
            with self.lock:
                removed = self.subs.pop(str(chat_id), None)
                self._save_subs()
            self.api.send(chat_id, "Alerts stopped." if removed
                          else "You had no active watch.")
        elif cmd == "/status":
            sub = self.subs.get(str(chat_id))
            if sub:
                self.api.send(chat_id,
                              f"Watching <b>{sub['symbol']} {sub['interval']}</b> "
                              f"every {sub['every_min']} min; last flow: "
                              f"{sub.get('last_direction', '—')}")
            else:
                self.api.send(chat_id, "No active watch. Use /watch to start.")
        elif cmd.startswith("/"):
            self.api.send(chat_id, "Unknown command — try /help")

    def cmd_predict(self, chat_id: int, args: list[str]):
        symbol, interval, _ = parse_args_text(args)
        self.api.send(chat_id, f"Crunching {symbol} {interval}…")
        try:
            candles = fetch_klines(symbol, interval, 600)
            pred = self.engine.predict(candles)
            self.api.send(chat_id, format_prediction(
                symbol, interval, pred, candles[-1].close,
                candles[-1].open_time))
        except Exception as e:
            self.api.send(chat_id, f"⚠️ failed: {e}")

    def cmd_backtest(self, chat_id: int, args: list[str]):
        symbol, interval, _ = parse_args_text(args)
        self.api.send(chat_id, f"Backtesting {symbol} {interval} "
                               f"(1500 bars), this takes a moment…")
        try:
            candles = fetch_klines(symbol, interval, 1500)
            result = run_backtest(candles, engine=self.engine, threshold=0.3)
            self.api.send(chat_id, "<pre>" + html.escape(result.summary())
                          + "</pre>" + DISCLAIMER)
        except Exception as e:
            self.api.send(chat_id, f"⚠️ failed: {e}")

    def cmd_watch(self, chat_id: int, args: list[str]):
        symbol, interval, rest = parse_args_text(args)
        every_min = max(5, int(rest[0])) if rest else 15
        with self.lock:
            self.subs[str(chat_id)] = {
                "symbol": symbol, "interval": interval,
                "every_min": every_min, "next_check": 0,
                "last_direction": None,
            }
            self._save_subs()
        self.api.send(chat_id,
                      f"👁 Watching <b>{symbol} {interval}</b>, checking every "
                      f"{every_min} min. I'll message you when the market flow "
                      f"direction flips. /unwatch to stop.")

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
        try:
            candles = fetch_klines(sub["symbol"], sub["interval"], 600)
            pred = self.engine.predict(candles)
            prev = sub.get("last_direction")
            if prev is not None and pred.direction != prev:
                self.api.send(chat_id,
                              f"🔔 <b>{sub['symbol']} {sub['interval']}</b> "
                              f"flow flipped: {prev} → <b>{pred.direction}</b>\n\n"
                              + format_prediction(sub["symbol"], sub["interval"],
                                                  pred, candles[-1].close,
                                                  candles[-1].open_time))
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

    def run(self):
        me = self.api.call("getMe")
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
                if text and chat:
                    try:
                        self.handle(chat, text)
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
