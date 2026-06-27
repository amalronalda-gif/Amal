#!/usr/bin/env python3
"""MarketFlow bot CLI.

Examples:
    python3 main.py predict
    python3 main.py predict --symbol PAXGUSDT --interval 4h
    python3 main.py backtest --interval 1h --limit 2000 --threshold 0.3
    python3 main.py watch --interval 15m --every 60
    python3 main.py fetch --limit 3000 --out gold_1h.csv
    python3 main.py backtest --csv gold_1h.csv
"""

import argparse
import sys
import time
from datetime import datetime, timezone

from marketflow.data import DEFAULT_SYMBOL, fetch_klines, load_csv, save_csv
from marketflow.engine import Engine
from marketflow.backtest import run_backtest

DISCLAIMER = ("NOTE: educational tool; probabilistic signals, not financial "
              "advice. Past performance does not guarantee future results.")


def get_candles(args, minimum=250):
    if getattr(args, "csv", None):
        candles = load_csv(args.csv)
        print(f"loaded {len(candles)} candles from {args.csv}")
    else:
        print(f"fetching {args.limit} x {args.interval} candles for "
              f"{args.symbol} from Binance public data API...")
        candles = fetch_klines(args.symbol, args.interval, args.limit)
        print(f"got {len(candles)} candles "
              f"(latest close {candles[-1].close:.2f})")
    if len(candles) < minimum:
        sys.exit(f"error: need at least {minimum} candles, got {len(candles)}")
    return candles


def cmd_predict(args):
    candles = get_candles(args)
    pred = Engine().predict(candles)
    ts = datetime.fromtimestamp(candles[-1].open_time / 1000, tz=timezone.utc)
    print(f"\n{args.symbol} {args.interval} | last bar {ts:%Y-%m-%d %H:%M UTC} "
          f"| close {candles[-1].close:.2f}\n")
    print(pred.summary())
    print(f"\n{DISCLAIMER}")


def cmd_backtest(args):
    candles = get_candles(args, minimum=300)
    print(f"running walk-forward backtest "
          f"(threshold {args.threshold}, stop {args.stop_atr} ATR, "
          f"target {args.target_atr} ATR, max hold {args.max_hold} bars)...\n")
    result = run_backtest(candles, threshold=args.threshold,
                          stop_atr=args.stop_atr, target_atr=args.target_atr,
                          max_hold=args.max_hold)
    print(result.summary())
    print(f"\n{DISCLAIMER}")


def cmd_watch(args):
    print(f"watching {args.symbol} {args.interval}; refresh every "
          f"{args.every}s (Ctrl-C to stop)\n")
    while True:
        try:
            candles = fetch_klines(args.symbol, args.interval, args.limit)
            pred = Engine().predict(candles)
            now = datetime.now(timezone.utc)
            print(f"[{now:%H:%M:%S}] close {candles[-1].close:.2f} -> "
                  f"{pred.direction} (score {pred.score:+.3f}, "
                  f"confidence {pred.confidence:.0f}%)")
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(f"fetch/predict failed: {e}")
        time.sleep(args.every)


def cmd_fetch(args):
    candles = fetch_klines(args.symbol, args.interval, args.limit)
    save_csv(candles, args.out)
    print(f"saved {len(candles)} candles to {args.out}")


def main():
    p = argparse.ArgumentParser(description="MarketFlow multi-strategy bot")
    sub = p.add_subparsers(dest="command", required=True)

    def common(sp):
        sp.add_argument("--symbol", default=DEFAULT_SYMBOL,
                        help="Binance symbol (default PAXGUSDT = gold/USDT)")
        sp.add_argument("--interval", default="1h",
                        help="candle interval, e.g. 15m 1h 4h 1d")
        sp.add_argument("--limit", type=int, default=1000,
                        help="number of candles")
        sp.add_argument("--csv", help="load candles from CSV instead of API")

    sp = sub.add_parser("predict", help="print current market-flow prediction")
    common(sp)
    sp.set_defaults(func=cmd_predict)

    sp = sub.add_parser("backtest", help="walk-forward backtest the ensemble")
    common(sp)
    sp.add_argument("--threshold", type=float, default=0.25,
                    help="min |score| to take a trade")
    sp.add_argument("--stop-atr", type=float, default=1.5)
    sp.add_argument("--target-atr", type=float, default=3.0)
    sp.add_argument("--max-hold", type=int, default=24,
                    help="max bars to hold a position")
    sp.set_defaults(func=cmd_backtest)

    sp = sub.add_parser("watch", help="poll and print predictions repeatedly")
    common(sp)
    sp.add_argument("--every", type=int, default=300,
                    help="seconds between refreshes")
    sp.set_defaults(func=cmd_watch)

    sp = sub.add_parser("fetch", help="download candles to CSV")
    common(sp)
    sp.add_argument("--out", default="candles.csv")
    sp.set_defaults(func=cmd_fetch)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
