#!/usr/bin/env python3
"""Check that project records use the declared provenance vocabulary."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

LABELS = {"BOOK-SUPPORTED", "ARTICLE-SUPPORTED", "INTERNAL-BASELINE", "OUR-DESIGN", "BLOCKED-SOURCE"}

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("root", type=Path); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); files = [p for p in args.root.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml", ".json", ".txt"}]
    text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in files)
    found = sorted(set(re.findall(r"[A-Z][A-Z-]+", text)) & LABELS)
    errors = [] if "provenance.md" in {p.name for p in files} else ["provenance.md missing"]
    if not found:
        errors.append("no provenance labels found")
    out = {"root": str(args.root), "labels_found": found, "files_checked": len(files), "errors": errors, "status": "ok" if not errors else "failed"}
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else ("OK" if not errors else "FAILED\n" + "\n".join(errors)))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
