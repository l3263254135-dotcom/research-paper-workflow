#!/usr/bin/env python3
"""Check that explicitly supplied numeric tokens occur in a text artifact."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("results",type=Path); ap.add_argument("text",nargs="+",type=Path); a=ap.parse_args()
    obj=json.loads(a.results.read_text(encoding="utf-8")); nums=[]
    for r in obj.get("results",[]):
        if r.get("status")=="verified":
            for k in ("estimate","ci_low","ci_high","n","p_exact"):
                v=r.get(k)
                if isinstance(v,(int,float)) and not isinstance(v,bool): nums.append((r.get("result_id"),k,str(v)))
    missing=[]
    for p in a.text:
        s=p.read_text(encoding="utf-8",errors="replace")
        for rid,k,v in nums:
            if v not in s: missing.append({"file":str(p),"result_id":rid,"field":k,"value":v})
    out={"checked_numbers":len(nums),"missing":missing,"status":"ok" if not missing else "failed"}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if not missing else 1
if __name__=="__main__": raise SystemExit(main())
