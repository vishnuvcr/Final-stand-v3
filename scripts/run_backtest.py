import argparse
import json
from datetime import date
from pathlib import Path

from src.backtest import CostConfig, run_backtest, write_summary
from src.strategy import STRATEGY_1, STRATEGY_2


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--dte-mode", default="calendar4", choices=["calendar4", "sessions4"])
    p.add_argument("--target-fraction", type=float, default=0.95)
    p.add_argument("--lot-size", type=int, default=0, help="0 means point P&L only")
    p.add_argument("--brokerage", type=float, default=10.0)
    p.add_argument("--stt", type=float, default=0.0015)
    p.add_argument("--exchange-rate", type=float, required=True)
    p.add_argument("--sebi-rate", type=float, required=True)
    p.add_argument("--stamp-rate", type=float, required=True)
    p.add_argument("--gst-rate", type=float, default=0.18)
    p.add_argument("--slippage-points", type=float, default=0.0)
    p.add_argument("--out", default="artifacts")
    a = p.parse_args()

    data = Path(a.data)
    option_files = sorted((data / "options" / "NIFTY").glob("*.parquet"))
    if not option_files:
        raise SystemExit("No NIFTY option parquet files found")

    start = date.fromisoformat(a.start)
    end = date.fromisoformat(a.end)
    lot = None if a.lot_size == 0 else a.lot_size
    costs = CostConfig(
        brokerage_per_order=a.brokerage,
        stt_on_sell_premium_rate=a.stt,
        exchange_turnover_rate=a.exchange_rate,
        sebi_turnover_rate=a.sebi_rate,
        stamp_duty_on_buy_premium_rate=a.stamp_rate,
        gst_rate=a.gst_rate,
        slippage_points_per_leg=a.slippage_points,
    )

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    for strategy in (STRATEGY_1, STRATEGY_2):
        trades = run_backtest(
            option_files,
            data / "index" / "NIFTY.parquet",
            strategy,
            start,
            end,
            a.dte_mode,
            a.target_fraction,
            lot,
            costs,
        )
        csv_path = out / f"{strategy.name}.csv"
        json_path = out / f"{strategy.name}.json"
        trades.to_csv(csv_path, index=False)
        write_summary(trades, json_path)
        print(json.dumps({"strategy": strategy.name, "trades": len(trades)}))


if __name__ == "__main__":
    main()
