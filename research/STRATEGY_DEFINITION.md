# Strategy definition and payoff

## User-confirmed strategy

### Strategy 1 — Put ratio
- Buy OTM4 put
- Sell OTM5 put
- Sell OTM6 put

### Strategy 2 — Call ratio
- Buy OTM4 call
- Sell OTM5 call
- Sell OTM6 call

OTM4/OTM5/OTM6 means the 4th, 5th and 6th OTM listed strikes from the 10:00 ATM reference.

## Entry

Entry is at 10:00 IST, exactly 4 trading sessions before expiry.

For a Tuesday weekly expiry:
Wednesday = 4 DTE -> Thursday = 3 DTE -> Friday = 2 DTE -> Monday = 1 DTE -> Tuesday = expiry.

## Payoff geometry

The 1:-1:-1 ratio structure has a horizontal expiry-payoff flatline, a finite profit bump/plateau between the short strikes, and an unbounded adverse tail.

## Flatline value

Let C0 be the net entry premium cashflow:

C0 = long premium - short premium(K5) - short premium(K6)

Expiry flatline P&L = -C0.

For equal strike spacing d:

MaxProfit = d - C0

Bump height = MaxProfit - Flatline = d.

## Correct early-exit rule

The user has clarified that the trade **does not need to move toward or into the bump first**.

At any time after entry and before expiry day:

1. Calculate current combined strategy P&L using executable/adverse-slippage marks.
2. Compare it directly with the expiry-payoff flatline.
3. If the live P&L is sufficiently close to the flatline, exit immediately.
4. The first qualifying timestamp is the exit.
5. If no qualifying timestamp occurs before expiry day, hold to expiry.

There is **no prior-profit, bump-entry, or reversion requirement**.

For flatline F and bump height H, with tolerance fraction T:

abs(LivePnL - F) <= T * H

The tolerance sensitivity remains:
- 2%
- 5%
- 10%

The 5% case is a descriptive reference, not an optimized historical choice.

## Expiry rule

The flatline-proximity early exit is not applied on expiry day. If no earlier qualifying timestamp exists, the position exits at the final tradable observation on expiry day.
