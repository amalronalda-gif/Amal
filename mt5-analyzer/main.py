#!/usr/bin/env python3
"""MT5 XAUUSD analyzer — signals only, no auto-trading.

Live (Windows + MT5 terminal):
    python main.py run

Backtest on MT5 history:
    python main.py backtest --bars 5000

Backtest from CSV (works anywhere; H4 is resampled from H1):
    python main.py backtest --csv path/to/xauusd_h1.csv
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone

import data as d
from strategy import SignalContext, check_entry, local_dt
from backtest import run_backtest
from notifier import log_csv, notify_telegram, signals_today


def cmd_backtest(args, cfg):
    if args.csv:
        h1 = d.load_csv(args.csv)
        h4 = d.resample(h1, "H1", "H4")
        print(f"loaded {len(h1)} H1 bars from {args.csv} "
              f"(H4 resampled: {len(h4)})")
    else:
        d.mt5_connect(cfg)
        try:
            h1 = d.get_bars(cfg["symbol"], "H1", args.bars)
            h4 = d.get_bars(cfg["symbol"], "H4", args.bars // 4 + 60)
        finally:
            d.mt5_disconnect()
        print(f"fetched {len(h1)} H1 / {len(h4)} H4 bars from MT5")
    res = run_backtest(h1, h4, cfg)
    print()
    print(res.summary())


def cmd_run(args, cfg):
    d.mt5_connect(cfg)
    print(f"connected to MT5; analyzing {cfg['symbol']} "
          f"(H1 signal / H4 trend), Ctrl-C to stop")
    last_bar_time = None
    try:
        while True:
            try:
                h1 = d.get_bars(cfg["symbol"], "H1", 400)
                h4 = d.get_bars(cfg["symbol"], "H4", 300)
            except Exception as e:
                print(f"[data] {e}; retrying")
                time.sleep(cfg.get("poll_seconds", 30))
                continue
            if h1 and h1[-1].time != last_bar_time:
                last_bar_time = h1[-1].time
                ctx = SignalContext(h1, h4, cfg)
                sig = check_entry(ctx, len(h1) - 1)
                now = datetime.now(timezone.utc)
                if sig:
                    today = local_dt(sig.time, cfg).date()
                    if signals_today(cfg, today) >= cfg["max_signals_per_day"]:
                        print(f"[{now:%H:%M}] signal suppressed: "
                              f"daily cap reached")
                    else:
                        log_csv(sig, cfg)
                        sent = notify_telegram(sig, cfg)
                        print(f"[{now:%H:%M}] {sig.side} @ {sig.entry:.2f} "
                              f"SL {sig.sl:.2f} TP {sig.tp:.2f} "
                              f"(telegram={'ok' if sent else 'off'})")
                else:
                    bar_dt = datetime.fromtimestamp(last_bar_time,
                                                    tz=timezone.utc)
                    print(f"[{now:%H:%M}] new H1 bar {bar_dt:%H:%M} — no setup")
            time.sleep(cfg.get("poll_seconds", 30))
    except KeyboardInterrupt:
        pass
    finally:
        d.mt5_disconnect()


def main():
    p = argparse.ArgumentParser(description="MT5 XAUUSD signal analyzer")
    p.add_argument("--config", default=None, help="path to config.json")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("run", help="live analysis loop (Windows + MT5)")
    sp.set_defaults(func=cmd_run)
    sp = sub.add_parser("backtest", help="walk-forward backtest")
    sp.add_argument("--bars", type=int, default=None,
                    help="H1 bars to fetch from MT5")
    sp.add_argument("--csv", help="H1 CSV file instead of MT5")
    sp.set_defaults(func=cmd_backtest)
    args = p.parse_args()
    cfg = d.load_config(args.config)
    if args.cmd == "backtest" and args.bars is None:
        args.bars = cfg.get("backtest_h1_bars", 5000)
    args.func(args, cfg)


if __name__ == "__main__":
    main()
