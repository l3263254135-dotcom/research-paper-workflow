---
name: submission-revision
description: Prepare and audit journal submission, revision, and proof packages, including declarations, data/code records, cover letters, authorship, and point-by-point responses without submitting externally.
---

# Submission and Revision

Read the target journal's current official instructions and record URL, access date, and verification status. Keep author and institutional fields as explicit pending inputs when unavailable.

## Audit

Check article type, title page, abstract/word limit, key points, line numbers, references, figures, tables, SI, data/code/materials statements, funding, conflicts, authorship/CRediT, ORCID, AI disclosure, permissions, license requirements, figure dimensions, resolution, color and grayscale behavior, file formats, figure numbering, and proof corrections.

For a revision, preserve the submitted version and maintain an opinion table with: reviewer comment, interpretation, action, evidence, manuscript location, response, and status. Verify every claimed change against the actual revised files. Classify comments as major, minor, factual correction, methodological request, or disagreement requiring an evidence-based explanation.

Do not access a submission portal, submit, publish, or invent author, funding, ethics, repository, or policy information. Leave `NOT_READY_FOR_SUBMISSION` when a hard gate is unresolved.

For a first submission, follow [first-submission gates](../../references/first-submission-gates.md) and use the [local record contract](../../references/readiness-records.md) to bind checks to the frozen files. Verify reviewer access through journal-approved evidence supplied by the author. A local open, an owner's download, or a resolving DOI does not prove reviewer access. Copy the [readiness template](../../assets/submission-readiness-template.json) with all gates pending and only mark a gate verified after inspecting its evidence. Run `build_workflow_report.py` with `--stage submission` before handing off. Never record a test fixture as an author confirmation or external receipt.
