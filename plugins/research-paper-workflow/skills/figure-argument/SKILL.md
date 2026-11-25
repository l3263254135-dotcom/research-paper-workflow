---
name: figure-argument
description: Build and audit figures as traceable argument units linked to results, claims, captions, and manuscript text.
---

# Figure Argument

Treat a figure as part of the reasoning and the reader path, not as decoration added after the prose. Use `$figure-optimization` for redesign and this skill for traceability and audit.

## Process

- Assign every figure a stable `figure_id`, a reader question, and one primary claim.
- Link each panel to result IDs, data sources, masks, units, denominators, time windows, and uncertainty definitions.
- Check the figure's role, main-text or supplementary placement, panel order, and relation to the story spine.
- Write a self-contained caption that states what is shown, how it was calculated, what visual encodings mean, and what the reader may infer.
- Check labels, scales, legends, error bars, color accessibility, grayscale behavior, panel order, export formats, and target-journal constraints.
- Compare figure values with `analysis_results.json`, tables, abstract, Results, Discussion, and Conclusion.

## When the core sequence breaks

Name the missing inference: which reader question remains unanswered, and what result would answer it? If the support is already visible, reorder the evidence or clarify the caption. Otherwise classify the gap before requesting another figure:

| Gap | Action |
|---|---|
| Display | A verified result answers the question but is not shown. Add the smallest useful figure, table, or panel, linked to that result. |
| Analysis | A needed comparison, estimate, or uncertainty check has not been verified. Return to data, methods, and analysis; mark the panel pending until the result is checked. |
| Design | Available data or design cannot distinguish the explanations or support the claim. Redesign with author agreement, or narrow or withdraw the claim; keep any independently supported finding. |

Record the gap and what would close it in the storyboard or existing ledger. A smoother transition or schematic is not evidence. A check that changes the meaning of a central result must stay visible alongside that result.

## Acceptance

- No figure exists without a claim, source result, caption, manuscript location, and status.
- Set `artifact_path` in the figure manifest to the project-relative path of the rendered figure checked in this round.
- Units, masks, signs, denominators, sample units, and time windows are explicit.
- Main-text figure order follows the paper's evidence sequence.
- The figure does not imply a stronger causal or mechanistic conclusion than the evidence supports.
- Duplicate, unreadable, or non-informative figures are repaired or moved to supporting information with a reason.
