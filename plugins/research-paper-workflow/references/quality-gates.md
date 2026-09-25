# Workflow Quality Gates

## Gate 0 — Publishability

- falsifiable question;
- verified knowledge gap;
- primary and alternative hypotheses;
- audience and journal fit;
- minimum publishable unit decision;
- title no stronger than the evidence.

## Gate 1 — Evidence contract

- project configuration and data boundary recorded;
- inputs, scripts, configurations, and hashes discoverable;
- missing dependencies labelled `BLOCKED`;
- provenance separated between method advice and local science evidence.

## Gate 2 — Analysis and figures

- result records contain estimand, uncertainty, sample unit, test, source script, and status;
- figure plan assigns each figure a reader question, role, primary claim, panel order, and main/supplement placement;
- figures link to results, claims, source files, captions, and manuscript locations;
- units, masks, signs, captions, and uncertainty are explicit;
- labels, scales, legends, colors, grayscale behavior, and export constraints are reviewed;
- figure order supports the evidence sequence;
- null, reverse, failed, and alternative results are preserved.

## Gate 3 — Manuscript reconstruction

- `manuscript_source.md` is treated as a fixed-fact input;
- `fact_ledger.yaml`, `story_spine.yaml`, and `section_map.yaml` are complete;
- all source blocks have a disposition;
- author approval is recorded before formal rewrite;
- figure sequence and story spine agree.

## Gate 4 — Manuscript

- title, abstract, introduction, results, discussion, conclusion, figures, and methods tell one consistent story;
- numeric and claim traceability checks pass;
- paragraph, sentence, word, citation, and style passes are complete;
- no unsupported causal, novelty, or mechanism language remains.

## Gate 5 — Review

- findings are location-specific and severity-ranked;
- each issue has a smallest repair and fallback wording;
- claims have support levels;
- author decisions and disagreements are recorded;
- AI review is not described as peer review.

## Gate 6 — Submission and revision

- current official journal rules are recorded;
- authorship, ethics, data, code, funding, conflict, and AI records are complete;
- all submission files share one version;
- every response-to-reviewer statement is verifiable in the revised manuscript.

## Readiness status

Use `NOT_READY_FOR_SUBMISSION` whenever a hard gate is unresolved, even if the prose is polished.
