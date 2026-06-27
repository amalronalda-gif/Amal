"""Accumulation → Manipulation → Distribution (AMD / Wyckoff / ICT Power of
Three).

Smart money builds a position inside a tight range (accumulation), then
pushes price beyond one edge to trigger stops and trap breakout traders
(manipulation), before driving the real move the opposite way
(distribution). We detect:

  1. Accumulation: a consolidation window whose total range is small
     relative to ATR (price coiled, no clear direction).
  2. Manipulation: a recent bar sweeps beyond the range edge (wick past it)
     but CLOSES back inside — the false breakout.
  3. Signal: trade away from the swept edge (distribution direction). A
     sweep of the range LOW => bullish; a sweep of the range HIGH => bearish.
"""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class AmdPhase(Strategy):
    name = "amd_phase"
    description = "Accumulation range, manipulation sweep, distribution move"

    RANGE_BARS = 20        # accumulation window length
    MAX_RANGE_ATR = 3.0    # range height must be <= this many ATR (tight)
    RECENT = 3             # manipulation sweep within the last N bars
    EDGE_FRAC = 0.15       # sweep must clear the edge by >=15% of range height

    def evaluate(self, ctx: Context, i: int) -> Signal:
        a = ctx.atr14[i]
        if a is None or a <= 0 or i < self.RANGE_BARS + self.RECENT:
            return NEUTRAL
        c = ctx.candles

        # accumulation window ends just before the recent (manipulation) bars
        win_end = i - self.RECENT
        win = c[win_end - self.RANGE_BARS + 1:win_end + 1]
        if len(win) < self.RANGE_BARS:
            return NEUTRAL
        hi = max(x.high for x in win)
        lo = min(x.low for x in win)
        height = hi - lo
        if height <= 0 or height > self.MAX_RANGE_ATR * a:
            return NEUTRAL  # not a tight accumulation
        margin = height * self.EDGE_FRAC
        price = ctx.closes[i]

        best = NEUTRAL
        for j in range(i - self.RECENT + 1, i + 1):
            bar = c[j]
            # bullish AMD: swept below the range low, closed back inside
            if bar.low < lo - margin and bar.close > lo and price > lo:
                depth = min((lo - bar.low) / a, 1.0)
                score = 0.45 + 0.2 * depth - 0.1 * (i - j)
                if score > best.score:
                    best = Signal(score, f"AMD: swept accumulation low "
                                         f"({lo:.2f}), distribution up expected")
            # bearish AMD: swept above the range high, closed back inside
            if bar.high > hi + margin and bar.close < hi and price < hi:
                depth = min((bar.high - hi) / a, 1.0)
                score = 0.45 + 0.2 * depth - 0.1 * (i - j)
                if score > best.score:
                    best = Signal(-(score), f"AMD: swept accumulation high "
                                            f"({hi:.2f}), distribution down expected")
        return best
