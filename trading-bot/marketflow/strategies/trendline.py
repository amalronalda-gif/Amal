"""Diagonal trendlines through the last two swing highs/lows: a break of a
descending line is bullish (and vice versa), a rejection at the line is a
continuation signal."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class Trendline(Strategy):
    name = "trendline"
    description = "Breaks and rejections of swing-point trendlines"

    def evaluate(self, ctx: Context, i: int) -> Signal:
        a = ctx.atr14[i]
        if not a:
            return NEUTRAL
        swing_highs, swing_lows = ctx.confirmed_swings(i)
        c = ctx.candles
        price = ctx.closes[i]
        best = NEUTRAL

        if len(swing_highs) >= 2:
            x1, x2 = swing_highs[-2], swing_highs[-1]
            y1, y2 = c[x1].high, c[x2].high
            if y2 < y1 and i - x2 <= 40:  # descending resistance line
                line = y2 + (y2 - y1) / (x2 - x1) * (i - x2)
                recently_below = any(
                    ctx.closes[j] <= y2 + (y2 - y1) / (x2 - x1) * (j - x2)
                    for j in range(max(0, i - 3), i))
                if price > line + 0.1 * a and recently_below:
                    best = Signal(0.6, "broke descending trendline")
                elif (c[i].high >= line - 0.2 * a and price < line
                      and c[i].upper_wick > c[i].body * 0.8):
                    best = Signal(-0.45, "rejected at descending trendline")

        if len(swing_lows) >= 2:
            x1, x2 = swing_lows[-2], swing_lows[-1]
            y1, y2 = c[x1].low, c[x2].low
            if y2 > y1 and i - x2 <= 40:  # ascending support line
                line = y2 + (y2 - y1) / (x2 - x1) * (i - x2)
                recently_above = any(
                    ctx.closes[j] >= y2 + (y2 - y1) / (x2 - x1) * (j - x2)
                    for j in range(max(0, i - 3), i))
                if price < line - 0.1 * a and recently_above:
                    sig = Signal(-0.6, "broke ascending trendline")
                elif (c[i].low <= line + 0.2 * a and price > line
                      and c[i].lower_wick > c[i].body * 0.8):
                    sig = Signal(0.45, "rejected at ascending trendline")
                else:
                    sig = NEUTRAL
                if abs(sig.score) > abs(best.score):
                    best = sig
        return best
