# Research Plan — OTM4/OTM5/OTM6 directional ratio structures

## Research question
For NIFTY weekly index options, what historical performance is produced by:
- Strategy 1: long OTM4 PE; short OTM5 PE; short OTM6 PE.
- Strategy 2: long OTM4 CE; short OTM5 CE; short OTM6 CE.
- Entry at 4 DTE, 10:00 IST.
- Exit when realized strategy P&L reaches a chosen fraction of the expiry payoff plateau, otherwise at 0 DTE/expiry.
- Costs and slippage included.

## Primary ambiguity assumptions
1. Underlying: NIFTY index options.
2. OTM strike convention: ATM is based on 10:00 underlying spot rounded to the listed NIFTY strike grid; OTM4/5/6 are the 4th/5th/6th available strikes OTM on the relevant side.
3. Expiry: nearest weekly expiry that is exactly 4 market DTE away at entry, using the historical exchange calendar.
4. Entry and exit fills: when bid/ask quotes are unavailable, use a documented conservative synthetic fill from intraday OHLC.
5. Target: test 90%, 95% and 100% of theoretical maximum/flatline profit because “close to flatline” is not a single number.
6. Expiry exit: use the last tradable price available before expiry close; reconcile with official settlement where available.
7. Lot size: use the historical exchange lot size for each trade date.
8. Costs: use a dated Paytm Money fee schedule plus statutory/exchange charges and a conservative slippage model; never assume today’s rates apply to all years.

## Phase 1 — Definition and literature/data-source review
- Formalize payoff algebra and the maximum-profit plateau.
- Verify NIFTY strike intervals, expiries, trading hours and lot-size history from authoritative NSE sources.
- Review research on ratio spreads, short-gamma exposure, implied volatility/skew, volatility risk premia and path-dependent exits.
- Inventory public, open, broker and paid intraday NIFTY option datasets, including licensing constraints.
Exit criterion: strategy parameters and data requirements frozen in the repo.

## Phase 2 — Data acquisition and validation
- Prefer exchange/broker-derived 1-minute option data covering all needed strikes and expiries.
- Search NSE/BSE archives, open-source GitHub datasets, Kaggle, Hugging Face and broker APIs.
- Cache data in partitioned Parquet/CSV where licensing allows.
- Validate timestamps, duplicate rows, missing bars, strike grids, expiry mapping and price sanity.
- Cross-check spot and option timestamps.
Exit criterion: contiguous, auditable test coverage.

## Phase 3 — Backtest engine
- Implement a deterministic event-driven Python backtester.
- At each eligible 4-DTE date, determine 10:00 ATM and OTM4/5/6 strikes.
- Mark the combined strategy each minute.
- Detect target crossing without future leakage.
- Apply conservative fills and the complete dated cost model.
- Unit-test payoff signs and expiry accounting.

## Phase 4 — Strategy 1
Run the PE structure and produce trade-level P&L, equity curve, drawdown, holding time, target-hit rate, expiry-loss rate and tail-risk statistics.

## Phase 5 — Strategy 2
Run the identical pipeline for the CE structure.

## Phase 6 — Robustness
Compare 90/95/100% targets, slippage assumptions, subperiods and regime/liquidity segments. Use confidence intervals/bootstrap and interpret multiple testing carefully.

## Phase 7 — Final manuscript
Mandatory outputs:
Abstract; research question and hypotheses; data/provenance; strategy/payoff derivation; methodology; cost/slippage model; statistical analysis; results; robustness; discussion; strengths/limitations; conclusion; future research; references; tables; charts; appendices; machine-readable trade log.

## Stop rule
Do not extend beyond Phase 7. If valid intraday data cannot be obtained, stop with a transparent feasibility result and reproducible acquisition specification rather than fabricating performance.