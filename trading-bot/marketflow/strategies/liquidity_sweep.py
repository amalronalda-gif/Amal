"""Liquidity sweep / stop hunt reversal (smart money concept).

Price wicks through a recent swing low (where sell stops cluster) and closes
back above it -> bullish reversal. Mirror image for swing highs -> bearish.
Equal lows/highs (double bottoms/tops) hold more liquidity and score higher.
"""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class LiquiditySweep(Strategy):
    name = "liquidity_sweep"
    description = "Stop-hunt wicks through swing levels that snap back (SMC)"

    LOOKBACK_SWINGS = 8     # how many recent swing levels to consider
    RECENT_BARS = 3         # sweep must have happened within the last N bars
    EQUAL_TOL = 0.0015      # levels within 0.15% count as "equal" (more liquidity)

    def evaluate(self, ctx: Context, i: int) -> Signal:
        a = ctx.atr14[i]
        if a is None or a <= 0:
            return NEUTRAL
        swing_highs, swing_lows = ctx.confirmed_swings(i)
        bull = self._sweep_score(ctx, i, swing_lows, a, bullish=True)
        bear = self._sweep_score(ctx, i, swing_highs, a, bullish=False)
        if bull == bear:
            return NEUTRAL
        if bull > bear:
            return Signal(bull, "swept sell-side liquidity below swing low(s), closed back above")
        return Signal(-bear, "swept buy-side liquidity above swing high(s), closed back below")

    def _sweep_score(self, ctx: Context, i: int, swings: list[int],
                     atr_val: float, bullish: bool) -> float:
        levels = []
        for s in swings[-self.LOOKBACK_SWINGS:]:
            levels.append(ctx.candles[s].low if bullish else ctx.candles[s].high)
        best = 0.0
        for level in levels:
            equal_count = sum(1 for l in levels
                              if abs(l - level) / level < self.EQUAL_TOL)
            for j in range(max(0, i - self.RECENT_BARS + 1), i + 1):
                c = ctx.candles[j]
                if bullish:
                    swept = c.low < level and c.close > level
                    wick = c.lower_wick
                else:
                    swept = c.high > level and c.close < level
                    wick = c.upper_wick
                if not swept:
                    continue
                # deeper wick + rejection close = stronger sweep
                depth = (level - c.low) if bullish else (c.high - level)
                strength = min(depth / atr_val, 1.0) * 0.5 + 0.3
                if wick > c.body:  # classic pin-bar rejection
                    strength += 0.15
                if equal_count >= 2:  # equal lows/highs = pooled liquidity
                    strength += 0.15
                # decay if the sweep wasn't on the current bar
                strength *= 1.0 - 0.2 * (i - j)
                best = max(best, strength)
        return min(best, 1.0)
