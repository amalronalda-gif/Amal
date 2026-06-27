"""RCI (Rank Correlation Index, Spearman) reversal: when both the fast and
slow RCI sit at an extreme and the fast one turns, price tends to reverse.
Popular momentum-exhaustion indicator (standard periods 9 and 26)."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


def _rci(closes: list[float]) -> float:
    """Spearman rank correlation of price vs time, scaled to [-100, 100]."""
    n = len(closes)
    order = sorted(range(n), key=lambda k: closes[k])
    price_rank = [0] * n
    for rank, k in enumerate(order, start=1):
        price_rank[k] = rank
    d2 = sum((t + 1 - price_rank[t]) ** 2 for t in range(n))
    return (1 - 6 * d2 / (n * (n * n - 1))) * 100


class RciReverse(Strategy):
    name = "rci"
    description = "RCI(9/26) extremes with the fast line turning (reversal)"

    FAST, SLOW = 9, 26
    EXTREME = 80.0

    def evaluate(self, ctx: Context, i: int) -> Signal:
        if i < self.SLOW + 1:
            return NEUTRAL
        closes = ctx.closes
        fast_now = _rci(closes[i - self.FAST + 1:i + 1])
        fast_prev = _rci(closes[i - self.FAST:i])
        slow_now = _rci(closes[i - self.SLOW + 1:i + 1])

        if fast_now > self.EXTREME and slow_now > self.EXTREME and fast_now < fast_prev:
            depth = min((min(fast_now, slow_now) - self.EXTREME) / 20.0, 1.0)
            return Signal(-(0.45 + 0.2 * depth), "RCI overbought and turning down")
        if fast_now < -self.EXTREME and slow_now < -self.EXTREME and fast_now > fast_prev:
            depth = min((-max(fast_now, slow_now) - self.EXTREME) / 20.0, 1.0)
            return Signal(0.45 + 0.2 * depth, "RCI oversold and turning up")
        return NEUTRAL
