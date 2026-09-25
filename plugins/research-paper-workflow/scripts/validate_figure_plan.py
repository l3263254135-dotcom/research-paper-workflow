#!/usr/bin/env python3
"""Validate the lightweight figure plan without requiring PyYAML."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_rows(path: Path):
    rows = []
    row = None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if line.startswith("- figure_id:"):
            if row:
                rows.append(row)
            row = {"figure_id": line.split(":", 1)[1].strip().strip("\"'")}
        elif row is not None and ":" in line and not line.startswith("#"):
            key, value = line.split(":", 1)
            row[key.strip()] = value.strip().strip("\"'")
    if row:
        rows.append(row)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rows = parse_rows(args.path)
    errors = []
    for idx, row in enumerate(rows, 1):
        for key in ("figure_id", "role", "reader_question", "primary_claim_id", "result_ids", "main_or_supplement", "rationale"):
            if key not in row:
                errors.append(f"row {idx}: missing {key}")
        if row.get("status") in {"verified", "approved"} and row.get("primary_claim_id") in {"", "[]", "null"}:
            errors.append(f"row {idx}: verified plan needs primary_claim_id")
    if not rows:
        errors.append("no figure plan rows found")
    out = {"path": str(args.path), "figures": len(rows), "errors": errors, "status": "ok" if not errors else "failed"}
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else ("OK" if not errors else "FAILED\n" + "\n".join(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
