---
name: manuscript-reconstruction
description: Rebuild a scientific manuscript's narrative and structure from an immutable fact ledger before rewriting prose.
---

# Manuscript Reconstruction

Use this skill when an existing manuscript contains fixed data, results, figures, and conclusions but needs a new scientific story, structure, and expression layer.

Treat `manuscript_source.md` as the product specification. The rewrite may change the reader path, section order, paragraph order, transitions, sentence structure, and wording. It must not silently change scientific facts or evidence strength.

## Two-stage contract

### R1 — Reconstruction design

Read `manuscript_source.md`, `analysis_results.json`, `claims.yaml`, `figure_manifest.yaml`, `section_traceability.md`, `citations_todo.md`, and `project_manifest.yaml`. Produce:

- `fact_ledger.yaml`;
- `reconstruction_brief.md`;
- `story_spine.yaml`;
- `section_map.yaml`;
- `rewrite_decision_log.md`;
- `reconstruction_status.yaml` with `AWAITING_AUTHOR_APPROVAL`.

R1 must state the core question, core claim, evidence ladder, role of every major result, alternative explanations, conclusion boundary, reader promise, and the disposition of material that is moved, merged, compressed, or removed.

### R2 — Section rewrite

Do not generate `manuscript_reconstructed.md` until `reconstruction_status.yaml` or `project_manifest.yaml` contains `reconstruction_approval: approved`.

Rewrite internally in this order: Results, Discussion, Introduction, Conclusion, Abstract, Title, then Methods and captions. Render the final manuscript in the target journal's required order. Keep stable result, claim, figure, and source markers during drafting.

## Fact preservation

Freeze and compare numeric values, units, sample sizes, windows, estimates, intervals, tests, exact p/q values, figure/table IDs, result IDs, claim IDs, null and reverse results, limitations, citations, and conclusion qualifiers.

Stop with `NOT_READY_FOR_SUBMISSION` when the rewrite adds a new fact, strengthens a causal or mechanistic statement, drops a material limitation without a disposition record, or leaves a paragraph without a source block, result, claim, or explicit transition function.

## Writing passes

Run one issue class per pass:

1. scientific argument: question -> method -> result -> claim;
2. structure: section roles, figure sequence, evidence placement, and transitions;
3. paragraphs: unity, topic sentence, old-to-new information flow;
4. sentences: subject-verb distance, voice, tense, parallelism, comparisons, and modifiers;
5. words: precision, concision, bias control, ambiguity, and claim strength.

Record every non-trivial move in `rewrite_log.md`. Use `validate_fact_preservation.py`, `validate_story_traceability.py`, and `validate_reconstruction_output.py` before delivery.
