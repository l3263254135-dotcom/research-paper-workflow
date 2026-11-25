---
name: workflow-orchestrator
description: Orchestrate a dual-AI, evidence-first research-paper project from publishability through analysis, drafting, independent review, submission, revision, and communication.
---

# Workflow Orchestrator

Use this skill when a research project needs a durable, auditable workflow rather than a one-off prose edit. Treat the researcher as the scientific decision-maker and AI as a local production and checking system.

## Priority rule

Scientific question, evidence quality, and claim boundaries outrank prose polish and formatting. Report scientific quality and presentation quality as separate axes; never let one compensate for the other. Apply the [mentor decision protocol](../../references/mentor-review-loop.md#0-导师式科学判断) at Gates 0, 2, and 5 even without a supplied review. Reuse the project ledger; do not require duplicate records.

## Operating contract

1. Inspect the project before changing it. Preserve existing versions and never overwrite an artifact unless explicitly requested.
2. Create or update `task_plan.md`, `findings.md`, and `progress.md`; record inputs, hashes, commands, outputs, status, and unresolved blockers.
3. Default production order: scientific question -> data and methods -> verified core figures/tables and Results -> Introduction and significance -> Conclusion -> Abstract. Enter at the current stage and revisit upstream decisions only when a gap affects the claim. This is a work order, not the journal's section order. Cross-review and submission checks follow the draft.
4. Use `BLOCKED` for missing inputs. Complete independent tasks and state exactly which claims are blocked.
5. Keep provenance labels visible: `BOOK-SUPPORTED`, `ARTICLE-SUPPORTED`, `INTERNAL-BASELINE`, `OUR-DESIGN`, and `BLOCKED-SOURCE`.
6. Maintain the minimum closed loop: `data -> analysis_results.json -> figure -> claim -> draft -> review_round_1`.
7. Use Claude Code as the generator/integrator and Codex as the independent critic only when process isolation is verified. Otherwise label the review `NON-INDEPENDENT`.
8. Keep author decisions explicit for question, method, interpretation, authorship, AI disclosure, and submission.

## Stage gates

### Gate 0 — Publishability

Run `$research-positioning`. Benchmark the proposed increment against the closest primary work and strongest applicable baseline. Require a falsifiable question, target readers, and an observation that discriminates the leading hypothesis from a credible alternative, with comparable conditions and a result-to-decision plan. With only an idea, deliver provisional positioning and the smallest decision-changing test; do not create a findings-based draft or mark results verified.

### Gate 1 — Data and methods

Run `$ai-research-production` and `$evidence-data-audit`. Write a data and methods record before running new analysis: sources, sample or experiment units, comparison, estimand, missing-data rules, uncertainty, and sensitivity checks. Keep planned methods separate from executed methods; the latter must match the actual scripts and run configuration. Require project configuration, data boundaries, source hashes, and an input -> script -> result -> figure -> claim ledger.

### Gate 2 — Analysis and visual argument

Run `$analysis-build`, `$figure-argument`, and `$figure-optimization`. Calibrate the method on a known case and a fair baseline where relevant. Arrange verified figures and tables as answers to successive subquestions, with an explicit connection between each pair. Use the [gap triage](../figure-argument/SKILL.md#when-the-core-sequence-breaks) before drafting: plot verified evidence that is missing from the display, return to Gates 1-2 for missing analysis, or revisit Gate 0 and narrow or withdraw a claim the design cannot support. Require reproducible results, uncertainty, figure-to-result links, and no silent replacement of missing values.

### Gate 3 — Manuscript reconstruction

If `manuscript_mode: reconstruction` is explicitly selected and a real source manuscript is provided, run `$manuscript-reconstruction` in R1 mode before `$manuscript-builder`. A scaffold placeholder is not a source. Require a fact ledger, story spine, section map, figure sequence, rewrite decision log, and `AWAITING_AUTHOR_APPROVAL`. After the author sets `reconstruction_approval: approved`, run R2 and require fact-preservation and story-traceability checks before recording `status: READY_FOR_REVIEW` in `reconstruction_status.yaml`.

In standard mode, continue with the standard manuscript path and write `draft.md`.

### Gate 4 — Manuscript

Run `$manuscript-builder`. Use the as-run methods and approved figure sequence to establish Results and Discussion. Then write Introduction and significance against what those results actually answer, followed by Conclusion and Abstract. Require a traceable outline, verified claims, and consistent evidence strength across the manuscript.

### Gate 5 — Independent pressure test

Run [`cross-review`](../cross-review/SKILL.md), which owns `claim_calibration.md`. Lead with the strongest fair counterexample and record which result would change the title or the evidential ceiling. Keep a verified finding if only its mechanism fails; withdraw it if the same-definition evidence overturns it. Recheck dependent panels, abstract, conclusions, and submission metadata. Require location-specific findings, revision logs, and author decisions for disagreements. Before review, run `python3 <plugin-root>/scripts/build_workflow_report.py <project> --stage review` with the [local record contract](../../references/readiness-records.md).

### Gate 6 — Submission and revision

Run [`submission-revision`](../submission-revision/SKILL.md). Require current official journal rules, consistent versioned files, authorship/ethics/AI records, and a complete response matrix for revisions. Run the report again with `--stage submission`; verified local records do not authorize external submission.

### Gate 7 — Communication (optional)

Run `$science-communication` only after claim calibration. Adapt audience and format without increasing claim strength.

## Required project records

Use `data/`, `figures/`, `runs/`, and `submission/` plus `claims.yaml`, `analysis_results.json`, `citations_todo.md`, `ai_disclosure.md`, `project_manifest.yaml`, `positioning.yaml`, `figure_manifest.yaml`, `figure_plan.yaml`, `figure_storyboard.md`, `section_traceability.md`, and, when reconstructing, `manuscript_source.md`, `fact_ledger.yaml`, `story_spine.yaml`, `section_map.yaml`, and `reconstruction_status.yaml`. Keep prompt/model/time records in `runs/`; do not upload unpublished data without explicit authorization.

## Completion rule

Report completed evidence, expression-only changes, and blocked work separately. A polished manuscript with missing configuration, unsupported mechanisms, or inconsistent results remains `NOT_READY_FOR_SUBMISSION`.
