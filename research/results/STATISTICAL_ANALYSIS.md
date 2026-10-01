# Statistical analysis — reference 5% tolerance

## Sample
36 paired qualifying expiries/trades were available for each strategy in the executed dataset.

## Bootstrap
A nonparametric bootstrap with 200,000 resamples was applied to the trade-level net P&L.

| Statistic | Put ratio | Call ratio |
|---|---:|---:|
| Mean net P&L/trade | ₹1,686.44 | ₹2,637.26 |
| 95% bootstrap CI for mean | -₹1,223.75 to ₹4,427.21 | ₹488.43 to ₹4,375.33 |
| Median net P&L/trade | ₹1,785.07 | ₹2,871.44 |
| 95% bootstrap CI for median | ₹1,056.54 to ₹3,694.67 | ₹1,634.55 to ₹3,694.71 |
| Net win-rate | 80.56% | 94.44% |
| Wilson 95% CI for win-rate | 64.97%–90.25% | 81.86%–98.46% |

## Paired comparison

For each qualifying expiry, call-strategy net P&L minus put-strategy net P&L was calculated.

- Mean paired difference: **₹950.82 per trade**.
- 95% bootstrap CI: **-₹2,560.10 to ₹4,278.95**.
- Median paired difference: **₹112.94**.
- 20 of 36 paired trades had a positive call-minus-put difference (55.56%).
- Two-sided Wilcoxon signed-rank test: p = **0.681**.

The paired sample therefore does not provide strong statistical evidence that the observed mean difference generalizes beyond this historical sample.

## Interpretation

The raw sample statistics are materially positive for both structures under the reference assumptions, but the uncertainty around the mean is wide, especially for the put ratio. The observed results should not be converted into an expected future return without out-of-sample validation.

The largest source of statistical risk is the small number of independent trades (36) and the extreme tail losses. Trade observations are also not guaranteed to be independent because market regimes persist across adjacent expiries.

## Limitations
- No historical bid/ask surface.
- Fixed slippage is a proxy, not quote-level execution.
- Incomplete executed source coverage after 26-May-2026.
- No independent out-of-sample period in this phase.
- Parameter sensitivity was tested, but the tolerance was not pre-registered externally.
