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
    "rsi_divergence": 1.1,
    "order_block": 1.0,
    "volume_flow": 1.0,
    "breakout": 1.0,
    "vwap": 0.9,
    "ichimoku": 0.9,
    "fair_value_gap": 0.9,
    "mean_reversion": 0.8,
    "news_sentiment": 0.6,  # live-only overlay supplied by the bot
    "double_top": 0.9,
    "head_shoulders": 0.9,
    "trendline": 1.0,
}

# direction thresholds, recalibrated whenever the registered ensemble
# changes (the weight sum scales the weighted-mean score)
BULLISH_T = 0.14
BEARISH_T = -0.14

# ADX trend-strength bands for the informational regime label (not used to
# re-weight signals: backtests showed weight-shifting by ADX hurt the edge).
ADX_TREND = 25.0   # >= strong directional trend
ADX_RANGE = 18.0   # <= flat/choppy

# Per-market weight overrides. FX majors are range-bound and mean-reverting:
# damp trend/breakout signals, boost fades (lifted EURUSDT 1h backtest
# profit factor 0.74 -> 1.29 when first tuned). Gold and BTC trend, so they
# keep the defaults.
MARKET_PROFILES: dict[str, dict[str, float]] = {
    "EURUSDT": {"trend_following": 0.7, "breakout": 0.5, "momentum": 0.8,
                "mean_reversion": 1.5,
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
    adx: float | None = None  # trend strength at the evaluated bar

    @property
    def regime(self) -> str:
        """trending / ranging / transitional from ADX (informational)."""
        if self.adx is None:
            return "unknown"
        if self.adx >= ADX_TREND:
            return "trending"
        if self.adx <= ADX_RANGE:
            return "ranging"
        return "transitional"

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

    def predict_at(self, ctx: Context, i: int,
                   extra_signals: dict[str, Signal] | None = None) -> Prediction:
        signals = {s.name: s.evaluate(ctx, i) for s in self.strategies}
        if extra_signals:
            signals.update(extra_signals)

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
        adx = ctx.adx14[i] if i < len(ctx.adx14) else None
        return Prediction(direction, score, min(confidence, 99.0),
                          agreement, signals, adx)

    def predict(self, candles: list[Candle],
                extra_signals: dict[str, Signal] | None = None) -> Prediction:
        if len(candles) < Context.MIN_BARS:
            raise ValueError(f"need at least {Context.MIN_BARS} candles, "
                             f"got {len(candles)}")
        ctx = Context(candles)
        return self.predict_at(ctx, len(candles) - 1, extra_signals)
