#!/usr/bin/env python3
"""Check that figure captions and manuscript text carry linked verified result values."""
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


def ids(value: str) -> set[str]:
    return set(re.findall(r"R\d{2,}", value or ""))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("results", type=Path)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("text", nargs="*", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    obj = json.loads(args.results.read_text(encoding="utf-8"))
    result_values = {str(row.get("result_id")): [str(row.get(key)) for key in ("estimate", "ci_low", "ci_high", "n", "p_exact") if row.get(key) is not None] for row in obj.get("results", []) if row.get("status") == "verified"}
    errors = []
    for row in parse_rows(args.manifest):
        if row.get("status") not in {"verified", "approved"}:
            continue
        linked = ids(row.get("result_ids", ""))
        body = row.get("caption", "") + "\n" + "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in args.text)
        for rid in linked:
            values = result_values.get(rid, [])
            if values and not any(value in body for value in values):
                errors.append(f"{row.get('figure_id')}: no linked verified result value found for {rid}")
    out = {"figures_checked": len(parse_rows(args.manifest)), "errors": errors, "status": "ok" if not errors else "failed"}
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else ("OK" if not errors else "FAILED\n" + "\n".join(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
