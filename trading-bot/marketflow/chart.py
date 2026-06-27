"""Chart rendering: candlestick PNG with full analysis overlay.

Optional feature — requires matplotlib (pip install matplotlib). Everything
degrades gracefully: when matplotlib is missing, render_chart returns None
and the bot simply sends text-only messages.
"""

from __future__ import annotations

import os
import tempfile

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    HAVE_MPL = True
except ImportError:
    HAVE_MPL = False

from .data import Candle
from . import indicators as ta

BG = "#131722"          # TradingView-like dark theme
FG = "#d1d4dc"
GRID = "#2a2e39"
UP = "#26a69a"
DOWN = "#ef5350"


def render_chart(candles: list[Candle], title: str = "",
                 levels: dict[str, float] | None = None,
                 side: int | None = None, bars: int = 120,
                 path: str | None = None) -> str | None:
    """Draw the last `bars` candles with EMAs, VWAP, swing S/R levels and
    (optionally) entry/SL/TP lines. Returns the PNG path or None when
    matplotlib is unavailable."""
    if not HAVE_MPL or len(candles) < 60:
        return None

    closes = [c.close for c in candles]
    ema20 = ta.ema(closes, 20)
    ema50 = ta.ema(closes, 50)
    ema200 = ta.ema(closes, 200)
    swing_highs, swing_lows = ta.swing_points(candles, 3)
    vwap = _rolling_vwap(candles, 96)

    window = candles[-bars:]
    off = len(candles) - len(window)
    xs = range(len(window))

    fig, ax = plt.subplots(figsize=(11, 6), dpi=110)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # candles
    for x, c in zip(xs, window):
        color = UP if c.bullish else DOWN
        ax.plot([x, x], [c.low, c.high], color=color, linewidth=0.8, zorder=2)
        body_lo, body_hi = min(c.open, c.close), max(c.open, c.close)
        height = max(body_hi - body_lo, (c.high - c.low) * 0.02 or 1e-9)
        ax.add_patch(Rectangle((x - 0.35, body_lo), 0.7, height,
                               facecolor=color, edgecolor=color, zorder=3))

    # overlays
    for series, color, label in ((ema20, "#f6c026", "EMA20"),
                                 (ema50, "#fb7c50", "EMA50"),
                                 (ema200, "#9c6ade", "EMA200"),
                                 (vwap, "#58a6ff", "VWAP")):
        ys = [series[off + x] for x in xs]
        if any(y is not None for y in ys):
            ax.plot(list(xs), ys, color=color, linewidth=1.1,
                    label=label, zorder=4)

    # swing-based support/resistance dots
    for s in swing_highs:
        if s >= off:
            ax.plot(s - off, candles[s].high, marker="v", color="#ef9a9a",
                    markersize=4, zorder=5)
    for s in swing_lows:
        if s >= off:
            ax.plot(s - off, candles[s].low, marker="^", color="#a5d6a7",
                    markersize=4, zorder=5)

    # entry/SL/TP levels and risk/profit zones
    if levels:
        styles = {"entry": ("#58a6ff", "-"), "SL": (DOWN, "--"),
                  "TP1": (UP, ":"), "TP2": (UP, "--")}
        x_right = len(window) - 1
        for name, value in levels.items():
            color, ls = styles.get(name, (FG, ":"))
            ax.axhline(value, color=color, linestyle=ls, linewidth=1.2,
                       zorder=6)
            ax.annotate(f"{name} {value:.2f}" if value >= 10
                        else f"{name} {value:.5f}",
                        xy=(x_right, value), xytext=(4, 0),
                        textcoords="offset points", color=color,
                        fontsize=8, va="center", zorder=7)
        if side and "entry" in levels:
            if "SL" in levels:
                ax.axhspan(*sorted((levels["entry"], levels["SL"])),
                           color=DOWN, alpha=0.10, zorder=1)
            if "TP2" in levels:
                ax.axhspan(*sorted((levels["entry"], levels["TP2"])),
                           color=UP, alpha=0.10, zorder=1)

    ax.set_title(title, color=FG, fontsize=11, loc="left")
    ax.grid(color=GRID, linewidth=0.5, zorder=0)
    ax.tick_params(colors=FG, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.set_xlim(-1, len(window) + 8)  # room for level labels
    ax.legend(loc="upper left", fontsize=8, facecolor=BG, edgecolor=GRID,
              labelcolor=FG)
    fig.tight_layout()

    if path is None:
        fd, path = tempfile.mkstemp(suffix=".png", prefix="marketflow_")
        os.close(fd)
    fig.savefig(path, facecolor=BG)
    plt.close(fig)
    return path


def _rolling_vwap(candles: list[Candle], window: int) -> list[float | None]:
    cum_pv, cum_v = [0.0], [0.0]
    for c in candles:
        typical = (c.high + c.low + c.close) / 3.0
        cum_pv.append(cum_pv[-1] + typical * c.volume)
        cum_v.append(cum_v[-1] + c.volume)
    out: list[float | None] = [None] * len(candles)
    for i in range(window - 1, len(candles)):
        vol = cum_v[i + 1] - cum_v[i + 1 - window]
        if vol > 0:
            out[i] = (cum_pv[i + 1] - cum_pv[i + 1 - window]) / vol
    return out
