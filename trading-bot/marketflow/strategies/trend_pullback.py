"""Trend pullback: the classic continuation entry. In a downtrend, price
retraces up into the EMA20/50 zone and gets rejected -> short with the trend
("sell the rally"); mirror image for uptrends. This is the canonical
short-entry technique of trend traders."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class TrendPullback(Strategy):
    name = "trend_pullback"
    description = "Rejection of a pullback into the EMA20/50 zone with the trend"

    TOUCH_ATR = 0.2   # how close to EMA20 counts as touching the zone

    def evaluate(self, ctx: Context, i: int) -> Signal:
        e20, e50, e200 = ctx.ema20[i], ctx.ema50[i], ctx.ema200[i]
        a = ctx.atr14[i]
        if None in (e20, e50, e200) or not a:
            return NEUTRAL
        c = ctx.candles[i]
        if e20 < e50 < e200:  # downtrend: short the rally into the zone
            touched = c.high >= e20 - self.TOUCH_ATR * a
            rejected = c.close < e20 and c.upper_wick > c.body * 0.8
            if touched and rejected:
                score = -0.55
                if c.high >= e50:
                    score -= 0.15  # deeper pullback = better entry
                return Signal(score, "pullback into EMA zone rejected in downtrend")
        elif e20 > e50 > e200:  # uptrend: buy the dip into the zone
            touched = c.low <= e20 + self.TOUCH_ATR * a
            rejected = c.close > e20 and c.lower_wick > c.body * 0.8
            if touched and rejected:
                score = 0.55
                if c.low <= e50:
                    score += 0.15
                return Signal(score, "pullback into EMA zone rejected in uptrend")
        return NEUTRAL
