#!/usr/bin/env python3
"""Create a non-destructive evidence-first research project skeleton."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    root = args.output_dir
    for name in ("data", "figures", "runs", "submission"):
        (root / name).mkdir(parents=True, exist_ok=True)
    files = {
        "task_plan.md": "# Task Plan\n\n- Status: planned\n- Blockers:\n",
        "findings.md": "# Findings\n\n- No audit completed.\n",
        "progress.md": "# Progress\n\n| UTC time | Action | Status | Evidence |\n|---|---|---|---|\n",
        "positioning.yaml": "schema_version: \"1.0\"\nquestion: \"\"\nprimary_hypothesis: \"\"\nalternative_hypotheses: []\nintended_readers: []\nminimum_publishable_unit: \"\"\nstatus: BLOCKED\n",
        "journal_fit_matrix.md": "# Journal Fit Matrix\n\n| Tier | Journal | Official URL/date | Why suitable | Why unsuitable | Transfer condition | Status |\n|---|---|---|---|---|---|---|\n| Sprint | | | | | | BLOCKED |\n| Match | | | | | | BLOCKED |\n| Safe | | | | | | BLOCKED |\n",
        "research_question.md": "# Research Question\n\n- Question: pending\n- Contribution: pending\n- Reader: pending\n",
        "hypotheses.yaml": "primary: \"\"\nalternatives: []\npredictions: []\nstatus: BLOCKED\n",
        "title_candidates.md": "# Title Candidates\n\n1.\n2.\n3.\n",
        "project_manifest.yaml": "schema_version: \"1.0\"\nproject_id: \"\"\nresearch_question: \"\"\nprimary_hypothesis: \"\"\nalternative_hypotheses: []\ntarget_journal: \"\"\narticle_type: \"\"\ndata_boundary: local-only-until-authorized\nmethod_constraints: []\ngenerator_role: \"\"\ncritic_role: \"\"\nprocess_isolation_verified: false\nauthor_decisions_pending: []\nprovenance_labels: [BOOK-SUPPORTED, ARTICLE-SUPPORTED, INTERNAL-BASELINE, OUR-DESIGN, BLOCKED-SOURCE]\nstatus: BLOCKED\n",
        "provenance.md": "# Provenance\n\n- BOOK-SUPPORTED: writing, communication, or review method from the book.\n- ARTICLE-SUPPORTED: AI workflow advice from the supplied article PDF.\n- INTERNAL-BASELINE: existing plugin rule.\n- OUR-DESIGN: project-specific design decision.\n- BLOCKED-SOURCE: unavailable source or dependency.\n",
        "claims.yaml": "- claim_id: C001\n  text: \"\"\n  evidence_ids: []\n  result_ids: []\n  figure_ids: []\n  evidence_level: to_verify\n  alternative_explanations: []\n  limitations: []\n  allowed_verbs: [shows, is consistent with]\n  status: blocked\n  provenance: OUR-DESIGN\n  author_decision: \"\"\n",
        "analysis_results.json": json.dumps({"schema_version":"1.0", "results":[]}, indent=2) + "\n",
        "analysis_plan.md": "# Analysis Plan\n\n- Estimand: pending\n- Sample unit: pending\n- Uncertainty: pending\n- Multiple testing: pending\n- Reproducibility command: pending\n",
        "figure_manifest.yaml": "figures:\n  - figure_id: F001\n    title: \"\"\n    caption: \"\"\n    claim_ids: []\n    result_ids: []\n    source_files: []\n    units: []\n    uncertainty: \"\"\n    status: blocked\n",
        "figure_claim_ledger.md": "# Figure Claim Ledger\n\n| Figure ID | Claim ID | Result IDs | Caption | Status |\n|---|---|---|---|---|\n",
        "citations_todo.md": "# Citation TODO\n\n| Citation | DOI/URL | Verified by/date | Status |\n|---|---|---|---|\n",
        "ai_disclosure.md": "# AI Use Disclosure\n\nStatus: pending author review.\n",
        "CLAUDE.md": "# Project Configuration\n\nResearch question: pending\nData boundary: local only until authorized\nTarget journal: pending\n",
        "outline.md": "# Manuscript Outline\n\nQuestion: pending\nContribution: pending\n\n## Results\n\n| Section | Result IDs | Figure IDs | Claim IDs |\n|---|---|---|---|\n",
        "section_traceability.md": "# Section Traceability\n\n| Section | Result IDs | Claim IDs | Figure IDs | Status |\n|---|---|---|---|---|\n",
        "proof_checklist.md": "# Proof Checklist\n\n| Item | Status | Location | Correction | Verified by/date |\n|---|---|---|---|---|\n| Numbers and units | BLOCKED | | | |\n| Figures and captions | BLOCKED | | | |\n| References | BLOCKED | | | |\n",
        "author_contributions.md": "# Author Contributions\n\nPending author confirmation.\n",
    }
    root.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        path = root / rel
        if path.exists() and not args.force:
            continue
        path.write_text(content, encoding="utf-8")
    print(root)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
