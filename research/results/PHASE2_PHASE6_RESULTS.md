# Phase 2 / Phase 6 empirical results

## Tested sample

- Underlying: NIFTY weekly index options.
- Entry: 10:00 IST, exactly four trading sessions before expiry.
- Current Tuesday-expiry regime.
- First qualifying entry in the executed dataset: 03-Sep-2025.
- Last qualifying entry: 20-May-2026, for expiry 26-May-2026.
- Qualifying trades: 36 per strategy.
- The source contains later-dated files, but the executed NIFTY spot/option path produced no qualifying trades after 26-May-2026. This is treated as a data-coverage limitation, not as zero P&L.

## Execution model

- 1-minute OHLC marks.
- 0.05 option-point adverse slippage per leg for the reference case.
- Paytm Money brokerage: ₹10 per executed order.
- Historical NIFTY lot size: 75 through 30-Dec-2025; 65 from 06-Jan-2026.
- STT: date-dependent 0.10% before 01-Apr-2026 and 0.15% from 01-Apr-2026.
- Exchange turnover rate input: 0.0003553.
- SEBI turnover rate input: 0.000001.
- Stamp duty on option purchase premium: 0.00003.
- GST: 18%.

## Reference case — 5% flatline tolerance

| Metric | Strategy 1: put ratio | Strategy 2: call ratio |
|---|---:|---:|
| Trades | 36 | 36 |
| Net P&L | ₹60,711.67 | ₹94,941.36 |
| Mean net P&L/trade | ₹1,686.44 | ₹2,637.26 |
| Median net P&L/trade | ₹1,785.07 | ₹2,871.44 |
| Net win rate | 80.56% | 94.44% |
| Profit factor | 1.762 | 4.074 |
| Max drawdown | -₹29,116.18 | -₹25,810.14 |
| Worst trade | -₹23,264.52 | -₹25,810.14 |
| Best trade | ₹20,852.30 | ₹15,485.89 |
| Total estimated costs | ₹3,799.58 | ₹3,748.14 |
| Flatline exits | 44.44% | 55.56% |
| Expiry exits | 55.56% | 44.44% |

These are descriptive historical results for this sample and execution model; they are not a prediction of future performance.

## Flatline-tolerance robustness

### Strategy 1 — put ratio

| Tolerance | Net P&L | Win rate | Profit factor | Max DD | Flatline exits |
|---|---:|---:|---:|---:|---:|
| 2% | ₹63,025.61 | 80.56% | 1.791 | -₹29,116.18 | 11.11% |
| 5% | ₹60,711.67 | 80.56% | 1.762 | -₹29,116.18 | 44.44% |
| 10% | ₹57,864.12 | 80.56% | 1.726 | -₹29,116.18 | 47.22% |

### Strategy 2 — call ratio

| Tolerance | Net P&L | Win rate | Profit factor | Max DD | Flatline exits |
|---|---:|---:|---:|---:|---:|
| 2% | ₹85,885.02 | 91.67% | 3.277 | -₹25,810.14 | 30.56% |
| 5% | ₹94,941.36 | 94.44% | 4.074 | -₹25,810.14 | 55.56% |
| 10% | ₹88,042.15 | 94.44% | 3.851 | -₹25,810.14 | 75.00% |

The tolerance changes exit timing materially. It should therefore be treated as a strategy parameter requiring out-of-sample validation, not as a parameter to optimize on the same sample.

## Slippage robustness — 5% tolerance

| Slippage/leg | Put net P&L | Call net P&L |
|---:|---:|---:|
| 0.00 points | ₹61,356.48 | ₹93,592.27 |
| 0.05 points | ₹60,711.67 | ₹94,941.36 |
| 0.10 points | ₹60,233.32 | ₹94,303.57 |

Because slippage changes the flatline and live P&L path, the effect is not a simple constant subtraction.

## Important interpretation

The strategy's positive sample P&L comes with large adverse-tail observations. The maximum observed single-trade losses were about ₹23.3k for the put ratio and ₹25.8k for the call ratio under the reference execution model.

The early flatline exit is not equivalent to a conventional take-profit. It can occur very soon after entry if the live P&L lies inside the flatline tolerance band, exactly as specified by the user.

## Data limitation

The selected public dataset is licensed CC BY-NC 4.0 and provides 1-minute OHLCV/OI. It does not provide the full historical bid/ask surface used for exact execution reconstruction. The backtest therefore uses conservative fixed adverse slippage and should not be interpreted as a quote-level execution simulation.

The current empirical run produced qualifying trades only through the 26-May-2026 expiry. Later source files were not converted into qualifying trades in the executed spot/option sample, so the period after 26-May-2026 is excluded rather than treated as zero-return observations.

## Next research phase

Phase 7 should produce:
- equity/drawdown charts
- distribution charts
- exit-timing analysis
- regime segmentation
- data-coverage audit
- brokerage sensitivity
- statistical confidence intervals/bootstrap
- final manuscript and appendices
