#!/usr/bin/env python3
"""Build a small status report from local workflow records."""
from __future__ import annotations
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project",type=Path); a=ap.parse_args(); root=a.project
    checks={
        "claims":(root/"claims.yaml").exists(),
        "analysis_results":(root/"analysis_results.json").exists(),
        "task_plan":(root/"task_plan.md").exists(),
        "findings":(root/"findings.md").exists(),
        "progress":(root/"progress.md").exists(),
        "project_manifest":(root/"project_manifest.yaml").exists(),
        "provenance":(root/"provenance.md").exists(),
        "figure_manifest":(root/"figure_manifest.yaml").exists(),
        "figure_plan":(root/"figure_plan.yaml").exists(),
        "figure_storyboard":(root/"figure_storyboard.md").exists(),
        "section_traceability":(root/"section_traceability.md").exists(),
        "manuscript_source":(root/"manuscript_source.md").exists(),
        "fact_ledger":(root/"fact_ledger.yaml").exists(),
        "story_spine":(root/"story_spine.yaml").exists(),
        "section_map":(root/"section_map.yaml").exists(),
        "reconstruction_status":(root/"reconstruction_status.yaml").exists(),
    }
    blockers=[]
    if not checks["claims"]: blockers.append("claims.yaml missing")
    if not checks["analysis_results"]: blockers.append("analysis_results.json missing")
    if not checks["project_manifest"]: blockers.append("project_manifest.yaml missing")
    if not checks["provenance"]: blockers.append("provenance.md missing")
    if checks["project_manifest"]:
        manifest_text=(root/"project_manifest.yaml").read_text(encoding="utf-8", errors="replace")
        if "status: BLOCKED" in manifest_text or 'status: "BLOCKED"' in manifest_text:
            blockers.append("project_manifest status is BLOCKED")
        if "manuscript_mode: reconstruction" in manifest_text and checks["manuscript_source"]:
            status_text = (root/"reconstruction_status.yaml").read_text(encoding="utf-8", errors="replace") if checks["reconstruction_status"] else ""
            if "status: BLOCKED" in status_text:
                blockers.append("reconstruction status is BLOCKED")
            if "reconstruction_approval: pending" in manifest_text:
                blockers.append("reconstruction approval is pending")
    if checks["figure_plan"]:
        figure_plan_text=(root/"figure_plan.yaml").read_text(encoding="utf-8", errors="replace")
        if "status: blocked" in figure_plan_text:
            blockers.append("figure plan status is BLOCKED")
    status="READY_FOR_REVIEW" if not blockers else "BLOCKED"
    report={"project":str(root),"status":status,"quality_axes":{"science":"not_scored","presentation":"not_scored","figure_argument":"not_scored","reconstruction":"not_scored"},"checks":checks,"blockers":blockers}
    (root/"workflow_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    md="# Workflow Report\n\n- Status: **%s**\n- Project: `%s`\n\n## Checks\n%s\n\n## Blockers\n%s\n"%(status,root,"\n".join(f"- {k}: {'ok' if v else 'missing'}" for k,v in checks.items()) or "- none", "\n".join(f"- {x}" for x in blockers) or "- none")
    (root/"workflow_report.md").write_text(md,encoding="utf-8"); print(json.dumps(report,ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
