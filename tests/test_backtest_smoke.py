from datetime import date, datetime, time
from pathlib import Path

import pandas as pd
import pytest
pytest.importorskip("pyarrow")

from src.backtest import CostConfig, run_backtest


def test_sessions4_flatline_exit_smoke(tmp_path: Path):
    expiry = date(2025, 9, 2)
    entry = date(2025, 8, 27)

    rows = []
    strikes = [70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130]

    for ts, day in [
        (datetime(2025, 8, 27, 10, 0), date(2025, 8, 27)),
        (datetime(2025, 8, 28, 10, 0), date(2025, 8, 28)),
        (datetime(2025, 8, 29, 10, 0), date(2025, 8, 29)),
        (datetime(2025, 9, 2, 15, 29), expiry),
    ]:
        for strike in strikes:
            for opt in ("CE", "PE"):
                price = 1.0
                if ts.minute == 0 and day == entry:
                    if opt == "PE":
                        price = {80: 10.0, 75: 4.0, 70: 2.0}.get(strike, 1.0)
                    else:
                        price = {120: 2.0, 125: 1.0, 130: 0.4}.get(strike, 1.0)
                elif ts.date() == date(2025, 8, 28):
                    if opt == "PE":
                        price = {80: 6.0, 75: 4.0, 70: 2.0}.get(strike, 1.0)
                    else:
                        price = {120: 1.0, 125: 1.0, 130: 0.4}.get(strike, 1.0)
                elif ts.date() == date(2025, 8, 29):
                    if opt == "PE":
                        price = {80: 16.0, 75: 4.0, 70: 2.0}.get(strike, 1.0)
                    else:
                        price = {120: 7.0, 125: 1.0, 130: 0.4}.get(strike, 1.0)
                rows.append({
                    "timestamp": ts,
                    "trading_day": day,
                    "expiry": expiry,
                    "strike": strike,
                    "option_type": opt,
                    "close": price,
                })

    option_path = tmp_path / "2025-09-02.parquet"
    pd.DataFrame(rows).to_parquet(option_path, index=False)

    spot_path = tmp_path / "NIFTY.parquet"
    pd.DataFrame([{
        "timestamp": datetime(2025, 8, 29, 10, 0),
        "trading_day": entry,
        "close": 100.0,
    }]).to_parquet(spot_path, index=False)

    cfg = CostConfig(
        brokerage_per_order=0.0,
        stt_on_sell_premium_rate=0.0,
        exchange_turnover_rate=0.0,
        sebi_turnover_rate=0.0,
        stamp_duty_on_buy_premium_rate=0.0,
        gst_rate=0.0,
        slippage_points_per_leg=0.0,
    )

    from src.strategy import STRATEGY_1, STRATEGY_2

    for strategy in (STRATEGY_1, STRATEGY_2):
        trades = run_backtest(
            [option_path],
            spot_path,
            strategy,
            date(2025, 8, 1),
            expiry,
            "calendar4",
            0.05,
            None,
            cfg,
        )
        assert len(trades) == 1
        assert trades.iloc[0]["exit_reason"] == "flatline_proximity"
        assert trades.iloc[0]["entry_date"] == "2025-08-29"
