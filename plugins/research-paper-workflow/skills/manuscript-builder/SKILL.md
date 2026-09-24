---
name: manuscript-builder
description: Build or revise a scientific manuscript from verified result and claim records while preserving numbers, citations, uncertainty, conclusion strength, and readable scientific structure.
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
- Use one primary function per paragraph and maintain old-information -> new-information flow.
- Prefer direct subjects and verbs; inspect tense, parallel structure, comparison, negation, and misplaced modifiers.
- Remove vague intensifiers, unsupported novelty language, biased wording, and avoidable ambiguity.
- Treat title, abstract, introduction, results, discussion, and conclusion as a connected argument rather than isolated sections.

## Five-pass editing order

1. Scientific argument: question -> method -> result -> claim.
2. Structure: section order, reader path, evidence placement, and transitions.
3. Paragraphs: unity, coherence, topic sentences, and old/new information.
4. Sentences: subject-verb distance, voice, tense, parallelism, comparisons, and modifiers.
5. Words: concision, precision, bias control, ambiguity, and claim strength.

Before delivery, run numeric consistency and manuscript traceability checks and list residual blockers. A fluent draft is not submission-ready evidence.
