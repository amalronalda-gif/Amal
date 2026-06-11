"""Walk-forward backtest of the ensemble engine.

At every bar i the engine sees only data up to i. When |score| exceeds the
entry threshold a position opens at the NEXT bar's open and exits on an
ATR-based stop/target or after a maximum holding period. Also reports raw
directional accuracy of the prediction vs the forward return.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .data import Candle
from .engine import Engine
from .strategies import Context


@dataclass
class Trade:
    entry_index: int
    exit_index: int
    direction: int      # +1 long, -1 short
    entry: float
    exit: float
    r_multiple: float

    @property
    def pnl_pct(self) -> float:
        return (self.exit / self.entry - 1.0) * 100.0 * self.direction


@dataclass
class BacktestResult:
    trades: list[Trade] = field(default_factory=list)
    predictions: int = 0
    directional_hits: int = 0
    directional_total: int = 0
    equity_curve: list[float] = field(default_factory=list)
    buy_hold_return: float = 0.0

    @property
    def win_rate(self) -> float:
        if not self.trades:
            return 0.0
        return sum(1 for t in self.trades if t.pnl_pct > 0) / len(self.trades)

    @property
    def profit_factor(self) -> float:
        wins = sum(t.pnl_pct for t in self.trades if t.pnl_pct > 0)
        losses = -sum(t.pnl_pct for t in self.trades if t.pnl_pct < 0)
        if losses == 0:
            return float("inf") if wins > 0 else 0.0
        return wins / losses

    @property
    def total_return(self) -> float:
        if not self.equity_curve:
            return 0.0
        return (self.equity_curve[-1] / self.equity_curve[0] - 1.0) * 100.0

    @property
    def max_drawdown(self) -> float:
        peak, mdd = float("-inf"), 0.0
        for v in self.equity_curve:
            peak = max(peak, v)
            mdd = max(mdd, (peak - v) / peak)
        return mdd * 100.0

    @property
    def directional_accuracy(self) -> float:
        if not self.directional_total:
            return 0.0
        return self.directional_hits / self.directional_total

    def summary(self) -> str:
        avg_r = (sum(t.r_multiple for t in self.trades) / len(self.trades)
                 if self.trades else 0.0)
        pf = self.profit_factor
        return "\n".join([
            "Backtest results",
            "-" * 72,
            f"  predictions evaluated     {self.predictions}",
            f"  directional accuracy      {self.directional_accuracy * 100:.1f}% "
            f"({self.directional_hits}/{self.directional_total} non-neutral calls)",
            f"  trades taken              {len(self.trades)}",
            f"  win rate                  {self.win_rate * 100:.1f}%",
            f"  avg R multiple            {avg_r:+.2f}",
            f"  profit factor             {'inf' if pf == float('inf') else f'{pf:.2f}'}",
            f"  strategy return           {self.total_return:+.2f}% "
            f"(1% risk per trade, no fees/slippage)",
            f"  buy & hold return         {self.buy_hold_return:+.2f}%",
            f"  max drawdown              {self.max_drawdown:.2f}%",
        ])


def run_backtest(candles: list[Candle], engine: Engine | None = None,
                 threshold: float = 0.21, stop_atr: float = 1.5,
                 target_atr: float = 3.0, max_hold: int = 24,
                 risk_pct: float = 1.0, horizon: int = 12) -> BacktestResult:
    engine = engine or Engine()
    ctx = Context(candles)
    result = BacktestResult()
    equity = 100.0
    result.equity_curve.append(equity)

    start = Context.MIN_BARS
    if len(candles) <= start + 2:
        raise ValueError(f"need more than {start + 2} candles to backtest")
    result.buy_hold_return = (candles[-1].close / candles[start].close - 1) * 100

    in_trade_until = -1
    i = start
    while i < len(candles) - 2:
        pred = engine.predict_at(ctx, i)
        result.predictions += 1

        # directional accuracy over a fixed horizon
        j = min(i + horizon, len(candles) - 1)
        fwd = candles[j].close - candles[i].close
        if pred.direction != "NEUTRAL" and fwd != 0:
            result.directional_total += 1
            if (fwd > 0) == (pred.direction == "BULLISH"):
                result.directional_hits += 1

        if abs(pred.score) >= threshold and i > in_trade_until:
            a = ctx.atr14[i]
            if a:
                direction = 1 if pred.score > 0 else -1
                entry = candles[i + 1].open
                stop = entry - direction * stop_atr * a
                target = entry + direction * target_atr * a
                exit_price, exit_idx = _simulate(candles, i + 1, direction,
                                                 stop, target, max_hold)
                risk = abs(entry - stop)
                r_mult = (exit_price - entry) * direction / risk if risk else 0.0
                result.trades.append(Trade(i + 1, exit_idx, direction,
                                           entry, exit_price, r_mult))
                equity *= 1.0 + (risk_pct / 100.0) * r_mult
                result.equity_curve.append(equity)
                in_trade_until = exit_idx
        i += 1
    return result


def _simulate(candles: list[Candle], entry_idx: int, direction: int,
              stop: float, target: float, max_hold: int) -> tuple[float, int]:
    last = min(entry_idx + max_hold, len(candles) - 1)
    for k in range(entry_idx, last + 1):
        c = candles[k]
        if direction == 1:
            if c.low <= stop:       # conservative: stop checked before target
                return stop, k
            if c.high >= target:
                return target, k
        else:
            if c.high >= stop:
                return stop, k
            if c.low <= target:
                return target, k
    return candles[last].close, last
