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
        "project_manifest.yaml": "schema_version: \"1.0\"\nproject_id: \"\"\nresearch_question: \"\"\nprimary_hypothesis: \"\"\nalternative_hypotheses: []\ntarget_journal: \"\"\narticle_type: \"\"\ndata_boundary: local-only-until-authorized\nmethod_constraints: []\ngenerator_role: \"\"\ncritic_role: \"\"\nprocess_isolation_verified: false\nmanuscript_mode: standard\nsource_manuscript: manuscript_source.md\nreconstruction_approval: pending\nfigure_optimization_status: blocked\nauthor_decisions_pending: []\nprovenance_labels: [BOOK-SUPPORTED, ARTICLE-SUPPORTED, INTERNAL-BASELINE, OUR-DESIGN, BLOCKED-SOURCE]\nstatus: BLOCKED\n",
        "provenance.md": "# Provenance\n\n- BOOK-SUPPORTED: writing, communication, or review method from the book.\n- ARTICLE-SUPPORTED: AI workflow advice from the supplied article PDF.\n- INTERNAL-BASELINE: existing plugin rule.\n- OUR-DESIGN: project-specific design decision.\n- BLOCKED-SOURCE: unavailable source or dependency.\n",
        "claims.yaml": "- claim_id: C001\n  text: \"\"\n  evidence_ids: []\n  result_ids: []\n  figure_ids: []\n  evidence_level: to_verify\n  alternative_explanations: []\n  limitations: []\n  allowed_verbs: [shows, is consistent with]\n  status: blocked\n  provenance: OUR-DESIGN\n  author_decision: \"\"\n",
        "analysis_results.json": json.dumps({"schema_version":"1.0", "results":[]}, indent=2) + "\n",
        "analysis_plan.md": "# Analysis Plan\n\n- Estimand: pending\n- Sample unit: pending\n- Uncertainty: pending\n- Multiple testing: pending\n- Reproducibility command: pending\n",
        "figure_manifest.yaml": "figures:\n  - figure_id: F001\n    role: primary_result\n    reader_question: \"\"\n    title: \"\"\n    caption: \"\"\n    primary_claim_id: \"\"\n    secondary_claim_ids: []\n    result_ids: []\n    panel_roles: []\n    source_files: []\n    analysis_script: \"\"\n    data_transform: \"\"\n    sample_unit: \"\"\n    denominator: \"\"\n    time_window: \"\"\n    comparison_baseline: \"\"\n    units: []\n    uncertainty_definition: \"\"\n    statistical_annotation: \"\"\n    color_encoding: \"\"\n    accessibility_check: pending\n    grayscale_check: pending\n    manuscript_locations: []\n    main_or_supplement: main\n    journal_constraints: []\n    status: blocked\n",
        "figure_claim_ledger.md": "# Figure Claim Ledger\n\n| Figure ID | Claim ID | Result IDs | Caption | Status |\n|---|---|---|---|---|\n",
        "citations_todo.md": "# Citation TODO\n\n| Citation | DOI/URL | Verified by/date | Status |\n|---|---|---|---|\n",
        "ai_disclosure.md": "# AI Use Disclosure\n\nStatus: pending author review.\n",
        "CLAUDE.md": "# Project Configuration\n\nResearch question: pending\nData boundary: local only until authorized\nTarget journal: pending\n",
        "outline.md": "# Manuscript Outline\n\nQuestion: pending\nContribution: pending\n\n## Figure Sequence\n\n| Order | Figure ID | Reader question | Primary claim | Main/Supplement |\n|---|---|---|---|---|\n\n## Results\n\n| Section | Result IDs | Figure IDs | Claim IDs |\n|---|---|---|---|---|\n",
        "section_traceability.md": "# Section Traceability\n\n| Section | Result IDs | Claim IDs | Figure IDs | Status |\n|---|---|---|---|---|\n",
        "manuscript_source.md": "# Source Manuscript\n\nPaste or convert the current manuscript here. This file is treated as the fixed-fact product specification for reconstruction mode.\n",
        "reconstruction_config.yaml": "schema_version: \"1.0\"\nmode: reconstruction\nsource_manuscript: manuscript_source.md\ninternal_rewrite_order: [Results, Discussion, Introduction, Conclusion, Abstract, Title, Methods, Captions]\nreconstruction_approval: pending\npreserve_facts: true\nallow_new_results: false\nallow_new_citations: false\nstatus: blocked\n",
        "reconstruction_status.yaml": "schema_version: \"1.0\"\nstatus: BLOCKED\nreconstruction_approval: pending\nblocking_reasons:\n  - source manuscript and evidence records are not verified\n",
        "fact_ledger.yaml": "schema_version: \"1.0\"\nsource_manuscript: manuscript_source.md\nstatus: blocked\nfacts:\n  - fact_id: FACT001\n    source_block: \"\"\n    fact_type: observation\n    text: \"\"\n    numeric_tokens: []\n    unit: \"\"\n    result_ids: []\n    claim_ids: []\n    figure_ids: []\n    limitation: \"\"\n    evidence_strength: to_verify\n    disposition: preserve\n    author_decision: \"\"\n",
        "reconstruction_brief.md": "# Reconstruction Brief\n\n- Core question: pending\n- Core claim: pending\n- Reader promise: pending\n- Knowledge gap: pending\n- Contribution boundary: pending\n- Approval: pending\n",
        "story_spine.yaml": "schema_version: \"1.0\"\nstatus: blocked\ncore_question: \"\"\ncore_claim: \"\"\nreader_promise: \"\"\nknowledge_gap: \"\"\ncontribution_boundary: \"\"\nevidence_sequence:\n  - step_id: S001\n    question: \"\"\n    result_ids: []\n    figure_ids: []\n    claim_ids: []\n    role: orientation\n    transition_to: []\nalternative_explanations: []\nconclusion_boundary: \"\"\nfigure_sequence: []\n",
        "section_map.yaml": "schema_version: \"1.0\"\nstatus: blocked\nsections:\n  - section_id: R001\n    target_section: Results\n    source_blocks: []\n    result_ids: []\n    figure_ids: []\n    claim_ids: []\n    function: \"\"\n    disposition: preserve\n    transition: \"\"\n",
        "rewrite_decision_log.md": "# Rewrite Decision Log\n\n| Source block | Target location | Action | Reason | Evidence preserved | Author decision | Status |\n|---|---|---|---|---|---|---|\n",
        "figure_plan.yaml": "schema_version: \"1.0\"\nstatus: blocked\nfigure_sequence:\n  - figure_id: F001\n    role: primary_result\n    reader_question: \"\"\n    primary_claim_id: \"\"\n    result_ids: []\n    panel_order: []\n    main_or_supplement: main\n    manuscript_locations: []\n    rationale: \"\"\n",
        "figure_storyboard.md": "# Figure Storyboard\n\n## Figure F001\n\n- Reader question: pending\n- Primary claim: pending\n- Evidence carried: pending\n- Main or supplement: pending\n- Panel order: pending\n- What the reader should notice first: pending\n- What the figure does not establish: pending\n- Planned caption: pending\n- Open author decisions: pending\n",
        "figure_reallocation_log.md": "# Figure Reallocation Log\n\n| Figure ID | Previous location | New location | Reason | Evidence preserved | Author decision | Status |\n|---|---|---|---|---|---|---|\n",
        "figure_change_log.md": "# Figure Change Log\n\n| Figure/panel | Before | After | Data unchanged | Claim unchanged | Reason | Reviewer/author decision | Status |\n|---|---|---|---|---|---|---|---|\n",
        "figure_qa_report.json": json.dumps({"status":"BLOCKED", "errors":["figure plan and manifest not verified"]}, ensure_ascii=False, indent=2) + "\n",
        "figure_qa_report.md": "# Figure QA Report\n\n- Status: **BLOCKED**\n- Figure plan and manifest are not verified.\n",
        "rewrite_log.md": "# Rewrite Log\n\n| Round | Section | Change type | Before/after location | Evidence checked | Status |\n|---|---|---|---|---|---|\n",
        "manuscript_reconstructed.md": "# Reconstructed Manuscript\n\nStatus: BLOCKED until the reconstruction approval gate is satisfied.\n",
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
