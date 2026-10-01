from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
import json

import pandas as pd

from src.strategy import RatioStrategy

def historical_nifty_lot_size(expiry: date) -> int:
    # NSE Circular FAOP70616: weekly/monthly NIFTY contracts retained lot 75
    # through 23-Dec-2025; first revised weekly lot 65 was 06-Jan-2026.
    if expiry <= date(2025, 12, 23):
        return 75
    if expiry >= date(2026, 1, 6):
        return 65
    raise ValueError(f"No NIFTY weekly lot-size regime defined for expiry {expiry}")
    
def historical_stt_rate(trade_date: date) -> float:
    # NSE current levy table: 0.10% through 31-Mar-2026; 0.15% from 01-Apr-2026.
    return 0.001 if trade_date < date(2026, 4, 1) else 0.0015


@dataclass(frozen=True)
class CostConfig:
    brokerage_per_order: float
    stt_on_sell_premium_rate: float
    exchange_turnover_rate: float
    sebi_turnover_rate: float
    stamp_duty_on_buy_premium_rate: float
    gst_rate: float
    slippage_points_per_leg: float = 0.0

    def validate(self) -> None:
        vals = [
            self.brokerage_per_order,
            self.stt_on_sell_premium_rate,
            self.exchange_turnover_rate,
            self.sebi_turnover_rate,
            self.stamp_duty_on_buy_premium_rate,
            self.gst_rate,
            self.slippage_points_per_leg,
        ]
        if any(v < 0 for v in vals):
            raise ValueError("Cost rates cannot be negative.")


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"])
    out["trading_day"] = pd.to_datetime(out["trading_day"]).dt.date
    out["expiry"] = pd.to_datetime(out["expiry"]).dt.date
    out["option_type"] = out["option_type"].astype(str).str.upper().replace({"CALL": "CE", "PUT": "PE"})
    return out


def eligible_entry_dates(expiry: date, trading_days: Iterable[date], dte_mode: str) -> list[date]:
    days = sorted(set(trading_days))
    if dte_mode == "calendar4":
        d = date.fromordinal(expiry.toordinal() - 4)
        return [d] if d in days else []
    if dte_mode == "sessions4":
        if expiry not in days:
            return []
        i = days.index(expiry)
        return [days[i - 4]] if i >= 4 else []
    raise ValueError("dte_mode must be calendar4 or sessions4")


def _leg_prices(df: pd.DataFrame, strikes: list[float], option_type: str) -> pd.DataFrame:
    x = df[(df["option_type"] == option_type) & (df["strike"].isin(strikes))]
    x = x[["timestamp", "strike", "close"]].copy()
    p = x.pivot_table(index="timestamp", columns="strike", values="close", aggfunc="last")
    return p.dropna(subset=strikes).sort_index()


def _turnover_and_costs(
    entry_prices: dict[float, float],
    exit_prices: dict[float, float],
    legs: list[tuple[float, int]],
    lot_size: int,
    cfg: CostConfig,
) -> float:
    cfg.validate()
    brokerage = 6.0 * cfg.brokerage_per_order
    buy_premium = 0.0
    sell_premium = 0.0
    turnover = 0.0

    for strike, sign in legs:
        ep, xp = entry_prices[strike], exit_prices[strike]
        turnover += lot_size * (ep + xp)
        if sign == 1:
            buy_premium += lot_size * ep
            sell_premium += lot_size * xp
        else:
            sell_premium += lot_size * ep
            buy_premium += lot_size * xp

    stt = sell_premium * cfg.stt_on_sell_premium_rate
    exchange = turnover * cfg.exchange_turnover_rate
    sebi = turnover * cfg.sebi_turnover_rate
    stamp = buy_premium * cfg.stamp_duty_on_buy_premium_rate
    gst = cfg.gst_rate * (brokerage + exchange + sebi)
    return brokerage + stt + exchange + sebi + stamp + gst


