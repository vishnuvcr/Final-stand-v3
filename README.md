# Final Stand v3 — Options Strategy Research

## Current status
- Repository baseline initialized on 2026-10-01.
- Research phase: Strategy definition and data-source validation.
- Test requested: two 1:-1:-1 OTM ratio structures, entered at 4 DTE at 10:00 IST, with early exit near the payoff-chart maximum-profit plateau and expiry otherwise.
- Working market assumption: NIFTY weekly index options, with OTM4/5/6 interpreted as the 4th/5th/6th listed OTM strikes from ATM. This is an explicit research assumption because the underlying was not specified.
- Intraday option data availability is the current gating item.

## Research files
- research/RESEARCH_PLAN.md
- RESEARCH_RULES.md
- research/STATUS.md
- research/ERROR_LOG.md
- research/CONVERSATION_LOG.md

## Phases
1. Strategy definition and data validation — in progress
2. Data acquisition and quality validation — pending
3. Backtest engine and transaction-cost model — pending
4. Strategy 1 backtest — pending
5. Strategy 2 backtest — pending
6. Robustness / sensitivity analysis — pending
7. Manuscript, charts, appendices, and final conclusions — pending

## Important caveat
The requested 10:00 entry and intraday profit-target exit require intraday option prices for the exact strikes in each historical trade. Daily NSE bhavcopy data alone is insufficient.

## Source note
NSE publishes official derivatives reports including historical F&O bhavcopy files, but the public daily bhavcopy is end-of-day and cannot reproduce the requested intraday exit path.