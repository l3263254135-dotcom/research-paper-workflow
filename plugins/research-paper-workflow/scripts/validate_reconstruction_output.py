#!/usr/bin/env python3
"""Validate approval, traceability markers, and claim-strength drift in a rewrite."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

STRONG_LANGUAGE = re.compile(r"\b(?:causes?|causal|mechanism|proves?|demonstrates? that|first to|solves?|establishes?)\b", re.I)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("reconstructed", type=Path)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--ledger", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    source = args.source.read_text(encoding="utf-8", errors="replace")
    rebuilt = args.reconstructed.read_text(encoding="utf-8", errors="replace")
    config = args.config.read_text(encoding="utf-8", errors="replace") if args.config and args.config.exists() else ""

    errors = []
    approval = re.search(r"reconstruction_approval:\s*['\"]?approved\b", config, re.I)
    if not approval:
        errors.append("reconstruction approval is not set to approved")
    if "[NUMBER_NEEDED]" in rebuilt:
        errors.append("reconstructed manuscript contains [NUMBER_NEEDED]")

    source_strong = {m.group(0).lower() for m in STRONG_LANGUAGE.finditer(source)}
    rebuilt_strong = {m.group(0).lower() for m in STRONG_LANGUAGE.finditer(rebuilt)}
    new_strong = sorted(rebuilt_strong - source_strong)
    if new_strong:
        errors.append("new strong causal/mechanistic language: " + ", ".join(new_strong))

    for marker in re.findall(r"\[(?:from|claim):\s*[^\]]+\]", rebuilt):
        if not marker.strip():
            errors.append("empty traceability marker")

    out = {
        "source": str(args.source),
        "reconstructed": str(args.reconstructed),
        "approval": bool(approval),
        "new_strong_language": new_strong,
        "status": "ok" if not errors else "failed",
        "errors": errors,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else ("OK" if not errors else "FAILED\n" + "\n".join(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
