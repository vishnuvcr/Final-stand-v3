# Final Stand v3 — Options Strategy Research

## Current status
**Research phases completed through Phase 7 with a usable empirical conclusion, subject to a documented data-coverage limitation.**

Active research branch: [phase-2-data-backtest](https://github.com/vishnuvcr/Final-stand-v3/tree/phase-2-data-backtest)

## User-confirmed strategy
- Strategy 1: buy OTM4 put; sell OTM5 put; sell OTM6 put.
- Strategy 2: buy OTM4 call; sell OTM5 call; sell OTM6 call.
- Entry: 10:00 IST, **4 trading sessions before Tuesday expiry**.
- Early exit: **at any time after entry, if live P&L is close to the expiry-payoff horizontal flatline**.
- No requirement to first move toward the profit bump.
- Otherwise exit on expiry.

## Empirical result
Reference case: 5% flatline tolerance, 0.05 option-point adverse slippage per leg, ₹10 brokerage/order and dated statutory costs.

| | Put ratio | Call ratio |
|---|---:|---:|
| Qualifying trades | 36 | 36 |
| Net P&L | ₹60,711.67 | ₹94,941.36 |
| Net win rate | 80.56% | 94.44% |
| Profit factor | 1.762 | 4.074 |
| Max drawdown | -₹29,116.18 | -₹25,810.14 |
| Worst trade | -₹23,264.52 | -₹25,810.14 |

The executed qualifying sample runs through the **26-May-2026 expiry**. Later-dated source files did not produce qualifying trades in the executed spot/option path, so later dates are excluded rather than treated as zero-return observations.

## Research documents
- [Complete manuscript](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/research/MANUSCRIPT.md)
- [Research plan](research/RESEARCH_PLAN.md)
- [Strategy definition](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/research/STRATEGY_DEFINITION.md)
- [Empirical results](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/research/results/PHASE2_PHASE6_RESULTS.md)
- [Statistical analysis](https://github.com/vishnuvcr/Final-stand-v3/blob/phase-2-data-backtest/research/results/STATISTICAL_ANALYSIS.md)
- [Status](research/STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Conversation log](research/CONVERSATION_LOG.md)

## Workflows
The phase workflows retain **manual run buttons**. They use HF_TOKEN and cache the selected 1-minute data. Automatic push-triggered reruns have been disabled after the empirical runs to prevent endless research execution.

## Main conclusion
Both structures were profitable in the executed historical sample under the stated assumptions, but the sample is too small and the data/execution limitations too material to treat that as validated future performance. The strategy's unbounded adverse tail and large observed losses remain central risk characteristics.
