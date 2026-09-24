---
name: ai-research-production
description: Build a local, auditable dual-AI research environment with explicit roles, data boundaries, run logs, and file-based handoffs.
---

# AI Research Production

Use this skill before analysis or drafting when the project needs a durable AI harness rather than a one-off prompt.

## Required setup

- Create or update `CLAUDE.md`, `project_manifest.yaml`, `provenance.md`, `ai_disclosure.md`, and `runs/`.
- Record the research question, data sources, method constraints, target journal, article type, privacy boundary, and author decisions.
- Keep unpublished, clinical, proprietary, or otherwise restricted data local unless the author explicitly authorizes another destination.

## Dual-AI protocol

- Generator/integrator: builds scripts, records, figures, outlines, and drafts from explicit local inputs.
- Independent critic: reads only the approved evidence package and manuscript files, then writes review artifacts.
- Exchange information through visible files such as `draft.md`, `review_round_N.md`, and `claim_calibration.md`.
- Verify process isolation before calling the review independent. If isolation cannot be demonstrated, label the run `NON-INDEPENDENT`.

## Run record

Each run under `runs/` records UTC time, model/tool, prompt or command, inputs, outputs, status, and unresolved blockers. Do not hide scientific decisions in prompts; copy final decisions into project records.

## Acceptance

- Project configuration is complete enough for a new session to understand the question, data boundary, methods, and journal.
- Every AI-produced artifact has a visible source record.
- The author remains responsible for method selection, interpretation, authorship, disclosure, and submission.
