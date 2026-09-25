#!/usr/bin/env python3
"""Check figure captions for required self-contained fields."""
from __future__ import annotations

import argparse
import json
import re
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
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    errors = []
    for idx, row in enumerate(parse_rows(args.manifest), 1):
        caption = row.get("caption", "")
        if row.get("status") not in {"verified", "approved"}:
            continue
        if not caption or caption in {'""', "''"}:
            errors.append(f"row {idx}: empty caption")
            continue
        lower = caption.lower()
        if not re.search(r"\b(?:figure|fig\.?|panel|\([a-z]\))\b", lower):
            errors.append(f"row {idx}: caption does not identify figure or panel")
        if row.get("units") not in {None, "", "[]"} and not any(token.lower() in lower for token in re.findall(r"[A-Za-z%µμ/]+", row.get("units", ""))):
            errors.append(f"row {idx}: caption does not mention manifest units")
        if row.get("uncertainty_definition") not in {None, "", '""'} and not any(word in lower for word in ("error", "uncertainty", "confidence", "interval", "sd", "se")):
            errors.append(f"row {idx}: caption does not define uncertainty")
    out = {"path": str(args.manifest), "errors": errors, "status": "ok" if not errors else "failed"}
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else ("OK" if not errors else "FAILED\n" + "\n".join(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
