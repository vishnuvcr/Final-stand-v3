# Strategy definition and payoff

## Position
For equal strike spacing d:

### Strategy 1 — Put ratio
Long the nearer OTM put K4; short the next farther OTM put K5; short the next farther OTM put K6, with K4 > K5 > K6.

Expiry P&L per underlying unit before entry premium:
- S >= K4: 0
- K5 <= S < K4: K4 - S
- K6 <= S < K5: K4 - K5 = d (maximum-profit plateau)
- S < K6: S - (K4 - 3d), which falls without bound as S falls.

### Strategy 2 — Call ratio
Long the nearer OTM call K4; short the next farther OTM call K5; short the next farther OTM call K6, with K4 < K5 < K6.

Expiry P&L per underlying unit before entry premium:
- S <= K4: 0
- K4 < S <= K5: S - K4
- K5 < S <= K6: K5 - K4 = d (maximum-profit plateau)
- S > K6: K4 + 3d - S, which falls without bound as S rises.

## Entry premium and flatline
Let entry cashflow be:

C0 = long premium - short premium(K5) - short premium(K6)

Then the all-options-out-of-the-money expiry flatline is -C0, and the maximum plateau P&L is d - C0.

Thus the bump height above the initial flatline is exactly d when strikes are equally spaced.

## Profit target
The user described exiting near the payoff-chart flatline/plateau. Because no exact threshold was specified, the research uses:
- 90% of theoretical maximum plateau P&L
- 95% of theoretical maximum plateau P&L
- 100% of theoretical maximum plateau P&L

The 95% case is the designated descriptive reference, not an optimized choice.

## DTE interpretation
NIFTY weekly expiry is currently Tuesday. NSE's transition circular introduced new weekly Tuesday contracts after the Thursday regime, with the first new Tuesday weekly expiry on 02-Sep-2025. Therefore the backtest will report:
1. Calendar-DTE mode: exactly 4 calendar days from entry date to expiry date.
2. Trading-session-DTE mode: exactly four future exchange sessions to expiry.

These are not mixed into one undisclosed sample. Calendar-DTE is the primary interpretation of the user's wording.

## Data and fill policy
When bid/ask is unavailable, use 1-minute OHLC data and a conservative, documented fill rule. Entry and exit decisions use only information timestamped at or after the decision time. No future bars are used for strike selection or target detection.
