"""Rolling VWAP (volume-weighted average price): the institutional fair-value
benchmark. Price holding above VWAP confirms buyers in control; an extreme
stretch away from VWAP tends to snap back (mean reversion)."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class VwapFlow(Strategy):
    name = "vwap"
    description = "Bias vs rolling VWAP, fade extreme stretches"

    STRETCH_ATR = 3.0   # |price - vwap| beyond this many ATR = overextended

    def evaluate(self, ctx: Context, i: int) -> Signal:
        v = ctx.vwap[i]
        a = ctx.atr14[i]
        if v is None or a is None or a <= 0:
            return NEUTRAL
        price = ctx.closes[i]
        dist = (price - v) / a
        if dist > self.STRETCH_ATR:
            return Signal(-0.45, "stretched far above VWAP (mean-revert)")
        if dist < -self.STRETCH_ATR:
            return Signal(0.45, "stretched far below VWAP (mean-revert)")
        if dist > 0.3:
            return Signal(min(0.25 + dist * 0.08, 0.45), "price above rolling VWAP")
        if dist < -0.3:
            return Signal(max(-0.25 + dist * 0.08, -0.45), "price below rolling VWAP")
        return NEUTRAL
