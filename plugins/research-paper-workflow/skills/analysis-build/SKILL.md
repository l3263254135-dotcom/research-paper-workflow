---
name: analysis-build
description: Turn an author-approved analysis plan into reproducible result records with explicit uncertainty, provenance, and negative-result handling.
---

# Analysis Build

Use after positioning and evidence audit. Do not choose a scientific method solely because an AI suggests it.

## Process

1. Read the approved question, hypotheses, data dictionary, and analysis plan.
2. Inspect scripts, environments, input hashes, masks, denominators, sample units, windows, and missingness.
3. Run or repair the analysis in a clean, reproducible environment.
4. Write `analysis_results.json` with one record per estimand or planned comparison.
5. Preserve null, reverse, failed, exploratory, and alternative analyses with explicit status.

## Required result fields

Each major result should include `result_id`, `variable`, `unit`, `region`, `season`, `contrast`, `window`, `n`, `estimate`, `ci_low`, `ci_high`, `test`, `p_exact`, `script_path`, `input_hash`, and `status`. Add effect-size or domain-specific fields when appropriate.

## Acceptance

- Verified results are finite and their intervals are ordered.
- Statistical objects match the question and sample unit.
- No missing value is replaced with zero without an explicit, documented rule.
- A clean rerun reproduces the recorded values within the declared tolerance.
- Missing configuration or data remains `BLOCKED`.
