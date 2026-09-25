#!/usr/bin/env python3
"""Validate story-spine links to local results, claims, and figures."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def ids_from_file(path: Path, pattern: str) -> set[str]:
    return set(re.findall(pattern, path.read_text(encoding="utf-8", errors="replace"), re.M)) if path.exists() else set()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("story_spine", type=Path)
    ap.add_argument("results", type=Path)
    ap.add_argument("claims", type=Path)
    ap.add_argument("figure_manifest", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    story = args.story_spine.read_text(encoding="utf-8", errors="replace")
    try:
        result_obj = json.loads(args.results.read_text(encoding="utf-8"))
        result_ids = {str(row.get("result_id")) for row in result_obj.get("results", []) if row.get("result_id")}
        parse_error = ""
    except Exception as exc:
        result_ids = set()
        parse_error = str(exc)

    claim_ids = ids_from_file(args.claims, r"^\s*-\s*claim_id:\s*([^\s#]+)")
    figure_ids = ids_from_file(args.figure_manifest, r"^\s*-\s*figure_id:\s*([^\s#]+)")
    referenced_results = set(re.findall(r"\bR\d{2,}\b", story))
    referenced_claims = set(re.findall(r"\bC\d{2,}\b", story))
    referenced_figures = set(re.findall(r"\bF\d{2,}\b", story))

    errors = []
    if parse_error:
        errors.append(f"results parse error: {parse_error}")
    for rid in sorted(referenced_results - result_ids):
        errors.append(f"unknown result {rid}")
    for cid in sorted(referenced_claims - claim_ids):
        errors.append(f"unknown claim {cid}")
    for fid in sorted(referenced_figures - figure_ids):
        errors.append(f"unknown figure {fid}")
    if "evidence_sequence:" in story and not (referenced_results or referenced_claims or referenced_figures):
        errors.append("evidence_sequence has no linked result, claim, or figure")

    out = {
        "story_spine": str(args.story_spine),
        "referenced_results": sorted(referenced_results),
        "referenced_claims": sorted(referenced_claims),
        "referenced_figures": sorted(referenced_figures),
        "errors": errors,
        "status": "ok" if not errors else "failed",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else ("OK" if not errors else "FAILED\n" + "\n".join(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
