---
name: manuscript-builder
description: Build or revise a scientific manuscript from verified result and claim records while preserving numbers, citations, uncertainty, and conclusion strength.
---

# Manuscript Builder

Draft only from verified `analysis_results.json`, `claims.yaml`, source records, and approved outlines. Keep claim, result, evidence, and figure IDs in the working draft until final human review.

## Structure

Use the target journal's article type. Unless its instructions require another order: Title, Key Points/Abstract, Introduction, Results, Discussion, Conclusions, Methods, Figures/Tables, References, Data/Code/AI disclosures.

## Rules

- Bind each quantitative sentence to estimate, interval, n, test, p/q, and source result.
- Separate direct observation, constrained inference, and unresolved mechanism.
- Preserve null, reverse, failed, and alternative results.
- Keep internal QA/version language out of scientific prose; retain it in audit files.
- Put unverified citations in `citations_todo.md`; never invent DOI, reference, method, or configuration.
- Keep figures, captions, tables, SI, abstract, and conclusion at the same evidence strength.

Before delivery, run numeric consistency checks and list residual blockers. A fluent draft is not submission-ready evidence.

