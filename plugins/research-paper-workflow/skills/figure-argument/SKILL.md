---
name: figure-argument
description: Build and audit figures as traceable argument units linked to results, claims, captions, and manuscript text.
---

# Figure Argument

Treat a figure as part of the reasoning, not as decoration added after the prose.

## Process

- Assign every figure a stable `figure_id` and one primary claim.
- Link each panel to result IDs, data sources, masks, units, and uncertainty definitions.
- Write a self-contained caption that states what is shown, how it was calculated, and what the reader should infer.
- Check labels, scales, legends, error bars, color accessibility, grayscale behavior, panel order, and export formats.
- Compare figure values with `analysis_results.json`, tables, abstract, results, and conclusion.

## Acceptance

- No figure exists without a claim, source result, caption, and status.
- Units, masks, signs, denominators, and time windows are explicit.
- The figure does not imply a stronger causal or mechanistic conclusion than the evidence supports.
- Duplicate or non-informative figures are removed or moved to supporting information with a reason.
