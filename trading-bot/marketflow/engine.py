"""Ensemble engine: combines all strategy scores into one market-flow
prediction with a confidence reading.

Weights reflect rough consensus on signal quality for gold intraday/swing:
structure- and trend-based signals carry more, single-candle patterns less.
Mean reversion is automatically damped when the trend module is strongly
directional (don't fade a freight train).
"""

from __future__ import annotations

from dataclasses import dataclass

from .data import Candle
from .strategies import ALL_STRATEGIES, Context, Signal

DEFAULT_WEIGHTS = {
    "trend_following": 1.3,
    "market_structure": 1.3,
    "liquidity_sweep": 1.2,
    "momentum": 1.1,
    "volume_flow": 1.0,
    "breakout": 1.0,
    "ichimoku": 0.9,
    "fair_value_gap": 0.9,
    "support_resistance": 0.9,
    "mean_reversion": 0.8,
    "candlestick": 0.7,
}

BULLISH_T = 0.18
BEARISH_T = -0.18

# Per-market weight overrides. FX majors are range-bound and mean-reverting:
# damp trend/breakout signals, boost fades. Backtested on EURUSDT 1h where
# this lifted profit factor 0.74 -> 1.29; metals keep the default profile
# (the same overrides hurt silver in testing).
MARKET_PROFILES = {
    "EURUSDT": {"trend_following": 0.7, "breakout": 0.5, "momentum": 0.8,
                "mean_reversion": 1.5, "support_resistance": 1.4,
                "liquidity_sweep": 1.3, "market_structure": 1.0},
}


def engine_for(symbol: str) -> "Engine":
    """Engine with the weight profile for this (possibly aliased) symbol."""
    from .data import SYMBOL_ALIASES
    resolved = SYMBOL_ALIASES.get(symbol.upper(), symbol.upper())
    return Engine(MARKET_PROFILES.get(resolved))


@dataclass
class Prediction:
    direction: str            # BULLISH / BEARISH / NEUTRAL
    score: float              # weighted ensemble score in [-1, 1]
    confidence: float         # 0..100
    agreement: float          # fraction of non-neutral strategies agreeing
    signals: dict[str, Signal]

    def summary(self) -> str:
        lines = [
            f"Market flow: {self.direction}  "
            f"(score {self.score:+.3f}, confidence {self.confidence:.0f}%, "
            f"agreement {self.agreement * 100:.0f}%)",
            "-" * 72,
        ]
        ordered = sorted(self.signals.items(), key=lambda kv: -abs(kv[1].score))
        for name, sig in ordered:
            arrow = "^" if sig.score > 0 else ("v" if sig.score < 0 else "-")
            lines.append(f"  {arrow} {name:<20} {sig.score:+.2f}  {sig.reason}")
        return "\n".join(lines)


class Engine:
    def __init__(self, weights: dict[str, float] | None = None):
        self.weights = dict(DEFAULT_WEIGHTS)
        if weights:
            self.weights.update(weights)
        self.strategies = [cls() for cls in ALL_STRATEGIES]

    def predict_at(self, ctx: Context, i: int) -> Prediction:
        signals = {s.name: s.evaluate(ctx, i) for s in self.strategies}

        # regime damping: don't let mean reversion fight a strong trend
        trend = signals["trend_following"].score
        if abs(trend) > 0.6:
            mr = signals["mean_reversion"]
            if mr.score * trend < 0:
                signals["mean_reversion"] = Signal(
                    mr.score * 0.4, mr.reason + " (damped: strong opposing trend)")

        total_w = sum(self.weights.get(n, 1.0) for n in signals)
        score = sum(sig.score * self.weights.get(n, 1.0)
                    for n, sig in signals.items()) / total_w

        active = [s for s in signals.values() if s.score != 0.0]
        if active:
            majority = 1 if score >= 0 else -1
            agreement = sum(1 for s in active if s.score * majority > 0) / len(active)
        else:
            agreement = 0.0

        if score > BULLISH_T:
            direction = "BULLISH"
        elif score < BEARISH_T:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"

        confidence = min(abs(score) * 120, 70) + agreement * 30 if active else 0.0
        return Prediction(direction, score, min(confidence, 99.0),
                          agreement, signals)

    def predict(self, candles: list[Candle]) -> Prediction:
        if len(candles) < Context.MIN_BARS:
            raise ValueError(f"need at least {Context.MIN_BARS} candles, "
                             f"got {len(candles)}")
        ctx = Context(candles)
        return self.predict_at(ctx, len(candles) - 1)
