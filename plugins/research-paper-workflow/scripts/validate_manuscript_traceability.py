#!/usr/bin/env python3
"""Check manuscript traceability markers against local result and claim records."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

def claim_ids(path: Path):
    return set(re.findall(r"^\s*-\s*claim_id:\s*([^\s#]+)", path.read_text(encoding="utf-8", errors="replace"), re.M))

def figure_ids(path: Path):
    return set(re.findall(r"^\s*-\s*figure_id:\s*([^\s#]+)", path.read_text(encoding="utf-8", errors="replace"), re.M))

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("results", type=Path); ap.add_argument("claims", type=Path); ap.add_argument("manuscript", nargs="+", type=Path); ap.add_argument("--figures", type=Path); ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        results_obj = json.loads(args.results.read_text(encoding="utf-8"))
        result_ids = {str(r.get("result_id")) for r in results_obj.get("results", []) if r.get("result_id")}
        parse_error = ""
    except Exception as exc:
        result_ids=set(); parse_error=str(exc)
    claims = claim_ids(args.claims)
    figures = figure_ids(args.figures) if args.figures else set()
    errors=[]; checked=0
    if parse_error: errors.append(f"results parse error: {parse_error}")
    for path in args.manuscript:
        text=path.read_text(encoding="utf-8", errors="replace")
        refs=re.findall(r"\[from:\s*([^\]]+)\]", text)
        crefs=re.findall(r"\[claim:\s*([^\]]+)\]", text)
        frefs=re.findall(r"\[figure:\s*([^\]]+)\]", text)
        checked += len(refs)+len(crefs)+len(frefs)
        for rid in refs:
            if rid.strip() not in result_ids: errors.append(f"{path}: unknown result {rid.strip()}")
        for cid in crefs:
            if cid.strip() not in claims: errors.append(f"{path}: unknown claim {cid.strip()}")
        if args.figures:
            for fid in frefs:
                if fid.strip() not in figures: errors.append(f"{path}: unknown figure {fid.strip()}")
        if "[NUMBER_NEEDED]" in text: errors.append(f"{path}: NUMBER_NEEDED placeholder remains")
    out={"manuscripts":len(args.manuscript),"markers_checked":checked,"figure_manifest":str(args.figures) if args.figures else None,"errors":errors,"status":"ok" if not errors else "failed"}
    print(json.dumps(out,ensure_ascii=False,indent=2) if args.json else ("OK" if not errors else "FAILED\n"+"\n".join(errors)))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
