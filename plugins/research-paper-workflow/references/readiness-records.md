# Local Readiness Records

Use Python 3.9+ with the plugin's `requirements.txt`. From the plugin root:

```sh
python3 scripts/build_workflow_report.py /path/to/project --stage review
python3 scripts/build_workflow_report.py /path/to/project --stage submission
```

Both commands write `workflow_report.json` and `workflow_report.md` in the project. A blocked check exits 1. Read the report and fix the evidence, not the status. These are local record checks, not an automatic scientific review, author attestation or submission receipt.

## Review

- Complete the project manifest and provenance. Set `status: READY_FOR_REVIEW` only after the draft and evidence records are prepared.
- Each `verified` result follows `analysis_results.json` and adds `input_files`, a mapping from project-relative paths to SHA-256. Use a project-local script and data snapshot. Null scientific results can be verified; blocked or exploratory rows cannot support verified claims. This checker currently implements the plugin's quantitative result schema, which expects a sample size, estimate, interval and p-value. Do not invent statistics to satisfy it; an incompatible study needs a schema extension or a documented manual audit, not a machine pass.
- Verified claims must link to verified results and figures, and figures must name their real output in `artifact_path`, include a caption and link back to the primary claim. A figure marked `approved` also qualifies. Use `draft.md` and `section_traceability.md`; for explicit reconstruction use the separately reviewed and author-approved `manuscript_reconstructed.md`. Include `[from:R001]`, `[claim:C001]`, and `[figure:F001]` markers in the working draft, not the submission copy. The gate checks the IDs, not whether every scientific sentence is correctly linked.

## Submission

Start with the [pending JSON template](../assets/submission-readiness-template.json) as `submission_readiness.json` in the project. Use the [first-submission gates](first-submission-gates.md) to actually perform the checks. Record the manuscript, SI, reproduction package and cover letter. For SI or a cover letter that genuinely does not apply, use `{"status": "not_applicable", "reason": "..."}` without a path.

- For each gate, record `verified` only after verifying it. Supply `checked_by`, `checked_on` and the path to a separate local evidence note explaining how it passed, including limitations. The reviewer-access note must document the actual access route and access test or explicit journal confirmation; the journal note must identify the official source, article type and check date. The author-confirmation note records actual approval of the frozen version and links to private local evidence if appropriate. Do not store access tokens or publish those notes.
- Compute `sha256` for the version's package files, gate evidence notes, project manifest, provenance, result/claim/figure records, result inputs, analysis scripts, figure outputs, draft and traceability records. Include any other files that the recorded checks depend on, such as review reports or submission metadata. Paths must be project-relative. Use `shasum -a 256` or an equivalent tool. A changed file trips the gate; repeat affected checks before updating the frozen manifest.
- Passing means `READY_FOR_AUTHOR_SUBMISSION`, not `SUBMITTED`. The script validates existence, structured records, selected links and frozen bytes. It does not run analysis, compare PDF prose with data, test a remote link, contact authors or verify the truth of a checker's attestation. Those checks must happen before recording a pass. A fixture can exercise software behavior but is never submission evidence.
