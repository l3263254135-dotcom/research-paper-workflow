---
name: workflow-orchestrator
description: Orchestrate an evidence-first research-paper project from positioning through analysis, drafting, independent review, submission preparation, and revision tracking.
---

# Workflow Orchestrator

Use this skill when a research project needs a durable, auditable workflow rather than a one-off prose edit. Treat the researcher as the scientific decision-maker and AI as a local production and checking system.

## Operating contract

1. Inspect the project before changing it. Preserve existing versions and never overwrite an artifact unless explicitly requested.
2. Create or update `task_plan.md`, `findings.md`, and `progress.md`; record inputs, hashes, commands, outputs, status, and unresolved blockers.
3. Route work through this order: positioning, evidence/data audit, analysis, figures, manuscript, cross-review, submission/revision. Do not generate an abstract from unverified results.
4. Use `BLOCKED` for missing inputs. Complete independent tasks and state exactly which claims are blocked.
5. Keep four provenance labels visible in project records: `ARTICLE-SUPPORTED`, `INTERNAL-BASELINE`, `OUR-DESIGN`, and `BLOCKED-SOURCE`.
6. Maintain the minimum closed loop: `data -> analysis_results.json -> figure -> claim -> draft -> review_round_1`.

## Required project records

Use `data/`, `figures/`, `runs/`, and `submission/` plus `claims.yaml`, `analysis_results.json`, `citations_todo.md`, and `ai_disclosure.md`. Keep prompt/model/time records in `runs/`; do not upload unpublished data without explicit authorization.

## Completion rule

Report completed evidence, expression-only changes, and blocked work separately. A polished manuscript with missing configuration, unsupported mechanisms, or inconsistent results remains `NOT_READY_FOR_SUBMISSION`.

