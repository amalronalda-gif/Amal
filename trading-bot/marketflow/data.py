"""OHLCV data loading: Binance public market-data API, with CSV import/export.

Uses data-api.binance.vision (public mirror, no API key required).
XAUUSDT note: on Binance spot the tradable gold/USDT market is PAXGUSDT
(PAX Gold, 1 token = 1 troy oz of gold), which tracks XAU/USD closely.
"""

from __future__ import annotations

import csv
import json
import os
import time
import urllib.request
from dataclasses import dataclass

BINANCE_DATA_URL = "https://data-api.binance.vision/api/v3/klines"
DEFAULT_SYMBOL = "PAXGUSDT"

INTERVAL_SECONDS = {
    "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
    "1h": 3600, "2h": 7200, "4h": 14400, "6h": 21600, "12h": 43200,
    "1d": 86400, "1w": 604800,
}


@dataclass(frozen=True)
class Candle:
    open_time: int  # ms epoch
    open: float
    high: float
    low: float
    close: float
    volume: float

    @property
    def bullish(self) -> bool:
        return self.close > self.open

    @property
    def body(self) -> float:
        return abs(self.close - self.open)

    @property
    def range(self) -> float:
        return self.high - self.low

    @property
    def upper_wick(self) -> float:
        return self.high - max(self.open, self.close)

    @property
    def lower_wick(self) -> float:
        return min(self.open, self.close) - self.low


def fetch_klines(symbol: str = DEFAULT_SYMBOL, interval: str = "1h",
                 limit: int = 1000, retries: int = 3) -> list[Candle]:
    """Fetch up to `limit` recent candles (multiple pages if limit > 1000)."""
    if interval not in INTERVAL_SECONDS:
        raise ValueError(f"unsupported interval {interval!r}")
    candles: list[Candle] = []
    end_time: int | None = None
    remaining = limit
    while remaining > 0:
        page = min(remaining, 1000)
        url = f"{BINANCE_DATA_URL}?symbol={symbol}&interval={interval}&limit={page}"
        if end_time is not None:
            url += f"&endTime={end_time}"
        rows = _http_get_json(url, retries=retries)
        if not rows:
            break
        batch = [Candle(int(r[0]), float(r[1]), float(r[2]), float(r[3]),
                        float(r[4]), float(r[5])) for r in rows]
        candles = batch + candles
        remaining -= len(batch)
        end_time = batch[0].open_time - 1
        if len(batch) < page:
            break
    return candles


def _http_get_json(url: str, retries: int = 3):
    delay = 2.0
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "marketflow/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            if attempt == retries:
                raise
            time.sleep(delay)
            delay *= 2


def save_csv(candles: list[Candle], path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["open_time", "open", "high", "low", "close", "volume"])
        for c in candles:
            w.writerow([c.open_time, c.open, c.high, c.low, c.close, c.volume])


def load_csv(path: str) -> list[Candle]:
    candles = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            candles.append(Candle(int(row["open_time"]), float(row["open"]),
                                  float(row["high"]), float(row["low"]),
                                  float(row["close"]), float(row["volume"])))
    return candles
