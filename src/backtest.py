from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
import json

import pandas as pd

from src.strategy import RatioStrategy


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
    target_fraction: float,
    lot_size: int | None,
    cost_config: CostConfig,
) -> pd.DataFrame:
    strategy.validate()

    expiry_maps: list[tuple[Path, date, list[date]]] = []
    all_entries: set[date] = set()

    for path in option_files:
        df0 = _prepare(pd.read_parquet(path, columns=["trading_day", "expiry"]))
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

            max_profit = strategy.max_profit_points(ep, legs)
            target = strategy.target_points(ep, legs, target_fraction)

            if max_profit <= 0:
                target_hit = pd.Series(dtype=float)
            else:
                path_prices = prices.loc[entry_ts:].copy()
                entry_adj = {}
                for strike, sign in legs:
                    adjustment = cfg_slip = cost_config.slippage_points_per_leg
                    entry_adj[strike] = ep[strike] + (adjustment if sign == 1 else -adjustment)

                pnl = pd.Series(0.0, index=path_prices.index)
                for strike, sign in legs:
                    pnl += sign * (path_prices[strike] - entry_adj[strike])
                target_hit = pnl[pnl >= target]

            if not target_hit.empty:
                exit_ts = target_hit.index[0]
                exit_reason = "profit_target"
            else:
                path_prices = prices.loc[entry_ts:]
                expiry_rows = path_prices[path_prices.index.date == expiry]
                if expiry_rows.empty:
                    continue
                exit_ts = expiry_rows.index[-1]
                exit_reason = "expiry"
                pnl = pd.Series(0.0, index=path_prices.index)
                for strike, sign in legs:
                    pnl += sign * (path_prices[strike] - entry_adj[strike])

            xp = {k: float(path_prices.loc[exit_ts, k]) for k in leg_strikes}
            gross_points = float(pnl.loc[exit_ts])

            cost_rupees = 0.0
            if lot_size is not None:
                cost_rupees = _turnover_and_costs(ep, xp, legs, lot_size, cost_config)
            net_points = gross_points - (cost_rupees / lot_size if lot_size else 0.0)

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
                "target_points": target,
                "gross_pnl_points": gross_points,
                "net_pnl_points": net_points,
                "cost_rupees": cost_rupees,
                "lot_size": lot_size,
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
