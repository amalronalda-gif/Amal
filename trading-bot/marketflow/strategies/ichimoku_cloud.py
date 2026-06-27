"""Ichimoku Kinko Hyo: price vs cloud, tenkan/kijun cross."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class IchimokuCloud(Strategy):
    name = "ichimoku"
    description = "Price vs Kumo cloud and Tenkan/Kijun cross"

    DISPLACEMENT = 26

    def evaluate(self, ctx: Context, i: int) -> Signal:
        ich = ctx.ichimoku
        j = i - self.DISPLACEMENT  # cloud at bar i was computed 26 bars ago
        if j < 0:
            return NEUTRAL
        tenkan, kijun = ich["tenkan"][i], ich["kijun"][i]
        sa, sb = ich["senkou_a"][j], ich["senkou_b"][j]
        if tenkan is None or kijun is None or sa is None or sb is None:
            return NEUTRAL
        price = ctx.closes[i]
        cloud_top, cloud_bot = max(sa, sb), min(sa, sb)
        score = 0.0
        parts = []
        if price > cloud_top:
            score += 0.4
            parts.append("price above Kumo cloud")
        elif price < cloud_bot:
            score -= 0.4
            parts.append("price below Kumo cloud")
        else:
            parts.append("price inside cloud (indecision)")
        if tenkan > kijun:
            score += 0.3
            parts.append("Tenkan above Kijun")
        elif tenkan < kijun:
            score -= 0.3
            parts.append("Tenkan below Kijun")
        if sa > sb:
            score += 0.1  # bullish (green) cloud
        elif sa < sb:
            score -= 0.1
        if abs(score) < 0.2:
            return NEUTRAL
        return Signal(score, ", ".join(parts))
