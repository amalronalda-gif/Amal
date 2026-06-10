# MarketFlow — Multi-Strategy Market Flow Prediction Bot (XAUUSDT / Gold)

A zero-dependency Python bot that combines **11 well-known trading strategies**
into a weighted ensemble and outputs a probabilistic "market flow" reading
(BULLISH / BEARISH / NEUTRAL with a confidence score) for gold priced in USDT.

> **Important disclaimer**
> No bot can truly *predict* the market — anyone claiming otherwise is selling
> something. This tool aggregates the same publicly known strategies that human
> traders use and expresses them as probabilities. Backtests here exclude fees,
> spread and slippage; real results will be worse. This is an educational /
> research tool, **not financial advice**. Never trade money you can't afford
> to lose, and the bot deliberately does **not** place orders.

## Data

Uses Binance's public market-data API (`data-api.binance.vision`, no API key
needed). The default symbol is **PAXGUSDT** (PAX Gold — 1 token = 1 troy oz of
gold), which is the tradable gold/USDT market on Binance spot and tracks
XAU/USD closely. Any other Binance spot symbol works too (`--symbol BTCUSDT`).

## The 11 strategies

| Strategy | Idea |
|---|---|
| `liquidity_sweep` | Stop-hunt wicks through swing lows/highs that close back inside → reversal (smart money concept) |
| `trend_following` | EMA 20/50/200 stack alignment and slope |
| `momentum` | MACD cross + histogram expansion, confirmed by RSI regime |
| `mean_reversion` | Fade closes outside Bollinger bands at RSI/stochastic extremes |
| `market_structure` | HH/HL vs LH/LL swings, break of structure (BOS), change of character (CHoCH) |
| `fair_value_gap` | Reactions from unfilled 3-candle imbalances (FVG) |
| `breakout` | 20-bar Donchian channel breakout with volume confirmation |
| `candlestick` | Engulfing, hammer/shooting star, morning/evening star — in trend context |
| `volume_flow` | OBV trend confirmation and price/OBV divergence (accumulation/distribution) |
| `ichimoku` | Price vs Kumo cloud, Tenkan/Kijun cross |
| `support_resistance` | Bounces from multi-touch horizontal levels |

Each strategy scores the market in **[-1, +1]**. The engine combines them with
quality weights (structure/trend signals weigh more than single-candle
patterns), damps mean-reversion when it fights a strong trend, and reports the
ensemble score, a confidence percentage, and how much the strategies agree.

## Usage

Requires Python 3.10+. No packages to install.

```bash
cd trading-bot

# current market-flow prediction with per-strategy breakdown
python3 main.py predict
python3 main.py predict --interval 4h --limit 1500

# walk-forward backtest (no look-ahead: each bar only sees prior data)
python3 main.py backtest --interval 4h --limit 1500 --threshold 0.3

# keep polling and printing predictions
python3 main.py watch --interval 15m --every 60

# work offline: download once, then reuse the CSV
python3 main.py fetch --interval 1h --limit 3000 --out gold_1h.csv
python3 main.py backtest --csv gold_1h.csv
```

Example output:

```
Market flow: BEARISH  (score -0.333, confidence 65%, agreement 83%)
------------------------------------------------------------------------
  v trend_following      -1.00  bearish EMA stack 20<50<200, price below EMA200
  v market_structure     -0.85  downtrend structure (LH+LL), BOS below last swing low
  v momentum             -0.75  MACD below signal, histogram expanding down, RSI 31
  ^ liquidity_sweep      +0.48  swept sell-side liquidity below swing low(s), closed back above
  ...
```

## Backtester

`backtest` walks the data bar by bar; when the ensemble score crosses the
threshold it enters at the next bar's open with an ATR-based stop (1.5 ATR)
and target (3 ATR), risking 1% of equity per trade. It reports directional
accuracy, win rate, average R, profit factor, total return vs buy & hold, and
max drawdown. Stops are checked before targets within a bar (conservative).

A 400-candle sample dataset is included at
`sample_data/paxgusdt_4h_sample.csv` so everything runs offline.

## Telegram bot

Get MarketFlow predictions and direction-flip alerts in Telegram:

1. In Telegram, open **@BotFather** → send `/newbot` → pick a name and a
   username ending in `bot` → copy the HTTP API **token** it gives you.
2. Run the bot (any machine with Python 3.10+ and internet, e.g. a VPS,
   Raspberry Pi, or your laptop):

   ```bash
   cd trading-bot
   export TELEGRAM_BOT_TOKEN="123456789:AAExampleTokenFromBotFather"
   python3 telegram_bot.py
   ```
3. Open your bot in Telegram and send `/start`.

Commands:

| Command | What it does |
|---|---|
| `/predict [symbol] [interval]` | current flow reading with strategy breakdown, e.g. `/predict 4h` |
| `/backtest [symbol] [interval]` | walk-forward backtest over 1500 bars |
| `/watch [symbol] [interval] [minutes]` | message you whenever the flow direction flips (checked every N minutes, default 15) |
| `/unwatch` | stop alerts |
| `/status` | show your subscription |

To keep the bot private, set `TELEGRAM_ALLOWED_CHATS` to a comma-separated
list of allowed chat IDs (send `/status` once and check the console log, or
ask @userinfobot for your ID). Subscriptions persist across restarts in
`subscriptions.json`. To keep it running on a server:
`nohup python3 telegram_bot.py >> bot.log 2>&1 &` (or a systemd unit).

## Tuning

- Weights: `marketflow/engine.py` → `DEFAULT_WEIGHTS`
- Entry threshold, stop/target ATR multiples, max holding period: CLI flags
- Add a strategy: subclass `Strategy` in `marketflow/strategies/`, implement
  `evaluate(ctx, i) -> Signal`, register it in `strategies/__init__.py`

## Honest expectations

In our test runs the ensemble was roughly break-even on 1h bars and showed an
edge on 4h bars (≈56% directional accuracy, profit factor ≈1.2 over ~7 months)
— *before* fees and slippage, on one historical window. That is what a
realistic multi-strategy signal looks like: a small, fragile edge, not a money
printer. Always re-backtest on fresh data and paper-trade before risking
anything.
