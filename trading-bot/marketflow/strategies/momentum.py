"""Momentum: MACD line/signal/histogram plus RSI regime."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class Momentum(Strategy):
    name = "momentum"
    description = "MACD cross/histogram expansion confirmed by RSI"

    def evaluate(self, ctx: Context, i: int) -> Signal:
        m, s, h = ctx.macd_line[i], ctx.macd_signal[i], ctx.macd_hist[i]
        r = ctx.rsi14[i]
        if m is None or s is None or h is None or r is None or i < 1:
            return NEUTRAL
        h_prev = ctx.macd_hist[i - 1]
        score = 0.0
        parts = []
        if m > s:
            score += 0.35
            parts.append("MACD above signal")
        else:
            score -= 0.35
            parts.append("MACD below signal")
        if h_prev is not None:
            if h > h_prev:
                score += 0.2
                parts.append("histogram expanding up")
            elif h < h_prev:
                score -= 0.2
                parts.append("histogram expanding down")
        # RSI regime: 50 midline; extremes damp momentum (overbought/oversold)
        if r > 55:
            score += 0.2
        elif r < 45:
            score -= 0.2
        if r > 75 or r < 25:
            score *= 0.6  # stretched, momentum likely exhausting
            parts.append(f"RSI stretched at {r:.0f}")
        else:
            parts.append(f"RSI {r:.0f}")
        if abs(score) < 0.2:
            return NEUTRAL
        return Signal(score, ", ".join(parts))
