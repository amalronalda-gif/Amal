"""Head and shoulders / inverse head and shoulders with neckline break —
the textbook trend-ending pattern: three swing highs where the middle (head)
is the highest, shoulders roughly equal, then a close below the neckline."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class HeadShoulders(Strategy):
    name = "head_shoulders"
    description = "Head & shoulders (and inverse) neckline breaks"

    SHOULDER_TOL = 0.005  # shoulders within 0.5% of each other
    HEAD_MIN = 0.0015     # head must exceed shoulders by at least 0.15%
    MAX_AGE = 30          # right shoulder must be recent
    FRESH = 5             # neckline break within the last N bars

    def evaluate(self, ctx: Context, i: int) -> Signal:
        swing_highs, swing_lows = ctx.confirmed_swings(i)
        c = ctx.candles
        price = ctx.closes[i]

        if len(swing_highs) >= 3:
            s1, head, s2 = swing_highs[-3], swing_highs[-2], swing_highs[-1]
            hs1, hh, hs2 = c[s1].high, c[head].high, c[s2].high
            if (i - s2 <= self.MAX_AGE
                    and hh > hs1 * (1 + self.HEAD_MIN)
                    and hh > hs2 * (1 + self.HEAD_MIN)
                    and abs(hs1 - hs2) / hs1 < self.SHOULDER_TOL):
                neck = min(x.low for x in c[s1:s2 + 1])
                was_above = any(ctx.closes[j] >= neck
                                for j in range(max(0, i - self.FRESH), i))
                if price < neck and was_above:
                    return Signal(-0.7, f"head and shoulders broke neckline ({neck:.2f})")

        if len(swing_lows) >= 3:
            s1, head, s2 = swing_lows[-3], swing_lows[-2], swing_lows[-1]
            ls1, lh, ls2 = c[s1].low, c[head].low, c[s2].low
            if (i - s2 <= self.MAX_AGE
                    and lh < ls1 * (1 - self.HEAD_MIN)
                    and lh < ls2 * (1 - self.HEAD_MIN)
                    and abs(ls1 - ls2) / ls1 < self.SHOULDER_TOL):
                neck = max(x.high for x in c[s1:s2 + 1])
                was_below = any(ctx.closes[j] <= neck
                                for j in range(max(0, i - self.FRESH), i))
                if price > neck and was_below:
                    return Signal(0.7, f"inverse head and shoulders broke neckline ({neck:.2f})")
        return NEUTRAL
