#!/usr/bin/env python3
"""Validate result records; missing/null fields remain missing, never zero."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
REQ=("result_id","variable","unit","region","season","contrast","window","n","estimate","ci_low","ci_high","test","p_exact","script_path","input_hash","status")
def finite(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("path",type=Path); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
    obj=json.loads(a.path.read_text(encoding="utf-8")); rows=obj.get("results",[]); errors=[]
    for i,r in enumerate(rows,1):
        for k in REQ:
            if k not in r: errors.append(f"row {i}: missing {k}")
        if r.get("status")=="verified":
            for k in ("n","estimate","ci_low","ci_high","p_exact"):
                if not finite(r.get(k)): errors.append(f"row {i}: verified {k} must be finite")
            if finite(r.get("ci_low")) and finite(r.get("ci_high")) and r["ci_low"]>r["ci_high"]: errors.append(f"row {i}: CI order")
            if finite(r.get("p_exact")) and not 0<=r["p_exact"]<=1: errors.append(f"row {i}: p outside [0,1]")
        if r.get("status") not in {"verified","blocked","exploratory"}: errors.append(f"row {i}: invalid status")
    out={"path":str(a.path),"results":len(rows),"errors":errors,"status":"ok" if not errors else "failed"}
    print(json.dumps(out,ensure_ascii=False,indent=2) if a.json else ("OK" if not errors else "FAILED\n"+"\n".join(errors)))
    return 0 if not errors else 1
if __name__ == "__main__": raise SystemExit(main())
