# Phase 1 findings

## Completed
1. Repository baseline and governance files created.
2. Strategy ambiguity converted into explicit parameters.
3. User clarified DTE: **4 trading sessions**, not calendar days.
4. For Tuesday expiry, entry is Wednesday at 10:00 IST.
5. User supplied the intended payoff-chart structure.
6. Early exit is based on P&L proximity to the horizontal expiry-payoff flatline, not proximity to maximum profit.
7. Intraday option data requirement confirmed.
8. Candidate 1-minute data sources inventoried.
9. Broker and statutory cost sources inventoried.

## Corrections to the previous interpretation

The previous four-calendar-day interpretation was incorrect for this requested strategy and is superseded by four trading sessions.

The previous 90/95/100%-of-maximum-profit exit rule is also superseded.

The current exit rule is proximity to the payoff flatline.

## Tolerance

Because "close to" has no numerical threshold in the screenshot, test:
- 2% of bump height
- 5% of bump height
- 10% of bump height

The 5% case is the descriptive reference.

## Phase 1 exit criterion

The corrected strategy definition is frozen sufficiently to continue Phase 2.
