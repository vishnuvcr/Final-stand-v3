# Final Stand v3 — Options Strategy Research

## Current status
- Repository baseline initialized on 2026-10-01.
- Research phase: Phase 1 complete; Phase 2 ready to start.
- Test requested: two 1:-1:-1 OTM ratio structures, entered at 4 DTE at 10:00 IST, with early exit near the payoff-chart maximum-profit plateau and expiry otherwise.
- Working market assumption: NIFTY weekly index options, with OTM4/5/6 interpreted as the 4th/5th/6th listed OTM strikes from ATM. This is an explicit research assumption because the underlying was not specified.
- A 1-minute NIFTY options data source has been selected for Phase 2; raw licensed data will be downloaded and cached in GitHub Actions rather than committed to this public repo.

## Research files
- research/RESEARCH_PLAN.md
- RESEARCH_RULES.md
- research/STATUS.md
- research/ERROR_LOG.md
- research/CONVERSATION_LOG.md

## Phases
1. Strategy definition and data validation — complete
2. Data acquisition and quality validation — ready to start
3. Backtest engine and transaction-cost model — pending
4. Strategy 1 backtest — pending
5. Strategy 2 backtest — pending
6. Robustness / sensitivity analysis — pending
7. Manuscript, charts, appendices, and final conclusions — pending

## Important caveat
The requested 10:00 entry and intraday profit-target exit require intraday option prices for the exact strikes in each historical trade. Daily NSE bhavcopy data alone is insufficient.

## Source note
NSE publishes official derivatives reports including historical F&O bhavcopy files, but the public daily bhavcopy is end-of-day and cannot reproduce the requested intraday exit path.
## Phase 1 result
The strategy definition is frozen. The payoff has a maximum-profit plateau between the two short strikes and an unbounded adverse tail. The 4-DTE definition will be evaluated separately for the historical Thursday-expiry regime and the Tuesday-expiry regime.
