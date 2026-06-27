"""Bank manipulation / Judas swing (ICT): during London/NY hours, a sweep
of the Asian session range that snaps back inside marks the manipulation
leg — the real move usually goes the other way. Intraday timeframes only."""

from __future__ import annotations

from datetime import datetime, timezone

from .base import Context, Signal, Strategy, NEUTRAL

ASIA_END_H = 7     # Asian session 00:00-07:00 UTC
ACTIVE_END_H = 17  # consider manipulation plays during 07:00-17:00 UTC


class SessionManipulation(Strategy):
    name = "session_manipulation"
    description = "Judas swing: Asian-range sweep at London/NY that reverses"

    def evaluate(self, ctx: Context, i: int) -> Signal:
        if ctx.step_ms is None or ctx.step_ms > 3600_000:
            return NEUTRAL  # needs intraday candles (<= 1h)
        c = ctx.candles
        now = datetime.fromtimestamp(c[i].open_time / 1000, tz=timezone.utc)
        if not ASIA_END_H <= now.hour < ACTIVE_END_H:
            return NEUTRAL
        day = now.date()
        bars_per_day = 86400_000 // ctx.step_ms
        start = max(0, i - bars_per_day)
        todays = [j for j in range(start, i + 1)
                  if datetime.fromtimestamp(c[j].open_time / 1000,
                                            tz=timezone.utc).date() == day]
        asian = [j for j in todays
                 if datetime.fromtimestamp(c[j].open_time / 1000,
                                           tz=timezone.utc).hour < ASIA_END_H]
        post = [j for j in todays if j not in asian]
        if len(asian) < 3 or not post:
            return NEUTRAL
        asian_hi = max(c[j].high for j in asian)
        asian_lo = min(c[j].low for j in asian)
        price = ctx.closes[i]

        swept_hi = max((c[j].high for j in post), default=0)
        if swept_hi > asian_hi and price < asian_hi:
            return Signal(-0.6, "swept Asian session high then returned "
                                "inside (Judas swing)")
        swept_lo = min((c[j].low for j in post), default=float("inf"))
        if swept_lo < asian_lo and price > asian_lo:
            return Signal(0.6, "swept Asian session low then returned "
                               "inside (Judas swing)")
        return NEUTRAL
