"""ICT Optimal Trade Entry: after an impulse leg, the 62-79% Fibonacci
retracement of that leg is the institutional entry zone in the impulse's
direction."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class IctOte(Strategy):
    name = "ict_ote"
    description = "62-79% retracement (OTE) of the latest impulse leg"

    MAX_AGE = 20  # the impulse extreme must be recent

    def evaluate(self, ctx: Context, i: int) -> Signal:
        swing_highs, swing_lows = ctx.confirmed_swings(i)
        if not swing_highs or not swing_lows:
            return NEUTRAL
        c = ctx.candles
        price = ctx.closes[i]
        h, l = swing_highs[-1], swing_lows[-1]

        if l < h and i - h <= self.MAX_AGE:  # bullish leg: low -> high
            lo, hi = c[l].low, c[h].high
            leg = hi - lo
            if leg > 0:
                zone_hi = hi - 0.62 * leg
                zone_lo = hi - 0.79 * leg
                if zone_lo <= price <= zone_hi and price > lo:
                    return Signal(0.55, "price in OTE zone (62-79% retracement) "
                                        "of bullish impulse")
        if h < l and i - l <= self.MAX_AGE:  # bearish leg: high -> low
            hi, lo = c[h].high, c[l].low
            leg = hi - lo
            if leg > 0:
                zone_lo = lo + 0.62 * leg
                zone_hi = lo + 0.79 * leg
                if zone_lo <= price <= zone_hi and price < hi:
                    return Signal(-0.55, "price in OTE zone (62-79% retracement) "
                                         "of bearish impulse")
        return NEUTRAL
