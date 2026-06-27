"""Double top / double bottom with a neckline break — one of the oldest and
most-traded reversal patterns. Two roughly equal swing highs, then a close
below the valley between them (the neckline) = bearish; mirrored for
double bottoms."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class DoubleTopBottom(Strategy):
    name = "double_top"
    description = "Double top/bottom neckline breaks"

    EQUAL_TOL = 0.0035   # peaks within 0.35% count as a double
    MAX_AGE = 30         # second peak must be within this many bars
    FRESH = 5            # break must have happened within the last N bars

    def evaluate(self, ctx: Context, i: int) -> Signal:
        swing_highs, swing_lows = ctx.confirmed_swings(i)
        c = ctx.candles
        price = ctx.closes[i]

        if len(swing_highs) >= 2:
            h2, h1 = swing_highs[-2], swing_highs[-1]
            top2, top1 = c[h2].high, c[h1].high
            if (h1 - h2 >= 5 and i - h1 <= self.MAX_AGE
                    and abs(top1 - top2) / top1 < self.EQUAL_TOL):
                neck = min(x.low for x in c[h2:h1 + 1])
                was_above = any(ctx.closes[j] >= neck
                                for j in range(max(0, i - self.FRESH), i))
                if price < neck and was_above:
                    return Signal(-0.65, f"double top broke neckline ({neck:.2f})")

        if len(swing_lows) >= 2:
            l2, l1 = swing_lows[-2], swing_lows[-1]
            bot2, bot1 = c[l2].low, c[l1].low
            if (l1 - l2 >= 5 and i - l1 <= self.MAX_AGE
                    and abs(bot1 - bot2) / bot1 < self.EQUAL_TOL):
                neck = max(x.high for x in c[l2:l1 + 1])
                was_below = any(ctx.closes[j] <= neck
                                for j in range(max(0, i - self.FRESH), i))
                if price > neck and was_below:
                    return Signal(0.65, f"double bottom broke neckline ({neck:.2f})")
        return NEUTRAL
