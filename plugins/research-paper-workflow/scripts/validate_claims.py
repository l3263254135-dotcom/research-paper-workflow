#!/usr/bin/env python3
"""Validate a deliberately small YAML-like claims file without third-party YAML."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

REQ = ("claim_id", "text", "evidence_ids", "result_ids", "figure_ids", "evidence_level", "status")
def parse(path: Path):
    rows=[]; row=None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line=raw.strip()
        if line.startswith("- "):
            if row: rows.append(row)
            row={}; line=line[2:]
        if ":" in line and row is not None:
            k,v=line.split(":",1); row[k.strip()]=v.strip()
    if row: rows.append(row)
    return rows
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("path", type=Path); ap.add_argument("--json", action="store_true"); a=ap.parse_args()
    errors=[]; rows=parse(a.path)
    for i,r in enumerate(rows,1):
        for k in REQ:
            if k not in r: errors.append(f"row {i}: missing {k}")
        if r.get("evidence_level") in {"source-backed","inference"} and r.get("evidence_ids") in {"[]","null",""}: errors.append(f"row {i}: evidence required")
        if r.get("status") == "verified" and r.get("result_ids") in {"[]","null",""}: errors.append(f"row {i}: verified claim needs result_ids")
    out={"path":str(a.path),"claims":len(rows),"errors":errors,"status":"ok" if not errors else "failed"}
    print(json.dumps(out, ensure_ascii=False, indent=2) if a.json else ("OK" if not errors else "FAILED\n"+"\n".join(errors)))
    return 0 if not errors else 1
if __name__ == "__main__": raise SystemExit(main())
