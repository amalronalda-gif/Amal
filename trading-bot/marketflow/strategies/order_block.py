"""Order blocks (smart money concept): the last opposite-direction candle
before an impulsive move. Price returning into an unviolated block tends to
react in the impulse's direction (institutions defend their entry zone)."""

from __future__ import annotations

from .base import Context, Signal, Strategy, NEUTRAL


class OrderBlock(Strategy):
    name = "order_block"
    description = "Reaction from unmitigated order blocks before impulses"

    LOOKBACK = 40
    IMPULSE_ATR = 1.5   # move within 3 candles that qualifies as impulsive

    def evaluate(self, ctx: Context, i: int) -> Signal:
        a = ctx.atr14[i]
        if a is None or a <= 0 or i < 6:
            return NEUTRAL
        c = ctx.candles
        price = ctx.closes[i]
        best = NEUTRAL
        for j in range(max(2, i - self.LOOKBACK), i - 2):
            after = c[j + 1:min(j + 4, i + 1)]
            if not after:
                continue
            if not c[j].bullish:  # bearish candle then impulse up = bullish OB
                move = max(x.high for x in after) - c[j].close
                if move >= self.IMPULSE_ATR * a:
                    lo, hi = c[j].close, c[j].open  # bearish body
                    violated = any(x.close < lo for x in c[j + 1:i + 1])
                    if not violated and lo <= price <= hi:
                        strength = min(move / a / 3.0, 1.0)
                        best = Signal(0.4 + 0.25 * strength,
                                      f"price inside bullish order block "
                                      f"({lo:.2f}-{hi:.2f})")
            else:  # bullish candle then impulse down = bearish OB
                move = c[j].close - min(x.low for x in after)
                if move >= self.IMPULSE_ATR * a:
                    lo, hi = c[j].open, c[j].close  # bullish body
                    violated = any(x.close > hi for x in c[j + 1:i + 1])
                    if not violated and lo <= price <= hi:
                        strength = min(move / a / 3.0, 1.0)
                        best = Signal(-(0.4 + 0.25 * strength),
                                      f"price inside bearish order block "
                                      f"({lo:.2f}-{hi:.2f})")
        return best
