---
name: evidence-data-audit
description: Audit research inputs, variables, units, windows, statistics, experiment configuration, figures, and claim provenance before manuscript drafting.
---

# Evidence and Data Audit

Inspect files, scripts, metadata, logs, and existing tables. Build an input -> script -> result -> figure -> claim ledger. Hash source files where possible.

## Check

- variable definitions, units, masks, denominators, sample units, seasons, windows, missingness, finite values, and sign convention;
- experimental case, branch/restart, forcing, spin-up, treatment implementation, and comparability;
- effect estimate, uncertainty, n, test, exact p, multiple-testing family, and sensitivity choices;
- figure/caption/text numbers and source links;
- unavailable material and the claims it blocks.

Use `scripts/validate_analysis_results.py`, `scripts/validate_claims.py`, and `scripts/check_numeric_consistency.py` when the corresponding files exist. Never replace missing values with zero or silently truncate a window.

## Status vocabulary

`verified` means the local source and execution record support the field; `exploratory` means the calculation is identified as such; `blocked` means a dependency is absent. Non-significance is not evidence of equivalence.

## P2 guardrails

Read `references/p2-domain-rules.md` for FLDS, Rnet, CICE, N_HEAT, OHC, budget, height-step, and configuration boundaries.

