# Phase 1 findings

## Completed
1. Repository baseline and governance files created.
2. Strategy ambiguity converted into explicit parameters.
3. User clarified DTE: four trading sessions, not four calendar days.
4. For Tuesday expiry, entry is Wednesday at 10:00 IST.
5. User supplied payoff screenshots confirming the horizontal flatline / bump structure.
6. User clarified that early exit does **not** require prior movement into the bump.
7. Early exit is simply the first time before expiry day that live P&L is sufficiently close to the expiry-payoff flatline.
8. Intraday option data requirement confirmed.
9. Candidate 1-minute data sources inventoried.
10. Broker and statutory cost sources inventoried.

## Superseded interpretations
- Four-calendar-day DTE: superseded.
- Exit only after entering the bump and reverting: superseded.
- Maximum-profit percentage target: superseded.

## Current tolerance
Test 2%, 5%, and 10% of bump height around the calculated flatline.

## Phase 1 exit criterion
The corrected strategy definition is frozen sufficiently to continue Phase 2.
