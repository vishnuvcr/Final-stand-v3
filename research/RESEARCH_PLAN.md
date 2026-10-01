# Research Plan — OTM4/OTM5/OTM6 directional ratio structures

## Research question
For NIFTY weekly index options, what historical performance is produced by:
- Strategy 1: long OTM4 PE; short OTM5 PE; short OTM6 PE.
- Strategy 2: long OTM4 CE; short OTM5 CE; short OTM6 CE.
- Entry at 10:00 IST exactly four trading sessions before expiry.
- Early exit when live P&L comes sufficiently close to the horizontal expiry-payoff flatline.
- Otherwise exit at expiry.
- Full transaction costs and adverse slippage included.

## Frozen interpretation

Primary DTE definition is **trading-session DTE**, not calendar DTE.

For a Tuesday expiry:
Wednesday 4 DTE -> Thursday 3 DTE -> Friday 2 DTE -> Monday 1 DTE -> Tuesday 0 DTE.

This is the user-confirmed interpretation.

The early exit is based on the live P&L returning close to the horizontal expiry-payoff flatline, not on reaching maximum profit.

Because "close to" is not numerically specified, use 2%, 5%, and 10% of bump height as tolerance sensitivity. The 5% case is the descriptive reference, not an optimized choice.

## Phase 1 — Strategy definition and data-source review
Complete:
- Payoff geometry
- Four-trading-session DTE
- Flatline-proximity exit concept
- Intraday data requirements
- Data-source inventory
- Cost-model requirements

## Phase 2 — Data acquisition and validation
- Download 1-minute NIFTY option and spot data.
- Validate timestamps, contracts, expiry mapping, strikes, missing bars and liquidity.
- Ensure every selected leg has a common 10:00 entry bar.
- Ensure minute-level data exists through the early-exit decision or expiry.
- Cache data in GitHub Actions using HF_TOKEN.
- Preserve provenance and hashes.

## Phase 3 — Backtest engine
- Select OTM4/5/6 using only 10:00 entry information.
- Enter all three legs simultaneously at 10:00.
- Calculate entry flatline and bump height.
- Monitor combined strategy P&L minute by minute.
- Trigger early exit when P&L enters the flatline tolerance band.
- Do not trigger the early-exit rule on expiry day.
- If no early exit occurs, exit at expiry.
- Apply brokerage, statutory charges and adverse slippage.

## Phase 4 — Strategy 1
Run the put ratio and report trade count, gross/net P&L, distribution, exit reasons, holding time, drawdown and tail losses.

## Phase 5 — Strategy 2
Run the identical pipeline for the call ratio.

## Phase 6 — Robustness
Test flatline tolerance, slippage, liquidity, volatility regime, trend/range regime, subperiods and expiry regimes without retrospectively selecting the best historical setting.

## Phase 7 — Final manuscript
Produce the complete research manuscript with abstract, literature review, data/provenance, strategy/payoff derivation, methodology, costs, statistical analysis, results, robustness, discussion, strengths/limitations, conclusion, future research, references, tables, charts, appendices and machine-readable trade supplement.

## Stop rule
Stop after Phase 7. If valid historical data cannot be obtained, report feasibility and the missing-data limitation rather than fabricating results.