def run_backtest(
    option_files: list[Path],
    spot_file: Path,
    strategy: RatioStrategy,
    start: date,
    end: date,
    dte_mode: str,
    flatline_tolerance: float,
    lot_size: int | None,
    cost_config: CostConfig,
) -> pd.DataFrame:
    strategy.validate()

    expiry_maps: list[tuple[Path, date, list[date]]] = []
    all_entries: set[date] = set()

    for path in option_files:
        df0 = pd.read_parquet(path, columns=["trading_day", "expiry"])
        if df0.empty:
            continue
        df0["trading_day"] = pd.to_datetime(df0["trading_day"]).dt.date
        df0["expiry"] = pd.to_datetime(df0["expiry"]).dt.date
        if df0.empty:
            continue
        for expiry in sorted(df0["expiry"].unique()):
            if not (start <= expiry <= end):
                continue
            eligible = [d for d in eligible_entry_dates(expiry, df0["trading_day"], dte_mode) if start <= d <= end]
            if eligible:
                expiry_maps.append((path, expiry, eligible))
                all_entries.update(eligible)

    if not all_entries:
        return pd.DataFrame()

    spot = pd.read_parquet(spot_file)
    spot["timestamp"] = pd.to_datetime(spot["timestamp"])
    spot["trading_day"] = pd.to_datetime(spot["trading_day"]).dt.date
    spot["hhmm"] = spot["timestamp"].dt.strftime("%H:%M")
    spot10 = spot[
        spot["trading_day"].isin(all_entries) & (spot["hhmm"] == "10:00")
    ][["trading_day", "close"]]
    spot_map = dict(zip(spot10["trading_day"], spot10["close"]))

    trades: list[dict] = []

    for path, expiry, entries in expiry_maps:
        raw = _prepare(pd.read_parquet(path))
        for entry_date in entries:
            if entry_date not in spot_map:
                continue

            day = raw[(raw["trading_day"] >= entry_date) & (raw["trading_day"] <= expiry)]
            strikes = sorted(day["strike"].dropna().unique().tolist())
            if len(strikes) < 7:
                continue

            atm = float(min(strikes, key=lambda s: abs(s - spot_map[entry_date])))
            legs = strategy.signed_legs(atm, strikes)
            leg_strikes = [k for k, _ in legs]

            prices = _leg_prices(day, leg_strikes, strategy.option_type)
            entry_rows = prices[(prices.index.date == entry_date) & (prices.index.strftime("%H:%M") == "10:00")]
            if entry_rows.empty:
                continue

            entry_ts = entry_rows.index[0]
            ep = {k: float(prices.loc[entry_ts, k]) for k in leg_strikes}

            # Executed entry prices: adverse slippage for each leg.
            entry_exec = {}
            for strike, sign in legs:
                adjustment = cost_config.slippage_points_per_leg
                entry_exec[strike] = ep[strike] + (adjustment if sign == 1 else -adjustment)

            max_profit = strategy.max_profit_points(entry_exec, legs)
            flatline = strategy.flatline_points(entry_exec, legs)
            bump_height = max_profit - flatline
            if not (0 <= flatline_tolerance <= 1):
                raise ValueError("flatline_tolerance must be between 0 and 1.")
            tolerance_points = flatline_tolerance * bump_height
            # Start monitoring strictly after the 10:00 entry bar.\n            path_prices = prices.loc[prices.index > entry_ts].copy()

            # Target detection uses executable exit prices at each minute close.
            pnl = pd.Series(0.0, index=path_prices.index)
            for strike, sign in legs:
                adjustment = cost_config.slippage_points_per_leg
                exit_exec = path_prices[strike] - adjustment if sign == 1 else path_prices[strike] + adjustment
                pnl += sign * (exit_exec - entry_exec[strike])

            # Early exit: at any time before expiry day, if live P&L is
            # close to the expiry-payoff flatline, exit immediately.
            # There is NO requirement that the trade first enters the bump.
            # This condition is evaluated from the first post-entry bar.
            pre_expiry_pnl = pnl[pnl.index.date < expiry]
            if bump_height > 0 and not pre_expiry_pnl.empty:
                return_band = pre_expiry_pnl[
                    (pre_expiry_pnl >= (flatline - tolerance_points)) &
                    (pre_expiry_pnl <= (flatline + tolerance_points))
                ]
            else:
                return_band = pd.Series(dtype=float)

            if not return_band.empty:
                exit_ts = return_band.index[0]
                exit_reason = "flatline_proximity"
            else:
                expiry_rows = path_prices[path_prices.index.date == expiry]
                if expiry_rows.empty:
                    continue
                exit_ts = expiry_rows.index[-1]
                exit_reason = "expiry"

            xp = {k: float(path_prices.loc[exit_ts, k]) for k in leg_strikes}
            exit_exec = {}
            for strike, sign in legs:
                adjustment = cost_config.slippage_points_per_leg
                exit_exec[strike] = xp[strike] - adjustment if sign == 1 else xp[strike] + adjustment
            gross_points = float(pnl.loc[exit_ts])

            effective_lot_size = historical_nifty_lot_size(expiry) if lot_size in (None, 0) else lot_size
            cost_rupees = 0.0
            if effective_lot_size is not None:
                dated_cfg = CostConfig(
                brokerage_per_order=cost_config.brokerage_per_order,
                stt_on_sell_premium_rate=historical_stt_rate(exit_ts.date()),
                exchange_turnover_rate=cost_config.exchange_turnover_rate,
                sebi_turnover_rate=cost_config.sebi_turnover_rate,
                stamp_duty_on_buy_premium_rate=cost_config.stamp_duty_on_buy_premium_rate,
                gst_rate=cost_config.gst_rate,
                slippage_points_per_leg=cost_config.slippage_points_per_leg,
            )
            cost_rupees = _turnover_and_costs(entry_exec, exit_exec, legs, effective_lot_size, dated_cfg)
            net_points = gross_points - (cost_rupees / effective_lot_size if effective_lot_size else 0.0)

            trades.append({
                "strategy": strategy.name,
                "option_type": strategy.option_type,
                "entry_date": entry_date.isoformat(),
                "expiry": expiry.isoformat(),
                "entry_timestamp": entry_ts.isoformat(),
                "exit_timestamp": exit_ts.isoformat(),
                "exit_reason": exit_reason,
                "spot_10am": float(spot_map[entry_date]),
                "atm": atm,
                "k4": leg_strikes[0],
                "k5": leg_strikes[1],
                "k6": leg_strikes[2],
                "strike_spacing": strategy.strike_spacing(legs),
                "entry_cashflow_points": strategy.entry_cashflow(ep, legs),
                "flatline_points": strategy.flatline_points(ep, legs),
                "max_profit_points": max_profit,
                "flatline_tolerance_fraction": flatline_tolerance,
                "flatline_tolerance_points": tolerance_points,
                "gross_pnl_points": gross_points,
                "net_pnl_points": net_points,
                "gross_pnl_rupees": gross_points * effective_lot_size,
                "net_pnl_rupees": net_points * effective_lot_size,
                "cost_rupees": cost_rupees,
                "lot_size": effective_lot_size,
                "holding_minutes": int((exit_ts - entry_ts).total_seconds() // 60),
                "data_file": str(path),
            })

    return pd.DataFrame(trades)


def write_summary(trades: pd.DataFrame, out_json: Path) -> None:
    if trades.empty:
        payload = {"trades": 0}
    else:
        payload = {
            "trades": int(len(trades)),
            "win_rate_gross": float((trades["gross_pnl_points"] > 0).mean()),
            "mean_gross_pnl_points": float(trades["gross_pnl_points"].mean()),
            "median_gross_pnl_points": float(trades["gross_pnl_points"].median()),
            "sum_gross_pnl_points": float(trades["gross_pnl_points"].sum()),
            "target_hit_rate": float((trades["exit_reason"] == "profit_target").mean()),
            "expiry_exit_rate": float((trades["exit_reason"] == "expiry").mean()),
            "max_loss_points": float(trades["gross_pnl_points"].min()),
            "max_win_points": float(trades["gross_pnl_points"].max()),
        }
    out_json.write_text(json.dumps(payload, indent=2))
