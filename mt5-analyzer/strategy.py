"""Strategy: H4 EMA(50) trend filter + H1 pullback-to-EMA(21) entries with
an RSI(14) 40-50 zone exit and candle confirmation. Analysis only.

Long setup (short is the mirror image):
  1. H4: last closed bar's close above EMA(50)        -> longs only
  2. H1: price pulled back to EMA(21) within the last `pullback_lookback`
     bars (bar low touched/crossed the EMA)
  3. RSI(14) on H1 exits the 40-50 zone upward: previous bar's RSI inside
     [40, 50], current bar's RSI above 50
  4. Confirmation: the signal bar is bullish and closes above EMA(21)
  SL = 1.5 * ATR(14), TP = 2 * SL (RR 1:2)

Session filter: signals only 10:00-20:00 UTC+5; news filter: no signals
within +-30 minutes of calendar events; at most 2 signals per (UTC+5) day.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from data import Bar, tf_seconds


# ---------------------------------------------------------------------------
# indicators (pure python, aligned lists with None during warm-up)
# ---------------------------------------------------------------------------

def ema(values: list[float], period: int) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    if len(values) < period:
        return out
    k = 2.0 / (period + 1)
    prev = sum(values[:period]) / period
    out[period - 1] = prev
    for i in range(period, len(values)):
        prev = values[i] * k + prev * (1 - k)
        out[i] = prev
    return out


def rsi(values: list[float], period: int = 14) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    if len(values) <= period:
        return out
    gains = losses = 0.0
    for i in range(1, period + 1):
        d = values[i] - values[i - 1]
        gains += max(d, 0.0)
        losses += max(-d, 0.0)
    ag, al = gains / period, losses / period
    out[period] = 100.0 if al == 0 else 100 - 100 / (1 + ag / al)
    for i in range(period + 1, len(values)):
        d = values[i] - values[i - 1]
        ag = (ag * (period - 1) + max(d, 0.0)) / period
        al = (al * (period - 1) + max(-d, 0.0)) / period
        out[i] = 100.0 if al == 0 else 100 - 100 / (1 + ag / al)
    return out


def atr(bars: list[Bar], period: int = 14) -> list[float | None]:
    out: list[float | None] = [None] * len(bars)
    if len(bars) <= period:
        return out
    trs = [bars[0].high - bars[0].low]
    for i in range(1, len(bars)):
        c, p = bars[i], bars[i - 1]
        trs.append(max(c.high - c.low, abs(c.high - p.close),
                       abs(c.low - p.close)))
    prev = sum(trs[1:period + 1]) / period
    out[period] = prev
    for i in range(period + 1, len(bars)):
        prev = (prev * (period - 1) + trs[i]) / period
        out[i] = prev
    return out


# ---------------------------------------------------------------------------
# filters
# ---------------------------------------------------------------------------

def local_dt(ts: int, cfg: dict) -> datetime:
    return (datetime.fromtimestamp(ts, tz=timezone.utc)
            + timedelta(hours=cfg["tz_offset_hours"]))


def in_trading_hours(ts: int, cfg: dict) -> bool:
    h = local_dt(ts, cfg).hour
    return cfg["trade_hour_start"] <= h < cfg["trade_hour_end"]


def parse_news(cfg: dict) -> list[tuple[int, str]]:
    events = []
    for when, label in cfg.get("news_events_utc", []):
        ts = int(datetime.strptime(when, "%Y-%m-%d %H:%M")
                 .replace(tzinfo=timezone.utc).timestamp())
        events.append((ts, label))
    events.sort()
    return events


def near_news(ts: int, events: list[tuple[int, str]], cfg: dict) -> str | None:
    """Returns the event label if `ts` is within the blackout window."""
    window = cfg["news_window_minutes"] * 60
    times = [e[0] for e in events]
    idx = bisect.bisect_left(times, ts)
    for j in (idx - 1, idx):
        if 0 <= j < len(events) and abs(events[j][0] - ts) <= window:
            return events[j][1]
    return None


# ---------------------------------------------------------------------------
# signal
# ---------------------------------------------------------------------------

@dataclass
class TradeSignal:
    time: int            # epoch seconds UTC of the signal (H1 bar close)
    side: str            # "LONG" / "SHORT"
    entry: float
    sl: float
    tp: float
    rsi_prev: float
    rsi_now: float
    h4_trend: str
    reason: str


class SignalContext:
    """Precomputed indicator series so the backtester is O(n)."""

    def __init__(self, h1: list[Bar], h4: list[Bar], cfg: dict):
        self.h1, self.h4, self.cfg = h1, h4, cfg
        h1_closes = [b.close for b in h1]
        self.ema_pb = ema(h1_closes, cfg["ema_pullback_period"])
        self.rsi = rsi(h1_closes, cfg["rsi_period"])
        self.atr = atr(h1, cfg["atr_period"])
        self.ema_h4 = ema([b.close for b in h4], cfg["ema_trend_period"])
        self.h4_starts = [b.time for b in h4]
        self.news = parse_news(cfg)

    def h4_index_for(self, h1_time: int) -> int:
        """Index of the last H4 bar fully closed at h1_time (no lookahead)."""
        return bisect.bisect_right(self.h4_starts,
                                   h1_time - tf_seconds("H4")) - 1

    def trend_at(self, h1_time: int) -> str | None:
        j = self.h4_index_for(h1_time)
        if j < 0 or self.ema_h4[j] is None:
            return None
        return "UP" if self.h4[j].close > self.ema_h4[j] else "DOWN"


def check_entry(ctx: SignalContext, i: int) -> TradeSignal | None:
    """Evaluate the H1 bar at index i (a CLOSED bar) for a signal.

    The signal timestamp is the bar's close time; session/news filters are
    applied to that moment (= when a trader could actually act).
    """
    cfg = ctx.cfg
    bar = ctx.h1[i]
    signal_ts = bar.time + tf_seconds("H1")

    if not in_trading_hours(signal_ts, cfg):
        return None
    if near_news(signal_ts, ctx.news, cfg):
        return None
    e = ctx.ema_pb[i]
    a = ctx.atr[i]
    r_now = ctx.rsi[i]
    r_prev = ctx.rsi[i - 1] if i > 0 else None
    if None in (e, a, r_now, r_prev) or a <= 0:
        return None
    trend = ctx.trend_at(bar.time)
    if trend is None:
        return None

    lo_z, hi_z = cfg["rsi_zone_low"], cfg["rsi_zone_high"]
    lb = cfg["pullback_lookback"]

    if trend == "UP":
        pulled_back = any(ctx.h1[j].low <= ctx.ema_pb[j]
                          for j in range(max(0, i - lb + 1), i + 1)
                          if ctx.ema_pb[j] is not None)
        rsi_exit_up = lo_z <= r_prev <= hi_z and r_now > hi_z
        confirmed = bar.bullish and bar.close > e
        if pulled_back and rsi_exit_up and confirmed:
            sl_dist = cfg["sl_atr_mult"] * a
            return TradeSignal(
                signal_ts, "LONG", bar.close,
                bar.close - sl_dist, bar.close + cfg["rr"] * sl_dist,
                r_prev, r_now, trend,
                f"H4 uptrend, pullback to EMA{cfg['ema_pullback_period']}, "
                f"RSI {r_prev:.0f}->{r_now:.0f} out of zone, bullish close")
    else:
        mirror_lo, mirror_hi = 100 - hi_z, 100 - lo_z  # 50-60 by default
        pulled_back = any(ctx.h1[j].high >= ctx.ema_pb[j]
                          for j in range(max(0, i - lb + 1), i + 1)
                          if ctx.ema_pb[j] is not None)
        rsi_exit_down = mirror_lo <= r_prev <= mirror_hi and r_now < mirror_lo
        confirmed = (not bar.bullish) and bar.close < e
        if pulled_back and rsi_exit_down and confirmed:
            sl_dist = cfg["sl_atr_mult"] * a
            return TradeSignal(
                signal_ts, "SHORT", bar.close,
                bar.close + sl_dist, bar.close - cfg["rr"] * sl_dist,
                r_prev, r_now, trend,
                f"H4 downtrend, pullback to EMA{cfg['ema_pullback_period']}, "
                f"RSI {r_prev:.0f}->{r_now:.0f} out of zone, bearish close")
    return None
