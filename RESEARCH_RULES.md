# Research rules

- Keep the detailed research plan in research/RESEARCH_PLAN.md.
- Update research/STATUS.md after every research step.
- Log every operational or methodological error in research/ERROR_LOG.md.
- Record user-facing conversation summaries in research/CONVERSATION_LOG.md; do not store hidden chain-of-thought.
- Preserve important raw/derived research data when licensing permits; otherwise store source metadata, hashes, schemas and reproducible acquisition instructions.
- Keep phase work separated by Git branch.
- Every phase workflow must be manually runnable.
- Include brokerage, statutory charges, transaction costs and slippage assumptions.
- Prefer primary sources for market rules and official data.
- Never silently change strike selection, expiry selection, entry time, exit rule or cost assumptions.
- Convert ambiguous terms into explicit parameters and sensitivity tests.
- Avoid look-ahead bias; strike selection must use only information available at entry.
- Stop after the predefined phases; do not expand scope indefinitely.