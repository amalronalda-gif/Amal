"""Trend following: EMA 20/50/200 alignment plus slope (Dow/MA-stack)."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL
from ..indicators import linreg_slope


class TrendFollowing(Strategy):
    name = "trend_following"
    description = "EMA 20/50/200 stack alignment and slope"

    def evaluate(self, ctx: Context, i: int) -> Signal:
        e20, e50, e200 = ctx.ema20[i], ctx.ema50[i], ctx.ema200[i]
        if e20 is None or e50 is None or e200 is None:
            return NEUTRAL
        price = ctx.closes[i]
        score = 0.0
        parts = []
        if e20 > e50 > e200:
            score += 0.5
            parts.append("bullish EMA stack 20>50>200")
        elif e20 < e50 < e200:
            score -= 0.5
            parts.append("bearish EMA stack 20<50<200")
        if price > e200:
            score += 0.15
        else:
            score -= 0.15
        # slope of EMA50 over the last 20 bars (per-bar, normalized)
        window = [v for v in ctx.ema50[i - 19:i + 1] if v is not None]
        slope = linreg_slope(window) if len(window) == 20 else 0.0
        score += max(-0.35, min(0.35, slope * 700))
        if abs(score) < 0.15:
            return NEUTRAL
        parts.append(f"price {'above' if price > e200 else 'below'} EMA200")
        return Signal(score, ", ".join(parts))
