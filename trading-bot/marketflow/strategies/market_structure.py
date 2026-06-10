"""Market structure (smart money concept): higher-highs/higher-lows vs
lower-highs/lower-lows, plus break of structure (BOS) and change of
character (CHoCH) off confirmed swing points."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class MarketStructure(Strategy):
    name = "market_structure"
    description = "HH/HL vs LH/LL swing structure with BOS/CHoCH detection"

    def evaluate(self, ctx: Context, i: int) -> Signal:
        swing_highs, swing_lows = ctx.confirmed_swings(i)
        if len(swing_highs) < 2 or len(swing_lows) < 2:
            return NEUTRAL
        h2, h1 = swing_highs[-2], swing_highs[-1]
        l2, l1 = swing_lows[-2], swing_lows[-1]
        hh = ctx.candles[h1].high > ctx.candles[h2].high
        hl = ctx.candles[l1].low > ctx.candles[l2].low
        lh = ctx.candles[h1].high < ctx.candles[h2].high
        ll = ctx.candles[l1].low < ctx.candles[l2].low

        score = 0.0
        parts = []
        if hh and hl:
            score += 0.5
            parts.append("uptrend structure (HH+HL)")
        elif lh and ll:
            score -= 0.5
            parts.append("downtrend structure (LH+LL)")

        price = ctx.closes[i]
        last_high = ctx.candles[h1].high
        last_low = ctx.candles[l1].low
        if price > last_high:
            # broke above the last swing high
            if lh and ll:
                score += 0.6
                parts.append("CHoCH: broke swing high against downtrend")
            else:
                score += 0.35
                parts.append("BOS above last swing high")
        elif price < last_low:
            if hh and hl:
                score -= 0.6
                parts.append("CHoCH: broke swing low against uptrend")
            else:
                score -= 0.35
                parts.append("BOS below last swing low")

        if abs(score) < 0.2:
            return NEUTRAL
        return Signal(score, ", ".join(parts))
