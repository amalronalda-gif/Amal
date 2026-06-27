"""Support/resistance: clustered swing levels acting as bounce zones.
Price approaching a level that held multiple times tends to react there."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class SupportResistance(Strategy):
    name = "support_resistance"
    description = "Bounces from multi-touch horizontal levels"

    CLUSTER_TOL = 0.002   # 0.2% price tolerance to group touches
    NEAR_ATR = 0.7        # "near a level" = within 0.7 ATR

    def evaluate(self, ctx: Context, i: int) -> Signal:
        a = ctx.atr14[i]
        if a is None or a <= 0:
            return NEUTRAL
        swing_highs, swing_lows = ctx.confirmed_swings(i)
        price = ctx.closes[i]
        c = ctx.candles[i]

        support = self._nearest_cluster(
            [ctx.candles[s].low for s in swing_lows[-20:]], price, below=True)
        resistance = self._nearest_cluster(
            [ctx.candles[s].high for s in swing_highs[-20:]], price, below=False)

        if support:
            level, touches = support
            if price - level < a * self.NEAR_ATR and touches >= 2:
                # at multi-touch support; rejection wick strengthens the case
                score = 0.35 + 0.1 * min(touches - 2, 3)
                if c.lower_wick > c.body:
                    score += 0.15
                return Signal(score, f"at support {level:.2f} ({touches} touches)")
        if resistance:
            level, touches = resistance
            if level - price < a * self.NEAR_ATR and touches >= 2:
                score = 0.35 + 0.1 * min(touches - 2, 3)
                if c.upper_wick > c.body:
                    score += 0.15
                return Signal(-score, f"at resistance {level:.2f} ({touches} touches)")
        return NEUTRAL

    def _nearest_cluster(self, levels: list[float], price: float,
                         below: bool) -> tuple[float, int] | None:
        candidates = [l for l in levels if (l <= price if below else l >= price)]
        if not candidates:
            return None
        anchor = max(candidates) if below else min(candidates)
        touches = sum(1 for l in levels
                      if abs(l - anchor) / anchor < self.CLUSTER_TOL)
        return anchor, touches
