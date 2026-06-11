"""Walk-forward backtest of the H1/H4 pullback strategy.

Reuses the exact live signal function (check_entry), entry at the next
bar's open, fixed SL/TP (no management — the spec is a clean RR 1:2),
conservative intra-bar ordering (SL checked before TP). Respects the
session window, news blackout and the 2-signals-per-day cap. One open
position at a time.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from data import Bar
from strategy import SignalContext, check_entry, local_dt


@dataclass
class BtTrade:
    signal_time: int
    side: str
    entry: float
    exit: float
    r: float           # realized R multiple (-1 / +rr / partial on timeout)
    bars_held: int


@dataclass
class BtResult:
    trades: list[BtTrade] = field(default_factory=list)
    signals: int = 0
    skipped_daily_cap: int = 0
    equity: list[float] = field(default_factory=lambda: [100.0])

    @property
    def win_rate(self) -> float:
        return (sum(1 for t in self.trades if t.r > 0) / len(self.trades)
                if self.trades else 0.0)

    @property
    def profit_factor(self) -> float:
        wins = sum(t.r for t in self.trades if t.r > 0)
        losses = -sum(t.r for t in self.trades if t.r < 0)
        if losses == 0:
            return float("inf") if wins else 0.0
        return wins / losses

    @property
    def avg_r(self) -> float:
        return (sum(t.r for t in self.trades) / len(self.trades)
                if self.trades else 0.0)

    @property
    def max_drawdown(self) -> float:
        peak, dd = float("-inf"), 0.0
        for v in self.equity:
            peak = max(peak, v)
            dd = max(dd, (peak - v) / peak)
        return dd * 100

    def summary(self) -> str:
        pf = self.profit_factor
        return "\n".join([
            "MT5 analyzer backtest",
            "-" * 60,
            f"  signals generated        {self.signals} "
            f"(+{self.skipped_daily_cap} blocked by daily cap)",
            f"  trades simulated         {len(self.trades)}",
            f"  win rate                 {self.win_rate * 100:.1f}%",
            f"  profit factor            "
            f"{'inf' if pf == float('inf') else f'{pf:.2f}'}",
            f"  avg R multiple           {self.avg_r:+.2f}",
            f"  total result             "
            f"{sum(t.r for t in self.trades):+.1f}R",
            f"  equity (1% risk/trade)   "
            f"{self.equity[-1] - 100:+.2f}%",
            f"  max drawdown             {self.max_drawdown:.2f}%",
        ])


def run_backtest(h1: list[Bar], h4: list[Bar], cfg: dict) -> BtResult:
    ctx = SignalContext(h1, h4, cfg)
    res = BtResult()
    warmup = max(cfg["ema_trend_period"] * 4 + 10, 220)
    risk = cfg.get("risk_pct_per_trade", 1.0) / 100.0
    max_hold = cfg.get("max_hold_bars", 96)
    daily: dict = {}
    busy_until = -1

    for i in range(warmup, len(h1) - 2):
        sig = check_entry(ctx, i)
        if sig is None:
            continue
        day = local_dt(sig.time, cfg).date()
        if daily.get(day, 0) >= cfg["max_signals_per_day"]:
            res.skipped_daily_cap += 1
            continue
        daily[day] = daily.get(day, 0) + 1
        res.signals += 1
        if i <= busy_until:
            continue  # already in a position; signal counted but not traded

        entry = h1[i + 1].open
        direction = 1 if sig.side == "LONG" else -1
        sl_dist = abs(sig.entry - sig.sl)
        sl = entry - direction * sl_dist
        tp = entry + direction * cfg["rr"] * sl_dist
        r, exit_px, exit_idx = _simulate(h1, i + 1, direction, entry, sl, tp,
                                         max_hold, cfg["rr"])
        res.trades.append(BtTrade(sig.time, sig.side, entry, exit_px, r,
                                  exit_idx - (i + 1)))
        res.equity.append(res.equity[-1] * (1 + risk * r))
        busy_until = exit_idx
    return res


def _simulate(h1: list[Bar], entry_idx: int, direction: int, entry: float,
              sl: float, tp: float, max_hold: int, rr: float
              ) -> tuple[float, float, int]:
    last = min(entry_idx + max_hold, len(h1) - 1)
    risk = abs(entry - sl)
    for k in range(entry_idx, last + 1):
        b = h1[k]
        if (b.low <= sl) if direction == 1 else (b.high >= sl):
            return -1.0, sl, k          # conservative: SL before TP
        if (b.high >= tp) if direction == 1 else (b.low <= tp):
            return rr, tp, k
    px = h1[last].close
    return (px - entry) * direction / risk, px, last
