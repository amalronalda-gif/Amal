"""Breakout: Donchian channel (20-bar) breakout with volume confirmation
(classic turtle/Donchian + volume filter)."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class Breakout(Strategy):
    name = "breakout"
    description = "20-bar Donchian channel breakout confirmed by volume"

    def evaluate(self, ctx: Context, i: int) -> Signal:
        hi, lo = ctx.donchian_hi[i], ctx.donchian_lo[i]
        a = ctx.atr14[i]
        if hi is None or lo is None or a is None or a <= 0 or i < 20:
            return NEUTRAL
        c = ctx.candles[i]
        avg_vol = sum(x.volume for x in ctx.candles[i - 20:i]) / 20
        vol_boost = 0.0
        if avg_vol > 0 and c.volume > 1.5 * avg_vol:
            vol_boost = 0.2
        if c.close > hi:
            depth = min((c.close - hi) / a, 1.0)
            return Signal(0.4 + 0.3 * depth + vol_boost,
                          "close above 20-bar high"
                          + (" on elevated volume" if vol_boost else ""))
        if c.close < lo:
            depth = min((lo - c.close) / a, 1.0)
            return Signal(-(0.4 + 0.3 * depth + vol_boost),
                          "close below 20-bar low"
                          + (" on elevated volume" if vol_boost else ""))
        return NEUTRAL
