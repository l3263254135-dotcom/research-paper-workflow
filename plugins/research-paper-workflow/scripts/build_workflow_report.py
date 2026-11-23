#!/usr/bin/env python3
"""Check local review and submission records; never submit or certify science."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from validate_analysis_results import REQ, finite


SUBMISSION_GATES = (
    "science_and_reproduction", "package_consistency", "reviewer_access",
    "journal_requirements", "author_confirmation",
)
PACKAGE_ROLES = ("manuscript", "supporting_information", "reproduction_package", "cover_letter")


def filled(value):
    return (isinstance(value, str) and bool(value.strip())
            and value.strip().casefold() not in {"pending", "tbd", "todo", "placeholder"})


def write_report(path, text):
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        staged = Path(stream.name)
        try:
            stream.write(text)
            stream.close()
            staged.replace(path)
        finally:
            staged.unlink(missing_ok=True)


class Audit:
    def __init__(self, root, yaml):
        self.root = root.resolve()
        self.yaml = yaml
        self.errors = []
        self.files = set()
        self.checks = {}

    def file(self, rel, *, track=True):
        if not filled(rel):
            self.errors.append("missing or invalid file path")
            return None
        path = self.root / rel
        try:
            if Path(rel).is_absolute() or ".." in Path(rel).parts or not path.resolve().is_relative_to(self.root):
                self.errors.append(f"{rel}: expected a project-local path")
                return None
            if path.resolve().name in {"workflow_report.json", "workflow_report.md"}:
                self.errors.append(f"{rel}: generated status reports are not evidence")
                return None
            if not path.is_file() or path.stat().st_size == 0:
                self.errors.append(f"{rel}: missing or empty file")
                return None
        except (OSError, ValueError, RuntimeError) as exc:
            self.errors.append(f"{rel}: {exc}")
            return None
        if track:
            self.files.add(path.relative_to(self.root).as_posix())
        return path

    def load(self, rel, kind, *, track=True):
        path = self.file(rel, track=track)
        if path is None:
            return kind()
        try:
            text = path.read_text(encoding="utf-8")
            obj = json.loads(text) if path.suffix == ".json" else self.yaml.safe_load(text)
        except (OSError, ValueError, RecursionError, self.yaml.YAMLError) as exc:
            self.errors.append(f"{rel}: cannot read structured record ({exc})")
            return kind()
        if not isinstance(obj, kind) or not obj:
            self.errors.append(f"{rel}: expected non-empty {kind.__name__}")
            return kind()
        return obj

    def markdown(self, rel):
        path = self.file(rel)
        if path is None:
            return ""
        try:
            text = path.read_text(encoding="utf-8")
            if not any(filled(line.strip()) and not line.lstrip().startswith("#")
                       for line in text.splitlines()):
                self.errors.append(f"{rel}: no content beyond headings")
            return text
        except (OSError, UnicodeError) as exc:
            self.errors.append(f"{rel}: cannot read text ({exc})")
            return ""

    def digest(self, path):
        try:
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            return digest.hexdigest()
        except OSError as exc:
            self.errors.append(f"{path.relative_to(self.root)}: cannot hash file ({exc})")
            return None

    def links(self, label, values, known):
        if not isinstance(values, list) or not values:
            self.errors.append(f"{label}: requires at least one ID")
        else:
            for value in values:
                if not filled(value) or value not in known:
                    self.errors.append(f"{label}: unknown or unverified ID {value!r}")

    def verified_rows(self, rows, key, label, accepted=("verified",)):
        verified = {}
        seen = set()
        if not isinstance(rows, list) or not rows:
            self.errors.append(f"{label}: no records")
            return verified
        for row in rows:
            if not isinstance(row, dict) or not filled(row.get(key)):
                self.errors.append(f"{label}: missing {key}")
                continue
            uid = row[key]
            if uid in seen:
                self.errors.append(f"{label}: duplicate ID {uid}")
            seen.add(uid)
            if row.get("status") in accepted:
                verified[uid] = row
        if not verified:
            self.errors.append(f"{label}: no verified records")
        return verified

    def review(self):
        manifest = self.load("project_manifest.yaml", dict)
        for key in ("project_id", "research_question", "target_journal", "article_type"):
            if not filled(manifest.get(key)):
                self.errors.append(f"project_manifest.yaml: missing {key}")
        status = manifest.get("status")
        if status != "READY_FOR_REVIEW":
            self.errors.append("project_manifest.yaml: status must be READY_FOR_REVIEW")
        if manifest.get("data_boundary") != "local-only-until-authorized":
            self.errors.append("project_manifest.yaml: local data boundary is required")
        self.markdown("provenance.md")

        results = self.verified_rows(self.load("analysis_results.json", dict).get("results"),
                                     "result_id", "analysis_results.json")
        for uid, row in results.items():
            fields = ("variable", "unit", "region", "season", "contrast", "window", "test")
            if set(REQ) - row.keys() or not all(filled(row.get(key)) for key in fields):
                self.errors.append(f"{uid}: incomplete result metadata")
            n, estimate, low, high, p = (row.get(key) for key in ("n", "estimate", "ci_low", "ci_high", "p_exact"))
            if not (type(n) is int and n > 0 and all(finite(x) for x in (estimate, low, high, p))
                    and low <= high and 0 <= p <= 1):
                self.errors.append(f"{uid}: invalid sample size, estimate, interval or p-value")
            self.file(row.get("script_path"))
            inputs = row.get("input_files")
            if not isinstance(inputs, dict) or not inputs:
                self.errors.append(f"{uid}: input_files must map local inputs to SHA-256")
            else:
                for rel, expected in inputs.items():
                    path = self.file(rel)
                    if path is not None and (not filled(expected) or self.digest(path) != expected):
                        self.errors.append(f"{uid}: input checksum mismatch for {rel}")

        claims = self.verified_rows(self.load("claims.yaml", list), "claim_id", "claims.yaml")
        figures = self.verified_rows(self.load("figure_manifest.yaml", dict).get("figures"),
                                     "figure_id", "figure_manifest.yaml", ("verified", "approved"))
        for uid, row in claims.items():
            if (not filled(row.get("text")) or row.get("evidence_level") not in ("source-backed", "inference")
                    or not isinstance(row.get("evidence_ids"), list) or not row["evidence_ids"]
                    or not all(filled(item) for item in row["evidence_ids"])):
                self.errors.append(f"{uid}: missing claim text or evidence")
            self.links(f"{uid} result_ids", row.get("result_ids"), results)
            self.links(f"{uid} figure_ids", row.get("figure_ids"), figures)
        for uid, row in figures.items():
            self.links(f"{uid} primary_claim_id", [row.get("primary_claim_id")], claims)
            self.links(f"{uid} result_ids", row.get("result_ids"), results)
            primary = row.get("primary_claim_id")
            if filled(primary) and primary in claims:
                linked_claim = claims[primary]
                ids = linked_claim.get("figure_ids")
                if not isinstance(ids, list) or uid not in ids:
                    self.errors.append(f"{uid}: {primary} does not link back to the figure")
                claim_results = linked_claim.get("result_ids")
                figure_results = row.get("result_ids")
                if (isinstance(claim_results, list) and isinstance(figure_results, list)
                        and not any(rid in claim_results for rid in figure_results)):
                    self.errors.append(f"{uid}: shares no result with {primary}")
            if not filled(row.get("caption")):
                self.errors.append(f"{uid}: caption is missing")
            self.file(row.get("artifact_path"))

        mode = manifest.get("manuscript_mode", "standard")
        if (self.root / "figure_plan.yaml").exists():
            plan = self.load("figure_plan.yaml", dict)
            if plan.get("status") == "blocked" or plan.get("status") == "BLOCKED":
                self.errors.append("figure_plan.yaml: figure plan is blocked")
        if mode == "reconstruction":
            self.markdown(manifest.get("source_manuscript", "manuscript_source.md"))
            state = self.load("reconstruction_status.yaml", dict)
            approvals = (manifest.get("reconstruction_approval"), state.get("reconstruction_approval"))
            if "approved" not in approvals or state.get("status") != "READY_FOR_REVIEW":
                self.errors.append("reconstruction: requires author approval and READY_FOR_REVIEW status")
        elif mode != "standard":
            self.errors.append("project_manifest.yaml: invalid manuscript_mode")
        draft_name = "manuscript_reconstructed.md" if mode == "reconstruction" else "draft.md"
        draft = self.markdown(draft_name)
        self.markdown("section_traceability.md")
        if draft:
            for marker, known in (("from", results), ("claim", claims), ("figure", figures)):
                ids = [match.strip() for match in re.findall(rf"\[{marker}:\s*([^\]\n]+)\]", draft)]
                self.links(f"{draft_name} [{marker}: ...]", ids, known)
            if "[NUMBER_NEEDED]" in draft:
                self.errors.append(f"{draft_name}: unresolved NUMBER_NEEDED marker")
        self.checks["review_records_valid"] = not self.errors

    def submission(self):
        report = self.load("submission_readiness.json", dict, track=False)
        if self.errors or not report:
            return
        if not filled(report.get("version")):
            self.errors.append("submission_readiness.json: missing frozen version")
        package = report.get("package")
        if not isinstance(package, dict):
            package = {}
        paths = set()
        for role in PACKAGE_ROLES:
            entry = package.get(role)
            if not isinstance(entry, dict):
                self.errors.append(f"{role}: missing package entry")
                continue
            if (role in {"supporting_information", "cover_letter"} and entry.get("status") == "not_applicable"
                    and filled(entry.get("reason")) and "path" not in entry):
                continue
            rel = entry.get("path")
            if self.file(rel):
                canonical = (self.root / rel).resolve()
                if canonical in paths:
                    self.errors.append(f"{role}: package file reused for another role")
                paths.add(canonical)

        gates = report.get("gates")
        if not isinstance(gates, dict):
            gates = {}
        for name in SUBMISSION_GATES:
            gate = gates.get(name)
            if not isinstance(gate, dict) or gate.get("status") != "verified":
                self.errors.append(f"{name}: not verified")
                continue
            if not all(filled(gate.get(key)) for key in ("checked_by", "checked_on")):
                self.errors.append(f"{name}: missing checker or date")
            self.markdown(gate.get("evidence"))

        hashes = report.get("sha256")
        if not isinstance(hashes, dict) or not hashes:
            self.errors.append("submission_readiness.json: frozen SHA-256 manifest missing")
            return
        for rel in sorted(self.files - hashes.keys()):
            self.errors.append(f"{rel}: omitted from frozen SHA-256 manifest")
        for rel, expected in hashes.items():
            path = self.file(rel, track=False)
            if path is not None and (not filled(expected) or self.digest(path) != expected):
                self.errors.append(f"{rel}: frozen SHA-256 mismatch")
        self.checks["submission_records_valid"] = not self.errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--stage", choices=("review", "submission"), default="review")
    args = parser.parse_args()
    if not args.project.is_dir():
        parser.error("project must be an existing directory")
    try:
        import yaml
    except ImportError:
        audit = Audit(args.project, None)
        audit.errors.append("PyYAML is required; install the dependency in your Python environment")
    else:
        audit = Audit(args.project, yaml)
        audit.review()
        if args.stage == "submission" and not audit.errors:
            audit.submission()
    if args.stage == "submission":
        status = "NOT_READY_FOR_SUBMISSION" if audit.errors else "READY_FOR_AUTHOR_SUBMISSION"
    else:
        status = "BLOCKED" if audit.errors else "READY_FOR_REVIEW"
    report = {"project": str(audit.root), "stage": args.stage, "status": status,
              "checks": audit.checks, "blockers": audit.errors}
    output = json.dumps(report, ensure_ascii=False, indent=2)
    write_report(audit.root / "workflow_report.json", output + "\n")
    blockers = "\n".join(f"- {error}" for error in audit.errors) or "- None"
    write_report(audit.root / "workflow_report.md",
        f"# Workflow Report\n\n- Stage: {args.stage}\n- Status: **{status}**\n\n## Blockers\n{blockers}\n",
    )
    print(output)
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
