# Final Stand v3 — Options Strategy Research

## Current status
- Active phase: Phase 2 — data acquisition and backtest implementation.
- Phase 1 definition is complete and frozen.
- Numeric historical performance is **not yet reported** because the current runtime cannot download/read the selected licensed parquet dataset and cannot dispatch the repository's GitHub Actions workflow.
- No empirical result has been fabricated.

## Active phase branch
[phase-2-data-backtest](https://github.com/vishnuvcr/Final-stand-v3/tree/phase-2-data-backtest)

Key active files:
- [Research plan](research/RESEARCH_PLAN.md)
- [Phase 2 findings](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/research/PHASE_2_FINDINGS.md)
- [Data specification](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/research/PHASE_2_DATA_SPEC.md)
- [Strategy definition](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/research/STRATEGY_DEFINITION.md)
- [Data-source review](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/research/DATA_SOURCE_REVIEW.md)
- [Error log](research/ERROR_LOG.md)
- [Conversation log](research/CONVERSATION_LOG.md)
- [Phase 2 workflow](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/.github/workflows/phase-2-backtest.yml)

## Strategy test definition
1. Long OTM4 put, short OTM5 put, short OTM6 put.
2. Long OTM4 call, short OTM5 call, short OTM6 call.
3. Entry at 4 DTE, 10:00 IST.
4. Exit when realized P&L reaches 90%, 95% or 100% of the theoretical maximum plateau, with 95% as the descriptive reference.
5. Otherwise exit at 0 DTE/expiry.
6. Execution costs and adverse slippage are explicit inputs.

## Working market assumption
Because the underlying was not specified, the implementation assumes NIFTY weekly index options. OTM4/5/6 means the 4th/5th/6th listed OTM strikes from the 10:00 ATM reference.

## Phase structure
1. Strategy definition and data validation — complete.
2. Data acquisition and quality validation — in progress.
3. Backtest engine and transaction-cost model — implemented on active Phase 2 branch; empirical completion pending data run.
4. Strategy 1 backtest — pending.
5. Strategy 2 backtest — pending.
6. Robustness / sensitivity analysis — pending.
7. Manuscript, charts, appendices, and final conclusions — pending.
