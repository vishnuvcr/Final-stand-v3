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

Entry is at **10:00 IST, exactly 4 trading sessions before expiry**.

For a Tuesday weekly expiry:
- Wednesday = 4 DTE
- Thursday = 3 DTE
- Friday = 2 DTE
- Monday = 1 DTE
- Tuesday = expiry

Therefore the primary entry day for a Tuesday expiry is Wednesday.

## Payoff geometry

For equal strike spacing, the 1:-1:-1 ratio structure has a horizontal expiry-payoff flatline, a finite profit bump/plateau between the short strikes, and an unbounded adverse tail.

For the put structure, with K4 > K5 > K6:
- S >= K4: flatline
- K5 <= S < K4: rising profit segment
- K6 <= S < K5: maximum-profit plateau
- S < K6: adverse unbounded tail

For the call structure, the geometry is mirrored.

## Flatline value

Let the entry net premium cashflow be:

C0 = long premium - short premium(K5) - short premium(K6)

Then the expiry flatline P&L is:

Flatline = -C0

The maximum plateau P&L is:

MaxProfit = d - C0

The bump height above the flatline is therefore d for equally spaced strikes.

## Corrected early-exit rule

The user does **not** want the earlier 90/95/100% maximum-profit target.

The intended rule is:

> After entry, monitor the live marked P&L. If the P&L comes back close to the horizontal flatline P&L shown by the expiry payoff chart, exit before expiry. If this condition is not reached, exit at 0 DTE/expiry.

The exact meaning of "close to" is parameterized because the screenshot does not specify a numerical tolerance.

The backtest will report:
- 2% of bump height
- 5% of bump height
- 10% of bump height

For flatline F and bump height H = MaxProfit - F, the early-exit condition is:

abs(LivePnL - F) <= tolerance * H

The early exit is only eligible before expiry day. Once expiry day is reached, the expiry rule takes precedence.

This is a path-dependent exit and is distinct from taking profit near maximum profit.
