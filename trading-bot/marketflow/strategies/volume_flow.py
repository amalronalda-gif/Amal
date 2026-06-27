"""Volume flow: OBV trend confirmation and price/OBV divergence
(Wyckoff-style effort-vs-result reading)."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL
from ..indicators import linreg_slope


class VolumeFlow(Strategy):
    name = "volume_flow"
    description = "OBV slope confirmation and price/OBV divergence"

    WINDOW = 20

    def evaluate(self, ctx: Context, i: int) -> Signal:
        if i < self.WINDOW + 1:
            return NEUTRAL
        price_win = ctx.closes[i - self.WINDOW + 1:i + 1]
        obv_win = ctx.obv[i - self.WINDOW + 1:i + 1]
        p_slope = linreg_slope(price_win)
        # OBV can cross zero, normalize by its range instead of mean
        obv_range = max(obv_win) - min(obv_win)
        if obv_range == 0:
            return NEUTRAL
        scaled = [(v - min(obv_win)) / obv_range for v in obv_win]
        o_slope = self._raw_slope(scaled)

        p_up, p_dn = p_slope > 1e-5, p_slope < -1e-5
        o_up, o_dn = o_slope > 0.01, o_slope < -0.01

        if p_up and o_up:
            return Signal(0.5, "rising price confirmed by rising OBV")
        if p_dn and o_dn:
            return Signal(-0.5, "falling price confirmed by falling OBV")
        if p_dn and o_up:
            return Signal(0.45, "bullish divergence: price down, OBV up (accumulation)")
        if p_up and o_dn:
            return Signal(-0.45, "bearish divergence: price up, OBV down (distribution)")
        return NEUTRAL

    @staticmethod
    def _raw_slope(values: list[float]) -> float:
        n = len(values)
        mean_x = (n - 1) / 2.0
        mean_y = sum(values) / n
        num = sum((j - mean_x) * (v - mean_y) for j, v in enumerate(values))
        den = sum((j - mean_x) ** 2 for j in range(n))
        return num / den * n if den else 0.0
