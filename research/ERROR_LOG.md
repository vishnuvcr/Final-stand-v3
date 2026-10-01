# Error log

| Date | Step | Error / issue | Impact | Corrective action |
|---|---|---|---|---|
| 2026-10-01 | Repository inspection | Repository was empty; no prior research files, branches or results existed | No historical project state available to inherit | Initialized governance, plan, status and conversation-log files on main |
| 2026-10-01 | Data acquisition | NSE public derivatives pages expose official historical reports, but daily bhavcopy is not enough for intraday option P&L path testing | Daily-only data cannot reproduce the requested early exit | Search for minute-level datasets/APIs and document provenance/licensing before backtest |
| 2026-10-01 | Phase 1 DTE review | NIFTY weekly expiry changed from Thursday to Tuesday in 2025; a single undifferentiated 4-DTE sample would change the meaning of the rule | Historical comparison could become invalid | Freeze calendar-DTE as primary and keep trading-session-DTE as a separately reported sensitivity; do not merge regimes silently |

| 2026-10-01 | Phase 2 local execution | Container could not resolve external hosts, and the local Python environment lacks PyArrow, so licensed parquet data could not be downloaded/read here | Full empirical backtest cannot be executed in this runtime | Added HF-token GitHub Actions acquisition with cache, added parquet/engine smoke tests, logged the limitation, and kept the workflow fail-closed on missing cost rates |

| 2026-10-01 | Strategy-definition correction | Previous implementation treated 4 DTE as four calendar days and targeted a fraction of maximum profit | This did not match the user's intended Wednesday entry for Tuesday expiry or the uploaded payoff-chart exit concept | Replaced with four-trading-session DTE and return-to-flatline exit; added tolerance sensitivity and regression test |

| 2026-10-01 | Flatline-exit correction | Previous engine required the P&L to first move into the bump before a flatline exit | That was not part of the user's rule | Removed the prior-bump requirement; the first flatline-proximity hit at any time before expiry day is now the exit |
