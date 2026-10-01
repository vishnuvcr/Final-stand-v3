# Research status

| Phase | Status | Latest update |
|---|---|---|
| 1. Definition + data-source validation | COMPLETE / CORRECTED | Four-session DTE and return-to-flatline exit frozen from user clarification |
| 2. Data acquisition + validation | IN PROGRESS | Acquisition script and manual GitHub Actions workflow implemented; local runtime cannot fetch external parquet data |
| 3. Backtest engine + costs | NOT STARTED | |
| 4. Strategy 1 | NOT STARTED | |
| 5. Strategy 2 | NOT STARTED | |
| 6. Robustness | NOT STARTED | |
| 7. Manuscript | NOT STARTED | |

## Latest findings
- With equal strike spacing, the 1:-1:-1 structure has a finite expiry maximum-profit plateau between the two short strikes.
- “Close to the flatline” is threshold-dependent; 90%, 95% and 100% of theoretical plateau profit are designated sensitivity cases.
- Minute-level option data is required for the requested early-exit rule.
## Phase 1 completion note
NSE confirms current NIFTY weekly expiry is Tuesday and the 2025 transition must be treated separately from earlier Thursday expiries. Target thresholds are frozen at 90%, 95% and 100% of theoretical maximum profit.

## Phase 2 current state
The reproducible acquisition/backtest workflow is implemented. No empirical trade results are claimed yet because the current execution environment cannot download the licensed parquet dataset or dispatch the repository workflow.

## Latest correction
Primary entry is four trading sessions before expiry. Early exit is the first flatline-proximity hit at any time after entry and before expiry day; no prior bump movement is required. No early exit is permitted on expiry day.

## Latest correction
The prior-bump requirement was removed. The event engine now scans from the first post-entry bar for the flatline-proximity condition.
