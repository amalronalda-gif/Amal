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
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

BINANCE_DATA_URL = "https://data-api.binance.vision/api/v3/klines"
DEFAULT_SYMBOL = "XAUUSD"  # display name; resolves to PAXGUSDT for data

# Binance spot has no literal XAUUSD market; PAXG (1 token = 1 troy oz of
# gold) is the tradable gold/USDT pair, so map common gold tickers to it.
SYMBOL_ALIASES = {
    "XAUUSD": "PAXGUSDT",
    "XAUUSDT": "PAXGUSDT",
    "GOLD": "PAXGUSDT",
    "PAXG": "PAXGUSDT",
    "XAUT": "XAUTUSDT",  # Tether Gold, the other on-exchange gold token
    "BTCUSD": "BTCUSDT",
    "BTC": "BTCUSDT",
    "BITCOIN": "BTCUSDT",
    "EURUSD": "EURUSDT",
    "EUR": "EURUSDT",
}

# the only markets this bot serves (resolved Binance symbols)
SUPPORTED_MARKETS = {"PAXGUSDT", "XAUTUSDT", "BTCUSDT", "EURUSDT"}

# what users see instead of internal Binance tickers
DISPLAY_NAMES = {"PAXGUSDT": "XAUUSD", "XAUTUSDT": "XAUUSD",
                 "BTCUSDT": "BTCUSD", "EURUSDT": "EURUSD"}


def display_symbol(symbol: str) -> str:
    """Trader-facing name for any alias (PAXG/GOLD/XAUUSDT -> XAUUSD)."""
    resolved = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
    return DISPLAY_NAMES.get(resolved, resolved)

# resolved symbol -> (TradingView symbol for the live anchor quote, label).
# Gold is anchored to COMEX front-month futures (GC1!) — what most brokers
# and TradingView show for "gold" — which trades a few $ above spot (carry).
# BTC needs no extra quote: its Binance candles ARE the live market.
SPOT_QUOTES = {
    "PAXGUSDT": ("COMEX:GC1!", "XAU/USD fut (GC)"),
    "XAUTUSDT": ("COMEX:GC1!", "XAU/USD fut (GC)"),
    "EURUSDT": ("OANDA:EURUSD", "EUR/USD"),
}

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
    symbol = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
    candles: list[Candle] = []
    end_time: int | None = None
    remaining = limit
    while remaining > 0:
        page = min(remaining, 1000)
        url = f"{BINANCE_DATA_URL}?symbol={symbol}&interval={interval}&limit={page}"
        if end_time is not None:
            url += f"&endTime={end_time}"
        try:
            rows = _http_get_json(url, retries=retries)
        except urllib.error.HTTPError as e:
            if e.code == 400:
                raise ValueError(
                    f"unknown symbol {symbol!r} on Binance — for gold use "
                    f"PAXGUSDT (or alias XAUUSD/GOLD)") from None
            raise
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


def _http_get_json(url: str, retries: int = 3, headers: dict | None = None):
    delay = 2.0
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url, headers=headers or {"User-Agent": "marketflow/1.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if 400 <= e.code < 500:
                raise  # client error, retrying won't help
            if attempt == retries:
                raise
        except Exception:
            if attempt == retries:
                raise
            time.sleep(delay)
            delay *= 2


TRADINGVIEW_QUOTE_URL = ("https://scanner.tradingview.com/symbol"
                         "?symbol={sym}&fields=close,bid,ask,change,high,low")

# Binance symbols that represent gold, for which a live spot XAU/USD quote
# from TradingView (OANDA feed) is a meaningful add-on.
GOLD_SYMBOLS = {"PAXGUSDT", "XAUTUSDT"}


def fx_market_open(dt: "datetime | None" = None) -> bool:
    """Approximate spot metals/FX schedule (UTC): opens Sunday 22:00, closes
    Friday 21:00, with a daily maintenance break 21:00-22:00 UTC."""
    from datetime import datetime, timezone
    now = dt or datetime.now(timezone.utc)
    wd = now.weekday()
    if wd == 5:                      # Saturday
        return False
    if wd == 6:                      # Sunday: opens 22:00 UTC
        return now.hour >= 22
    if wd == 4:                      # Friday: closes 21:00 UTC
        return now.hour < 21
    return not 21 <= now.hour < 22   # Mon-Thu daily break


def fetch_tradingview_quote(tv_symbol: str = "OANDA:XAUUSD") -> dict | None:
    """Live quote from TradingView's public scanner endpoint.

    Returns e.g. {'close': 4100.5, 'bid': ..., 'ask': ..., 'change': ...,
    'high': ..., 'low': ...} or None on failure. Quote only — TradingView
    has no public endpoint for candle history.
    """
    url = TRADINGVIEW_QUOTE_URL.format(sym=urllib.parse.quote(tv_symbol))
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0 Safari/537.36"),
        "Accept": "application/json",
        "Referer": "https://www.tradingview.com/",
    }
    for attempt in range(3):  # endpoint throttles intermittently with 503s
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                quote = json.loads(resp.read().decode())
            if isinstance(quote, dict) and "close" in quote:
                return quote
            return None
        except Exception:
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
    return None


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
