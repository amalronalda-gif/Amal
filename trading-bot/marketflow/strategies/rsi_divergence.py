"""RSI divergence at confirmed swing points: price makes a lower low while
RSI makes a higher low (bullish), or a higher high with a lower RSI high
(bearish). One of the most reliable classic reversal signals."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class RsiDivergence(Strategy):
    name = "rsi_divergence"
    description = "Price/RSI divergence at swing points"

    MAX_AGE = 10        # the newer swing must be recent (bars before i)
    MIN_RSI_GAP = 3.0   # required RSI difference between the two swings

    def evaluate(self, ctx: Context, i: int) -> Signal:
        swing_highs, swing_lows = ctx.confirmed_swings(i)
        r = ctx.rsi14

        if len(swing_lows) >= 2:
            l2, l1 = swing_lows[-2], swing_lows[-1]
            if (i - l1 <= self.MAX_AGE and r[l1] is not None and r[l2] is not None
                    and ctx.candles[l1].low < ctx.candles[l2].low
                    and r[l1] > r[l2] + self.MIN_RSI_GAP):
                strength = min((r[l1] - r[l2]) / 15.0, 1.0)
                return Signal(0.45 + 0.25 * strength,
                              "bullish RSI divergence: lower low in price, "
                              "higher low in RSI")

        if len(swing_highs) >= 2:
            h2, h1 = swing_highs[-2], swing_highs[-1]
            if (i - h1 <= self.MAX_AGE and r[h1] is not None and r[h2] is not None
                    and ctx.candles[h1].high > ctx.candles[h2].high
                    and r[h1] < r[h2] - self.MIN_RSI_GAP):
                strength = min((r[h2] - r[h1]) / 15.0, 1.0)
                return Signal(-(0.45 + 0.25 * strength),
                              "bearish RSI divergence: higher high in price, "
                              "lower high in RSI")
        return NEUTRAL
