# Phase 2 findings to date

## Implemented
- Hugging Face acquisition script using HF_TOKEN.
- Cached download design for NIFTY 1-minute spot and expiry parquet files.
- Event-driven minute-close backtest for both ratio structures.
- 4-calendar-DTE and 4-session-DTE modes.
- 90/95/100 percent target parameterization.
- Entry and exit adverse-slippage model.
- Brokerage, STT, exchange, SEBI, stamp duty and GST cost hooks.
- Synthetic payoff and target-hit tests.

## Empirical status
No historical performance table is reported yet. The current model runtime cannot resolve external download hosts and cannot read parquet locally because PyArrow is unavailable. GitHub Actions is the reproducible execution path because the repository workflow can use the user's HF_TOKEN secret and cache the selected dataset files.

## Data/licensing handling
The selected Hugging Face dataset is CC BY-NC 4.0 and is therefore not copied into this public GitHub repository. The workflow caches it for execution and records provenance in a manifest.

## Next exit criterion
A successful manual Phase 2 workflow run must produce non-empty, validated trade-level files for both strategies and preserve the workflow artifact before Phase 3 can be marked complete.
