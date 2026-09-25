#!/usr/bin/env python3
"""Check that a reconstructed manuscript preserves source facts and identifiers."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NUMBER = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?%?")
ID = re.compile(r"\b(?:FACT|R|C|F|T|S)\d{2,}\b")


def tokens(text: str) -> list[str]:
    return NUMBER.findall(text)


def ids(text: str) -> set[str]:
    return set(ID.findall(text))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("reconstructed", type=Path)
    ap.add_argument("--ledger", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    source_text = args.source.read_text(encoding="utf-8", errors="replace")
    rebuilt_text = args.reconstructed.read_text(encoding="utf-8", errors="replace")
    ledger_text = args.ledger.read_text(encoding="utf-8", errors="replace") if args.ledger and args.ledger.exists() else ""

    source_numbers = sorted(set(tokens(source_text)))
    rebuilt_numbers = set(tokens(rebuilt_text))
    required_numbers = sorted(set(source_numbers) | set(tokens(ledger_text)))
    missing_numbers = [value for value in required_numbers if value not in rebuilt_numbers]

    required_ids = sorted(ids(source_text) | ids(ledger_text))
    rebuilt_ids = ids(rebuilt_text)
    missing_ids = [value for value in required_ids if value not in rebuilt_ids]

    errors = []
    if "[NUMBER_NEEDED]" in rebuilt_text:
        errors.append("reconstructed manuscript contains [NUMBER_NEEDED]")
    if missing_numbers:
        errors.append("missing numeric tokens: " + ", ".join(missing_numbers))
    if missing_ids:
        errors.append("missing identifiers: " + ", ".join(missing_ids))

    out = {
        "source": str(args.source),
        "reconstructed": str(args.reconstructed),
        "required_numbers": required_numbers,
        "missing_numbers": missing_numbers,
        "required_ids": required_ids,
        "missing_ids": missing_ids,
        "status": "ok" if not errors else "failed",
        "errors": errors,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2) if args.json else ("OK" if not errors else "FAILED\n" + "\n".join(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
