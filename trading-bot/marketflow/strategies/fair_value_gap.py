"""Fair value gaps (FVG, smart money concept): a 3-candle imbalance where
candle 1's high < candle 3's low (bullish gap) or candle 1's low > candle 3's
high (bearish gap). Price revisiting an unfilled gap tends to react from it
in the gap's direction."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class FairValueGap(Strategy):
    name = "fair_value_gap"
    description = "Reaction from unfilled 3-candle imbalances (FVG)"

    LOOKBACK = 60
    MIN_GAP_ATR = 0.25  # ignore gaps smaller than a quarter ATR

    def evaluate(self, ctx: Context, i: int) -> Signal:
        a = ctx.atr14[i]
        if a is None or a <= 0 or i < 4:
            return NEUTRAL
        price = ctx.closes[i]
        c = ctx.candles
        best = NEUTRAL
        start = max(2, i - self.LOOKBACK)
        for j in range(start, i):  # gap formed by candles j-2, j-1, j
            lo_gap, hi_gap, bullish = None, None, True
            if c[j - 2].high < c[j].low:  # bullish imbalance
                lo_gap, hi_gap, bullish = c[j - 2].high, c[j].low, True
            elif c[j - 2].low > c[j].high:  # bearish imbalance
                lo_gap, hi_gap, bullish = c[j].high, c[j - 2].low, False
            else:
                continue
            if hi_gap - lo_gap < a * self.MIN_GAP_ATR:
                continue
            # gap is "filled" once a later close passes fully through it
            filled = any(
                (c[k].close < lo_gap) if bullish else (c[k].close > hi_gap)
                for k in range(j + 1, i + 1)
            )
            if filled:
                continue
            if lo_gap <= price <= hi_gap:
                # price is inside an unfilled gap -> expect reaction
                size = min((hi_gap - lo_gap) / a, 2.0)
                score = (0.35 + 0.15 * size) * (1 if bullish else -1)
                kind = "bullish" if bullish else "bearish"
                best = Signal(score, f"price inside unfilled {kind} FVG "
                                     f"({lo_gap:.2f}-{hi_gap:.2f})")
        return best
