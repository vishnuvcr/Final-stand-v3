# Research status

| Phase | Status | Latest update |
|---|---|---|
| 1. Definition + data-source validation | COMPLETE | Payoff, DTE regimes, data sources and cost-model requirements frozen |
| 2. Data acquisition + validation | IN PROGRESS | HF acquisition, caching, synthetic tests and manual workflow implemented; empirical run still pending |
| 3. Backtest engine + costs | IMPLEMENTED / VALIDATION PENDING | Event-driven engine with slippage and cost hooks is on phase-2-data-backtest |
| 4. Strategy 1 | NOT STARTED | |
| 5. Strategy 2 | NOT STARTED | |
| 6. Robustness | NOT STARTED | |
| 7. Manuscript | NOT STARTED | |

## Current result
No numeric historical performance is claimed yet. The current runtime cannot execute the licensed parquet download or dispatch GitHub Actions.

## Phase 1 findings
- Equal-spaced 1:-1:-1 ratio structures have a maximum-profit plateau between the two short strikes.
- The adverse tail is unbounded.
- Target threshold is parameterized rather than silently chosen.
- NIFTY weekly expiry changed from Thursday to Tuesday in 2025; DTE regimes are handled separately.
