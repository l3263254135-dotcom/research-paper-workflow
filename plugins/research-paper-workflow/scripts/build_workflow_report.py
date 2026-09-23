#!/usr/bin/env python3
"""Build a small status report from local workflow records."""
from __future__ import annotations
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project",type=Path); a=ap.parse_args(); root=a.project
    checks={"claims":(root/"claims.yaml").exists(),"analysis_results":(root/"analysis_results.json").exists(),"task_plan":(root/"task_plan.md").exists(),"findings":(root/"findings.md").exists(),"progress":(root/"progress.md").exists()}
    blockers=[]
    if not checks["claims"]: blockers.append("claims.yaml missing")
    if not checks["analysis_results"]: blockers.append("analysis_results.json missing")
    status="READY_FOR_REVIEW" if not blockers else "BLOCKED"
    report={"project":str(root),"status":status,"checks":checks,"blockers":blockers}
    (root/"workflow_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    md="# Workflow Report\n\n- Status: **%s**\n- Project: `%s`\n\n## Checks\n%s\n\n## Blockers\n%s\n"%(status,root,"\n".join(f"- {k}: {'ok' if v else 'missing'}" for k,v in checks.items()) or "- none", "\n".join(f"- {x}" for x in blockers) or "- none")
    (root/"workflow_report.md").write_text(md,encoding="utf-8"); print(json.dumps(report,ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
