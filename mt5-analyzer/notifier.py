"""Signal output: CSV journal + Telegram notification (stdlib urllib)."""

from __future__ import annotations

import csv
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from strategy import TradeSignal, local_dt

CSV_FIELDS = ["time_utc", "side", "entry", "sl", "tp", "rsi_prev", "rsi_now",
              "h4_trend", "reason"]


def _csv_path(cfg: dict) -> str:
    path = cfg.get("signals_csv", "signals.csv")
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    return path


def log_csv(sig: TradeSignal, cfg: dict) -> None:
    path = _csv_path(cfg)
    new_file = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new_file:
            w.writeheader()
        w.writerow({
            "time_utc": datetime.fromtimestamp(
                sig.time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M"),
            "side": sig.side, "entry": f"{sig.entry:.2f}",
            "sl": f"{sig.sl:.2f}", "tp": f"{sig.tp:.2f}",
            "rsi_prev": f"{sig.rsi_prev:.1f}", "rsi_now": f"{sig.rsi_now:.1f}",
            "h4_trend": sig.h4_trend, "reason": sig.reason,
        })


def signals_today(cfg: dict, local_date) -> int:
    """Count today's already-logged signals (survives restarts)."""
    path = _csv_path(cfg)
    if not os.path.exists(path):
        return 0
    count = 0
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            ts = int(datetime.strptime(row["time_utc"], "%Y-%m-%d %H:%M")
                     .replace(tzinfo=timezone.utc).timestamp())
            if local_dt(ts, cfg).date() == local_date:
                count += 1
    return count


def notify_telegram(sig: TradeSignal, cfg: dict) -> bool:
    token = cfg.get("telegram_token")
    chat_id = cfg.get("telegram_chat_id")
    if not token or not chat_id:
        return False
    icon = "🟢 LONG" if sig.side == "LONG" else "🔴 SHORT"
    when = datetime.fromtimestamp(sig.time, tz=timezone.utc)
    text = (f"{icon} <b>{cfg['symbol']} H1</b>\n"
            f"entry <code>{sig.entry:.2f}</code> · SL <code>{sig.sl:.2f}</code>"
            f" · TP <code>{sig.tp:.2f}</code> (RR 1:{cfg['rr']:g})\n"
            f"{sig.reason}\n{when:%Y-%m-%d %H:%M} UTC")
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text,
                                   "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode()).get("ok", False)
    except Exception as e:
        print(f"[telegram] failed: {e}")
        return False
