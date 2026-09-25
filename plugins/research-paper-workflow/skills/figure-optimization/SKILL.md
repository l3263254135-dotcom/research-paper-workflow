---
name: figure-optimization
description: Redesign scientific figures, tables, and schematics as traceable argument units without changing data or scientific conclusions.
---

# Figure Optimization

Use this skill after verified analysis and before manuscript reconstruction. Treat each figure as a reasoning unit with a reader question, a primary claim, and an explicit place in the paper's evidence sequence.

## Process

1. Read `analysis_results.json`, `claims.yaml`, `figure_manifest.yaml`, and `story_spine.yaml` when available.
2. Build `figure_plan.yaml` and `figure_storyboard.md` before proposing visual edits.
3. Assign each figure a role such as orientation, primary result, comparison, robustness, alternative explanation, null result, mechanism constraint, or supplementary verification.
4. Decide main-text versus supplementary placement and order panels as problem -> evidence -> comparison -> bounded interpretation.
5. Propose visual changes to chart type, panel order, axes, labels, annotations, legend, color, line type, spacing, and export settings.
6. Record every move in `figure_reallocation_log.md` and `figure_change_log.md`.
7. Run the figure validators and compare figure values with results, claims, captions, and manuscript text.

## Hard boundaries

- Never edit raw data, sample definitions, statistical estimands, or scientific conclusions through a visual change.
- Preserve null, reverse, failed, and inconvenient results; move them to supplementary material only with a recorded reason.
- Do not use scale truncation, decorative effects, dual axes, color contrast, or annotations to exaggerate evidence.
- Do not add unsupported arrows or causal pathways to a mechanism schematic.

## Figure and caption standard

Every figure must have a stable ID, a primary claim, source results, source files, units, sample unit, denominator when relevant, uncertainty definition, panel roles, caption, manuscript locations, and status.

The caption must explain what is shown, what each panel does, how values were calculated, what error bars or shading mean, what symbols and colors mean, and what limited conclusion the reader may draw. It must not introduce new facts or stronger claims.

Check label clarity, scale choice, legend completeness, grayscale and color accessibility, panel order, figure citation order, export format, and consistency with the target journal.

## Acceptance

- No figure is orphaned from its claim, result, caption, or manuscript location.
- Every core claim has an explicit evidence carrier or is marked text-only with an author decision.
- Figure, caption, abstract, Results, Discussion, and Conclusion use the same evidence strength.
- Duplicate, unreadable, or non-informative figures are repaired, moved, or dispositioned with a reason.
