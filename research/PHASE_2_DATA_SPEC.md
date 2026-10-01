# Phase 2 data specification

## Required fields
Spot: timestamp, trading_day, close.

Options: timestamp, trading_day, expiry, strike, option_type, close.

OHLCV and open interest are retained for liquidity and quality checks.

## Coverage requirement
For every eligible 4-DTE entry:
- all three selected option contracts must have a 10:00 bar;
- all three must have a common timestamp path through the exit;
- the expiry-day path must contain a final tradable observation;
- the corresponding 10:00 spot observation must exist.

## Validation checks
- duplicate timestamp/contract rows
- non-monotone timestamps
- missing 10:00 bars
- missing leg bars
- negative prices
- strike ordering
- expiry-date consistency
- stale or zero-volume bars
- spot timestamp alignment
- outlier prices

## Execution limitation
The public source exposes OHLC rather than historical bid/ask. Phase 2 must therefore report close-based marks plus explicit adverse-slippage sensitivity.

Raw licensed parquet files are not committed to this public repository. GitHub Actions will download and cache them, while manifests record the source and selected files.
