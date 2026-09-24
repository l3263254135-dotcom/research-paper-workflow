#!/usr/bin/env python3
"""Validate required project configuration fields without requiring PyYAML."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

REQUIRED = (
    "schema_version", "project_id", "research_question", "target_journal",
    "article_type", "data_boundary", "generator_role", "critic_role",
    "process_isolation_verified", "status",
)

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("path", type=Path); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); text = args.path.read_text(encoding="utf-8", errors="replace")
    errors = []
    for key in REQUIRED:
        if not re.search(rf"^\s*{re.escape(key)}\s*:", text, re.M):
            errors.append(f"missing {key}")
    if "local-only-until-authorized" not in text:
        errors.append("data_boundary must declare a local default")
    status = "ok" if not errors else "failed"
    out = {"path": str(args.path), "errors": errors, "status": status}
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else ("OK" if not errors else "FAILED\n" + "\n".join(errors)))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
