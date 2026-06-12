"""Data layer: MetaTrader5 terminal (live/backtest) and CSV fallback.

The MetaTrader5 package works on Windows with an installed MT5 terminal.
CSV mode exists so the strategy and backtester can be developed and tested
anywhere (columns: time,open,high,low,close — time as epoch seconds UTC or
'YYYY-MM-DD HH:MM').
"""

from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone

try:
    import MetaTrader5 as mt5
    HAVE_MT5 = True
except ImportError:
    mt5 = None
    HAVE_MT5 = False

_HERE = os.path.dirname(os.path.abspath(__file__))


def load_config(path: str | None = None) -> dict:
    with open(path or os.path.join(_HERE, "config.json")) as f:
        return json.load(f)


@dataclass(frozen=True)
class Bar:
    time: int      # bar OPEN time, epoch seconds UTC
    open: float
    high: float
    low: float
    close: float

    @property
    def bullish(self) -> bool:
        return self.close > self.open


TIMEFRAMES = {"M15": 15 * 60, "M30": 30 * 60, "H1": 3600, "H4": 4 * 3600,
              "D1": 24 * 3600}


def tf_seconds(tf: str) -> int:
    return TIMEFRAMES[tf]


def mt5_connect(cfg: dict) -> None:
    if not HAVE_MT5:
        raise RuntimeError(
            "MetaTrader5 package is not installed (Windows-only). "
            "Install with: pip install MetaTrader5 — and make sure the MT5 "
            "terminal is installed and logged in to a broker account.")
    kwargs = {}
    if cfg.get("mt5_terminal_path"):
        kwargs["path"] = cfg["mt5_terminal_path"]
    if not mt5.initialize(**kwargs):
        raise RuntimeError(f"mt5.initialize() failed: {mt5.last_error()}")
    if mt5.symbol_info(cfg["symbol"]) is None:
        mt5.symbol_select(cfg["symbol"], True)


def mt5_disconnect() -> None:
    if HAVE_MT5:
        mt5.shutdown()


def get_bars(symbol: str, timeframe: str, count: int,
             drop_forming: bool = True) -> list[Bar]:
    """Latest `count` bars from MT5, oldest first. The newest bar returned
    by MT5 is still forming; drop it for signal logic (no repainting)."""
    tf_map = {"M15": mt5.TIMEFRAME_M15, "M30": mt5.TIMEFRAME_M30,
              "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4,
              "D1": mt5.TIMEFRAME_D1}
    rates = mt5.copy_rates_from_pos(symbol, tf_map[timeframe], 0, count)
    if rates is None:
        raise RuntimeError(f"copy_rates_from_pos failed: {mt5.last_error()}")
    bars = [Bar(int(r["time"]), float(r["open"]), float(r["high"]),
                float(r["low"]), float(r["close"])) for r in rates]
    return bars[:-1] if drop_forming and bars else bars


def load_csv(path: str) -> list[Bar]:
    bars = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            t = row["time"]
            if t.isdigit():
                ts = int(t)
            else:
                ts = int(datetime.strptime(t, "%Y-%m-%d %H:%M")
                         .replace(tzinfo=timezone.utc).timestamp())
            bars.append(Bar(ts, float(row["open"]), float(row["high"]),
                            float(row["low"]), float(row["close"])))
    bars.sort(key=lambda b: b.time)
    return bars


def resample(bars: list[Bar], from_tf: str, to_tf: str) -> list[Bar]:
    """Aggregate e.g. H1 -> H4 (UTC-aligned buckets); lets CSV users supply
    a single H1 file."""
    step = tf_seconds(to_tf)
    out: list[Bar] = []
    group: list[Bar] = []
    bucket = None
    for b in bars:
        bk = b.time // step
        if bk != bucket and group:
            out.append(Bar(bucket * step, group[0].open,
                           max(x.high for x in group),
                           min(x.low for x in group), group[-1].close))
            group = []
        bucket = bk
        group.append(b)
    if group:
        out.append(Bar(bucket * step, group[0].open,
                       max(x.high for x in group),
                       min(x.low for x in group), group[-1].close))
    return out


# ---------------------------------------------------------------------------
# Binance source: lets the analyzer run anywhere (phone/Termux/Linux) with
# no MT5 terminal. Gold = PAXGUSDT (tokenized gold, tracks XAU/USD).
# ---------------------------------------------------------------------------

BINANCE_URL = "https://data-api.binance.vision/api/v3/klines"
BINANCE_SYMBOLS = {"XAUUSD": "PAXGUSDT", "BTCUSD": "BTCUSDT",
                   "EURUSD": "EURUSDT"}
BINANCE_TF = {"M15": "15m", "M30": "30m", "H1": "1h", "H4": "4h", "D1": "1d"}


def get_bars_binance(symbol: str, timeframe: str, count: int,
                     drop_forming: bool = True) -> list[Bar]:
    import urllib.request
    bsym = BINANCE_SYMBOLS.get(symbol.upper(), symbol.upper())
    bars: list[Bar] = []
    end = None
    remaining = count + 1  # +1 so we can drop the forming bar
    while remaining > 0:
        page = min(remaining, 1000)
        url = (f"{BINANCE_URL}?symbol={bsym}"
               f"&interval={BINANCE_TF[timeframe]}&limit={page}")
        if end is not None:
            url += f"&endTime={end}"
        req = urllib.request.Request(url,
                                     headers={"User-Agent": "mt5-analyzer"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            rows = json.loads(resp.read().decode())
        if not rows:
            break
        batch = [Bar(int(r[0]) // 1000, float(r[1]), float(r[2]),
                     float(r[3]), float(r[4])) for r in rows]
        bars = batch + bars
        remaining -= len(batch)
        end = rows[0][0] - 1
        if len(batch) < page:
            break
    return bars[:-1] if drop_forming and bars else bars
