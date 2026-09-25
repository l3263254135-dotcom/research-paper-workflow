---
name: workflow-orchestrator
description: Orchestrate a dual-AI, evidence-first research-paper project from publishability through analysis, drafting, independent review, submission, revision, and communication.
---

# Workflow Orchestrator

Use this skill when a research project needs a durable, auditable workflow rather than a one-off prose edit. Treat the researcher as the scientific decision-maker and AI as a local production and checking system.

## Priority rule

Scientific question, evidence quality, and claim boundaries outrank prose polish and formatting. Report scientific quality and presentation quality as separate axes; never let one compensate for the other.

## Operating contract

1. Inspect the project before changing it. Preserve existing versions and never overwrite an artifact unless explicitly requested.
2. Create or update `task_plan.md`, `findings.md`, and `progress.md`; record inputs, hashes, commands, outputs, status, and unresolved blockers.
3. Route work through this order: publishability, project harness, evidence/data audit, analysis, figure optimization and audit, manuscript reconstruction or standard manuscript build, cross-review, submission/revision, optional communication. Do not generate an abstract from unverified results.
4. Use `BLOCKED` for missing inputs. Complete independent tasks and state exactly which claims are blocked.
5. Keep provenance labels visible: `BOOK-SUPPORTED`, `ARTICLE-SUPPORTED`, `INTERNAL-BASELINE`, `OUR-DESIGN`, and `BLOCKED-SOURCE`.
6. Maintain the minimum closed loop: `data -> analysis_results.json -> figure -> claim -> draft -> review_round_1`.
7. Use Claude Code as the generator/integrator and Codex as the independent critic only when process isolation is verified. Otherwise label the review `NON-INDEPENDENT`.
8. Keep author decisions explicit for question, method, interpretation, authorship, AI disclosure, and submission.

## Stage gates

### Gate 0 — Publishability

Run `$research-positioning`. Require a falsifiable question, primary and alternative hypotheses, target readers, a verified gap, a provisional title, and sprint/match/safe journal options.

### Gate 1 — Evidence contract

Run `$ai-research-production` and `$evidence-data-audit`. Require project configuration, data boundaries, source hashes, a methods record, and an input -> script -> result -> figure -> claim ledger.

### Gate 2 — Analysis and visual argument

Run `$analysis-build`, `$figure-optimization`, and `$figure-argument`. Require reproducible result records, explicit uncertainty, a figure plan, reader-question and claim links, figure-to-result links, and no silent replacement of missing values.

### Gate 3 — Manuscript reconstruction

If `manuscript_source.md` exists, run `$manuscript-reconstruction` in R1 mode before `$manuscript-builder`. Require a fact ledger, story spine, section map, figure sequence, rewrite decision log, and `AWAITING_AUTHOR_APPROVAL`. After the author sets `reconstruction_approval: approved`, run R2 and require fact-preservation and story-traceability checks.

If `manuscript_source.md` does not exist, continue with the standard manuscript path.

### Gate 4 — Manuscript

Run `$manuscript-builder`. Require approved outline, verified claims, traceable numbers, calibrated language, and consistent evidence strength across title, abstract, figures, discussion, and conclusion.

### Gate 5 — Independent pressure test

Run `$cross-review` and `$claim-calibration`. Require location-specific findings, repair actions, claim support levels, revision logs, and author decisions for disagreements.

### Gate 6 — Submission and revision

Run `$submission-revision`. Require current official journal rules, consistent versioned files, authorship/ethics/AI records, and a complete response matrix for revisions.

### Gate 7 — Communication (optional)

Run `$science-communication` only after claim calibration. Adapt audience and format without increasing claim strength.

## Required project records

Use `data/`, `figures/`, `runs/`, and `submission/` plus `claims.yaml`, `analysis_results.json`, `citations_todo.md`, `ai_disclosure.md`, `project_manifest.yaml`, `positioning.yaml`, `figure_manifest.yaml`, `figure_plan.yaml`, `figure_storyboard.md`, `section_traceability.md`, and, when reconstructing, `manuscript_source.md`, `fact_ledger.yaml`, `story_spine.yaml`, `section_map.yaml`, and `reconstruction_status.yaml`. Keep prompt/model/time records in `runs/`; do not upload unpublished data without explicit authorization.

## Completion rule

Report completed evidence, expression-only changes, and blocked work separately. A polished manuscript with missing configuration, unsupported mechanisms, or inconsistent results remains `NOT_READY_FOR_SUBMISSION`.
