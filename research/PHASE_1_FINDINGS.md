# Phase 1 findings

## Completed
1. Repository baseline and governance files created.
2. Strategy ambiguity converted into explicit parameters.
3. Expiry regime verified from NSE.
4. Payoff algebra formalized.
5. Intraday-data requirement confirmed.
6. Candidate 1-minute data sources inventoried.
7. Broker and statutory cost sources inventoried.

## Critical methodological findings
- The payoff has a finite maximum-profit plateau between the two short strikes, with a tail loss that is unbounded in the adverse direction.
- The plateau profit before costs is strike spacing minus the net entry debit or credit.
- Close to the flatline is not a unique numerical trigger; 90%, 95% and 100% of the theoretical plateau are frozen sensitivity cases.
- The user's 4 DTE rule cannot be applied identically across NIFTY's historical Thursday and current Tuesday weekly-expiry regimes without changing what DTE means.
- Public intraday datasets located are OHLC-based and generally do not provide a historical bid/ask surface; execution assumptions must therefore be conservative.

## Phase 1 exit criterion
Definition, data requirements and cost-model requirements are sufficiently frozen to start Phase 2 implementation.
