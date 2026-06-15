"""Strategy framework: each strategy scores the market at a bar index.

Score convention: float in [-1.0, +1.0].
  +1.0 = strongly bullish, -1.0 = strongly bearish, 0.0 = no opinion.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..data import Candle
from .. import indicators as ta


@dataclass
class Signal:
    score: float
    reason: str

    def __post_init__(self):
        self.score = max(-1.0, min(1.0, self.score))


NEUTRAL = Signal(0.0, "no setup")


class Context:
    """Precomputed indicator series shared by all strategies.

    Everything here is computed only from data up to each index (no
    look-ahead), so the backtester can safely evaluate at any bar i.
    """

    MIN_BARS = 220  # enough warm-up for the slowest indicator (EMA200)

    def __init__(self, candles: list[Candle]):
        self.candles = candles
        closes = [c.close for c in candles]
        self.closes = closes
        self.ema20 = ta.ema(closes, 20)
        self.ema50 = ta.ema(closes, 50)
        self.ema200 = ta.ema(closes, 200)
        self.rsi14 = ta.rsi(closes, 14)
        self.macd_line, self.macd_signal, self.macd_hist = ta.macd(closes)
        self.atr14 = ta.atr(candles, 14)
        self.bb_upper, self.bb_mid, self.bb_lower = ta.bollinger(closes, 20, 2.0)
        self.stoch_k, self.stoch_d = ta.stochastic(candles)
        self.obv = ta.obv(candles)
        self.donchian_hi, self.donchian_lo = ta.donchian(candles, 20)
        self.adx14 = ta.adx(candles, 14)
        self.ichimoku = ta.ichimoku(candles)
        # swing points are confirmed `strength` bars late; strategies must
        # only use swings with index <= i - strength to avoid look-ahead
        self.swing_strength = 3
        self.swing_highs, self.swing_lows = ta.swing_points(candles, self.swing_strength)
        # rolling 96-bar VWAP from cumulative sums (O(1) per bar)
        self.vwap = self._rolling_vwap(candles, 96)
        # candle spacing in ms (None for a single candle); lets time-of-day
        # strategies know the timeframe
        self.step_ms = (candles[1].open_time - candles[0].open_time
                        if len(candles) > 1 else None)

    @staticmethod
    def _rolling_vwap(candles: list[Candle], window: int) -> list[float | None]:
        cum_pv = [0.0]
        cum_v = [0.0]
        for c in candles:
            typical = (c.high + c.low + c.close) / 3.0
            cum_pv.append(cum_pv[-1] + typical * c.volume)
            cum_v.append(cum_v[-1] + c.volume)
        out: list[float | None] = [None] * len(candles)
        for i in range(window - 1, len(candles)):
            vol = cum_v[i + 1] - cum_v[i + 1 - window]
            if vol > 0:
                out[i] = (cum_pv[i + 1] - cum_pv[i + 1 - window]) / vol
        return out

    def confirmed_swings(self, i: int) -> tuple[list[int], list[int]]:
        """Swing highs/lows already confirmed as of bar i."""
        cutoff = i - self.swing_strength
        return ([s for s in self.swing_highs if s <= cutoff],
                [s for s in self.swing_lows if s <= cutoff])


class Strategy:
    name = "base"
    description = ""

    def evaluate(self, ctx: Context, i: int) -> Signal:
        raise NotImplementedError
