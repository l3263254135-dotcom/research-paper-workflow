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
        "claims.yaml": "- claim_id: C001\n  text: \"\"\n  evidence_ids: []\n  result_ids: []\n  figure_ids: []\n  evidence_level: to_verify\n  alternative_explanations: []\n  limitations: []\n  allowed_verbs: [shows, is consistent with]\n  status: blocked\n",
        "analysis_results.json": json.dumps({"schema_version":"1.0", "results":[]}, indent=2) + "\n",
        "citations_todo.md": "# Citation TODO\n\n| Citation | DOI/URL | Verified by/date | Status |\n|---|---|---|---|\n",
        "ai_disclosure.md": "# AI Use Disclosure\n\nStatus: pending author review.\n",
        "CLAUDE.md": "# Project Configuration\n\nResearch question: pending\nData boundary: local only until authorized\nTarget journal: pending\n",
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
