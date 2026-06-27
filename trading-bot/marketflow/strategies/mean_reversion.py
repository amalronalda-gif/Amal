"""Mean reversion: fade closes outside Bollinger bands when RSI/stochastic
confirm an extreme. Counter-trend by design; the engine weights it lower in
strong trends via the ensemble."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class MeanReversion(Strategy):
    name = "mean_reversion"
    description = "Bollinger band extremes + RSI/stochastic oversold/overbought fade"

    def evaluate(self, ctx: Context, i: int) -> Signal:
        up, mid, lo = ctx.bb_upper[i], ctx.bb_mid[i], ctx.bb_lower[i]
        r, k = ctx.rsi14[i], ctx.stoch_k[i]
        if up is None or r is None or k is None:
            return NEUTRAL
        price = ctx.closes[i]
        band_width = up - lo
        if band_width <= 0:
            return NEUTRAL
        score = 0.0
        parts = []
        if price < lo:
            score += 0.4 + min((lo - price) / band_width, 0.5) * 0.4
            parts.append("close below lower Bollinger band")
            if r < 30:
                score += 0.2
                parts.append(f"RSI oversold {r:.0f}")
            if k < 20:
                score += 0.1
                parts.append("stochastic oversold")
        elif price > up:
            score -= 0.4 + min((price - up) / band_width, 0.5) * 0.4
            parts.append("close above upper Bollinger band")
            if r > 70:
                score -= 0.2
                parts.append(f"RSI overbought {r:.0f}")
            if k > 80:
                score -= 0.1
                parts.append("stochastic overbought")
        else:
            return NEUTRAL
        return Signal(score, ", ".join(parts))
