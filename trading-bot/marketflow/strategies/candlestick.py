"""Candlestick patterns with trend context: engulfing, hammer/shooting star,
morning/evening star. Patterns only count at sensible locations (e.g. a
hammer after a decline)."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class Candlestick(Strategy):
    name = "candlestick"
    description = "Engulfing, pin bars and star patterns in context"

    def evaluate(self, ctx: Context, i: int) -> Signal:
        if i < 5:
            return NEUTRAL
        c, p = ctx.candles[i], ctx.candles[i - 1]
        declined = ctx.closes[i - 1] < ctx.closes[i - 4]
        advanced = ctx.closes[i - 1] > ctx.closes[i - 4]

        # bullish/bearish engulfing
        if (c.bullish and not p.bullish and c.close > p.open and c.open < p.close
                and c.body > p.body and declined):
            return Signal(0.6, "bullish engulfing after decline")
        if (not c.bullish and p.bullish and c.close < p.open and c.open > p.close
                and c.body > p.body and advanced):
            return Signal(-0.6, "bearish engulfing after advance")

        # hammer / shooting star (pin bars)
        if c.range > 0:
            if (c.lower_wick > 2 * c.body and c.upper_wick < c.body and declined):
                return Signal(0.5, "hammer (long lower wick) after decline")
            if (c.upper_wick > 2 * c.body and c.lower_wick < c.body and advanced):
                return Signal(-0.5, "shooting star (long upper wick) after advance")

        # morning / evening star (3-candle)
        a = ctx.candles[i - 2]
        small_middle = p.body < a.body * 0.5
        if (not a.bullish and small_middle and c.bullish
                and c.close > (a.open + a.close) / 2 and declined):
            return Signal(0.55, "morning star reversal")
        if (a.bullish and small_middle and not c.bullish
                and c.close < (a.open + a.close) / 2 and advanced):
            return Signal(-0.55, "evening star reversal")

        return NEUTRAL
