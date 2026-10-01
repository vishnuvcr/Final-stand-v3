# Research Plan — OTM4/OTM5/OTM6 directional ratio structures

## Research question
For NIFTY weekly index options, what historical performance is produced by:
- Strategy 1: long OTM4 PE; short OTM5 PE; short OTM6 PE.
- Strategy 2: long OTM4 CE; short OTM5 CE; short OTM6 CE.
- Entry at 10:00 IST exactly four trading sessions before expiry.
- Early exit whenever live P&L is sufficiently close to the horizontal expiry-payoff flatline.
- Otherwise exit at expiry.
- Full transaction costs and adverse slippage included.

## Frozen interpretation

### DTE
Primary DTE definition is trading-session DTE.

For a Tuesday expiry:
Wednesday 4 DTE -> Thursday 3 DTE -> Friday 2 DTE -> Monday 1 DTE -> Tuesday 0 DTE.

### Early exit
The uploaded payoff screenshots establish the intended horizontal flatline and profit bump.

The corrected rule is:

> At ANY time after entry and before expiry day, if the live combined position P&L is close enough to the expiry-payoff flatline, exit immediately.

The trade does **not** have to previously move into the bump or show a prior profit excursion.

Tolerance is parameterized at 2%, 5%, and 10% of bump height. The 5% case is the descriptive reference.

### Phase 1
Complete:
- payoff geometry
- user-confirmed DTE
- user-confirmed flatline-proximity exit
- intraday data requirements
- data-source inventory
- cost-model requirements

### Phase 2
- Acquire and validate 1-minute NIFTY option and spot data.
- Ensure every selected leg has a common 10:00 entry bar.
- Monitor combined executable P&L minute by minute from the first post-entry bar.
- Test flatline-proximity exit immediately from the first post-entry bar.
- Exclude expiry day from the early-exit scan.
- If no early exit occurs, use final expiry-day observation.
- Apply dated brokerage/statutory charges and adverse slippage.

### Phase 3
Validate the deterministic event-driven engine and execution-cost model.

### Phase 4
Run Strategy 1 and report full trade-level and aggregate statistics.

### Phase 5
Run Strategy 2 with the identical pipeline.

### Phase 6
Robustness:
- 2%, 5%, 10% flatline tolerance
- slippage sensitivity
- liquidity filters
- volatility and regime segmentation
- subperiods
- historical expiry regimes where the four-session definition is applicable

### Phase 7
Prepare the complete research manuscript with tables, charts, appendices, references and machine-readable trade supplement.

## Stop rule
Stop after Phase 7. If valid historical data cannot be obtained, report the feasibility limitation rather than inventing performance.
