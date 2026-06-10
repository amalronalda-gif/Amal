"""Technical indicators, pure Python. All return lists aligned to the input
candles, with None during the warm-up period.
"""

from __future__ import annotations

import math

from .data import Candle


def sma(values: list[float], period: int) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    total = 0.0
    for i, v in enumerate(values):
        total += v
        if i >= period:
            total -= values[i - period]
        if i >= period - 1:
            out[i] = total / period
    return out


def ema(values: list[float], period: int) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    if len(values) < period:
        return out
    k = 2.0 / (period + 1)
    prev = sum(values[:period]) / period  # seed with SMA
    out[period - 1] = prev
    for i in range(period, len(values)):
        prev = values[i] * k + prev * (1 - k)
        out[i] = prev
    return out


def rsi(values: list[float], period: int = 14) -> list[float | None]:
    """Wilder's RSI."""
    out: list[float | None] = [None] * len(values)
    if len(values) <= period:
        return out
    gains = losses = 0.0
    for i in range(1, period + 1):
        d = values[i] - values[i - 1]
        gains += max(d, 0.0)
        losses += max(-d, 0.0)
    avg_gain, avg_loss = gains / period, losses / period
    out[period] = _rsi_value(avg_gain, avg_loss)
    for i in range(period + 1, len(values)):
        d = values[i] - values[i - 1]
        avg_gain = (avg_gain * (period - 1) + max(d, 0.0)) / period
        avg_loss = (avg_loss * (period - 1) + max(-d, 0.0)) / period
        out[i] = _rsi_value(avg_gain, avg_loss)
    return out


def _rsi_value(avg_gain: float, avg_loss: float) -> float:
    if avg_loss == 0:
        return 100.0
    return 100.0 - 100.0 / (1.0 + avg_gain / avg_loss)


def macd(values: list[float], fast: int = 12, slow: int = 26,
         signal: int = 9) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """Returns (macd_line, signal_line, histogram)."""
    ema_fast, ema_slow = ema(values, fast), ema(values, slow)
    line: list[float | None] = [
        (f - s) if f is not None and s is not None else None
        for f, s in zip(ema_fast, ema_slow)
    ]
    # signal = EMA of the macd line over its non-None tail
    start = next((i for i, v in enumerate(line) if v is not None), len(line))
    tail = [v for v in line[start:] if v is not None]
    sig_tail = ema(tail, signal)
    sig: list[float | None] = [None] * len(values)
    for j, v in enumerate(sig_tail):
        sig[start + j] = v
    hist = [(m - s) if m is not None and s is not None else None
            for m, s in zip(line, sig)]
    return line, sig, hist


def atr(candles: list[Candle], period: int = 14) -> list[float | None]:
    """Wilder's Average True Range."""
    out: list[float | None] = [None] * len(candles)
    if len(candles) <= period:
        return out
    trs = [candles[0].range]
    for i in range(1, len(candles)):
        c, p = candles[i], candles[i - 1]
        trs.append(max(c.high - c.low, abs(c.high - p.close), abs(c.low - p.close)))
    prev = sum(trs[1:period + 1]) / period
    out[period] = prev
    for i in range(period + 1, len(candles)):
        prev = (prev * (period - 1) + trs[i]) / period
        out[i] = prev
    return out


def bollinger(values: list[float], period: int = 20, num_std: float = 2.0
              ) -> tuple[list[float | None], list[float | None], list[float | None]]:
    """Returns (upper, middle, lower)."""
    mid = sma(values, period)
    upper: list[float | None] = [None] * len(values)
    lower: list[float | None] = [None] * len(values)
    for i in range(period - 1, len(values)):
        window = values[i - period + 1:i + 1]
        m = mid[i]
        var = sum((v - m) ** 2 for v in window) / period
        sd = math.sqrt(var)
        upper[i] = m + num_std * sd
        lower[i] = m - num_std * sd
    return upper, mid, lower


def stochastic(candles: list[Candle], k_period: int = 14, d_period: int = 3
               ) -> tuple[list[float | None], list[float | None]]:
    """Returns (%K, %D)."""
    k: list[float | None] = [None] * len(candles)
    for i in range(k_period - 1, len(candles)):
        window = candles[i - k_period + 1:i + 1]
        hh = max(c.high for c in window)
        ll = min(c.low for c in window)
        k[i] = 50.0 if hh == ll else (candles[i].close - ll) / (hh - ll) * 100.0
    start = k_period - 1
    d_tail = sma([v for v in k[start:]], d_period)
    d: list[float | None] = [None] * len(candles)
    for j, v in enumerate(d_tail):
        d[start + j] = v
    return k, d


def obv(candles: list[Candle]) -> list[float]:
    out = [0.0] * len(candles)
    for i in range(1, len(candles)):
        if candles[i].close > candles[i - 1].close:
            out[i] = out[i - 1] + candles[i].volume
        elif candles[i].close < candles[i - 1].close:
            out[i] = out[i - 1] - candles[i].volume
        else:
            out[i] = out[i - 1]
    return out


def donchian(candles: list[Candle], period: int = 20
             ) -> tuple[list[float | None], list[float | None]]:
    """Returns (upper, lower) channel of the *previous* `period` bars
    (excluding the current bar, so a close above upper is a breakout)."""
    upper: list[float | None] = [None] * len(candles)
    lower: list[float | None] = [None] * len(candles)
    for i in range(period, len(candles)):
        window = candles[i - period:i]
        upper[i] = max(c.high for c in window)
        lower[i] = min(c.low for c in window)
    return upper, lower


def swing_points(candles: list[Candle], strength: int = 3
                 ) -> tuple[list[int], list[int]]:
    """Fractal swing highs/lows: bar whose high/low is the extreme of
    `strength` bars on each side. Returns (high_indices, low_indices).
    Only confirmed swings (i.e. `strength` bars after) are included."""
    highs, lows = [], []
    for i in range(strength, len(candles) - strength):
        window = candles[i - strength:i + strength + 1]
        if candles[i].high == max(c.high for c in window):
            highs.append(i)
        if candles[i].low == min(c.low for c in window):
            lows.append(i)
    return highs, lows


def ichimoku(candles: list[Candle], tenkan_p: int = 9, kijun_p: int = 26,
             senkou_b_p: int = 52) -> dict[str, list[float | None]]:
    """Tenkan, Kijun and the cloud (senkou A/B values as computed at each bar,
    i.e. un-displaced — compare against values from `kijun_p` bars ago for the
    cloud at the current bar)."""
    n = len(candles)

    def midline(period: int) -> list[float | None]:
        out: list[float | None] = [None] * n
        for i in range(period - 1, n):
            window = candles[i - period + 1:i + 1]
            out[i] = (max(c.high for c in window) + min(c.low for c in window)) / 2
        return out

    tenkan = midline(tenkan_p)
    kijun = midline(kijun_p)
    senkou_a = [(t + k) / 2 if t is not None and k is not None else None
                for t, k in zip(tenkan, kijun)]
    senkou_b = midline(senkou_b_p)
    return {"tenkan": tenkan, "kijun": kijun,
            "senkou_a": senkou_a, "senkou_b": senkou_b}


def linreg_slope(values: list[float]) -> float:
    """Least-squares slope of values vs index, normalized by mean value."""
    n = len(values)
    if n < 2:
        return 0.0
    mean_x = (n - 1) / 2.0
    mean_y = sum(values) / n
    num = sum((i - mean_x) * (v - mean_y) for i, v in enumerate(values))
    den = sum((i - mean_x) ** 2 for i in range(n))
    if den == 0 or mean_y == 0:
        return 0.0
    return (num / den) / abs(mean_y)
