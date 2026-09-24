#!/usr/bin/env python3
"""Validate minimal figure -> claim -> result links in a simple YAML manifest."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("path", type=Path); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); rows=[]; row=None
    for raw in args.path.read_text(encoding="utf-8", errors="replace").splitlines():
        line=raw.strip()
        if line.startswith("- figure_id:"):
            if row: rows.append(row)
            row={"figure_id": line.split(":",1)[1].strip()}
        elif row is not None and ":" in line and not line.startswith("#"):
            k,v=line.split(":",1); row[k.strip()]=v.strip()
    if row: rows.append(row)
    errors=[]
    for i,r in enumerate(rows,1):
        for k in ("figure_id","caption","claim_ids","result_ids","status"):
            if k not in r: errors.append(f"row {i}: missing {k}")
        if r.get("status") == "verified" and (r.get("claim_ids") in {"[]",""} or r.get("result_ids") in {"[]",""}):
            errors.append(f"row {i}: verified figure needs claim_ids and result_ids")
    out={"path":str(args.path),"figures":len(rows),"errors":errors,"status":"ok" if not errors else "failed"}
    print(json.dumps(out,ensure_ascii=False,indent=2) if args.json else ("OK" if not errors else "FAILED\n"+"\n".join(errors)))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
