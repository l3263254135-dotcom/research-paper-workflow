import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN = Path(os.environ.get("PAPER_WORKFLOW_PLUGIN", Path(__file__).resolve().parents[1]))


class ReadinessTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def record(self, rel, obj):
        self.write(rel, json.dumps(obj))  # JSON is also valid YAML.

    def digest(self, rel):
        return hashlib.sha256((self.root / rel).read_bytes()).hexdigest()

    def audit(self, status, stage="review"):
        run = subprocess.run([sys.executable, str(PLUGIN / "scripts/build_workflow_report.py"),
                              str(self.root), "--stage", stage], text=True, capture_output=True)
        self.assertIn(run.returncode, (0, 1), run.stderr)
        self.assertTrue(run.stdout, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result, json.loads((self.root / "workflow_report.json").read_text()))
        self.assertEqual(result["status"], status, result["blockers"])
        self.assertEqual(run.returncode, int(bool(result["blockers"])))
        return "\n".join(result["blockers"])

    def controlled_fixture(self):
        self.record("project_manifest.yaml", {
            "project_id": "synthetic-test", "research_question": "Fixture question?",
            "target_journal": "Fictional test journal", "article_type": "Test article",
            "manuscript_mode": "standard", "status": "READY_FOR_REVIEW",
            "data_boundary": "local-only-until-authorized",
        })
        self.write("data/input.csv", "x\n1\n2\n3\n")
        self.write("runs/analysis.py", "# Non-executed synthetic record-checking fixture\n")
        digest = self.digest("data/input.csv")
        self.record("analysis_results.json", {"results": [{
            "result_id": "R1", "variable": "x", "unit": "count", "region": "fixture",
            "season": "all", "contrast": "one sample", "window": "fixture window", "n": 3,
            "estimate": 2, "ci_low": 1, "ci_high": 3, "test": "fixture", "p_exact": 0.5,
            "script_path": "runs/analysis.py", "input_hash": digest, "status": "verified",
            "input_files": {"data/input.csv": digest},
        }]})
        self.record("claims.yaml", [{"claim_id": "C1", "text": "Fixture claim", "status": "verified",
                                     "evidence_level": "source-backed", "evidence_ids": ["E1"],
                                     "result_ids": ["R1"], "figure_ids": ["F1"]}])
        self.record("figure_manifest.yaml", {"figures": [{"figure_id": "F1", "primary_claim_id": "C1",
                     "result_ids": ["R1"], "status": "approved", "caption": "Fixture caption",
                     "artifact_path": "figures/F1.txt"}]})
        self.write("figures/F1.txt", "Synthetic figure stand-in\n")
        self.write("draft.md", "# Fixture draft\n\nSynthetic result [from:R1] [claim:C1] [figure:F1].\n")
        self.write("provenance.md", "This is a synthetic fixture, not a scientific validation.\n")
        self.write("section_traceability.md", "Results: C1 uses R1 and F1.\n")
        package = json.loads((PLUGIN / "assets/submission-readiness-template.json").read_text())
        package["version"] = "fixture-v1"
        for role, entry in package["package"].items():
            entry["path"] = f"submission/{role}.txt"
            self.write(entry["path"], f"Synthetic stand-in for {role}.\n")
        for name, gate in package["gates"].items():
            note = f"checks/{name}.md"
            self.write(note, f"Simulated check: {name}; never use as real approval.\n")
            gate.update(status="verified", evidence=note, checked_by="fixture", checked_on="2026-11-23")
        package["sha256"] = {str(path.relative_to(self.root)): self.digest(path.relative_to(self.root))
                             for path in self.root.rglob("*") if path.is_file()}
        self.record("submission_readiness.json", package)
        return package

    def test_original_four_empty_records(self):
        for name in ("claims.yaml", "analysis_results.json", "project_manifest.yaml", "provenance.md"):
            self.write(name, "")
        self.assertIn("analysis_results.json: missing or empty", self.audit("BLOCKED"))

    def test_idea_only_scaffold(self):
        subprocess.run([sys.executable, str(PLUGIN / "scripts/scaffold_research_project.py"), str(self.root)],
                       check=True, capture_output=True)
        self.assertIn("analysis_results.json: no records", self.audit("BLOCKED"))
        self.audit("NOT_READY_FOR_SUBMISSION", "submission")
        self.assertFalse((self.root / "draft.md").exists())

    def test_complete_fixture_passes_both_local_stages(self):
        self.controlled_fixture()
        self.audit("READY_FOR_REVIEW")
        self.audit("READY_FOR_AUTHOR_SUBMISSION", "submission")

    def test_verified_result_requires_its_input(self):
        self.controlled_fixture()
        (self.root / "data/input.csv").unlink()
        self.assertIn("data/input.csv: missing", self.audit("NOT_READY_FOR_SUBMISSION", "submission"))

    def test_claim_must_link_to_verified_results(self):
        self.controlled_fixture()
        claims = json.loads((self.root / "claims.yaml").read_text())
        claims[0]["result_ids"] = ["R-missing"]
        self.record("claims.yaml", claims)
        self.assertIn("unknown or unverified ID 'R-missing'", self.audit("BLOCKED"))

    def test_draft_must_use_verified_ids(self):
        self.controlled_fixture()
        self.write("draft.md", "Draft result [from:R99] [claim:C1] [figure:F1].\n")
        self.assertIn("draft.md [from: ...]: unknown or unverified ID 'R99'", self.audit("BLOCKED"))

    def test_unverified_access_and_author_confirmation_block_submission(self):
        package = self.controlled_fixture()
        for gate in ("reviewer_access", "author_confirmation"):
            package["gates"][gate]["status"] = "pending"
        self.record("submission_readiness.json", package)
        self.audit("READY_FOR_REVIEW")
        blockers = self.audit("NOT_READY_FOR_SUBMISSION", "submission")
        self.assertIn("reviewer_access: not verified", blockers)
        self.assertIn("author_confirmation: not verified", blockers)

    def test_frozen_version_change_blocks_submission(self):
        self.controlled_fixture()
        self.write("submission/manuscript.txt", "Changed after checks.\n")
        self.assertIn("frozen SHA-256 mismatch", self.audit("NOT_READY_FOR_SUBMISSION", "submission"))

    def test_submission_requires_current_review_and_gate_manifest(self):
        package = self.controlled_fixture()
        del package["sha256"]["checks/reviewer_access.md"]
        self.record("submission_readiness.json", package)
        self.assertIn("omitted from frozen SHA-256 manifest", self.audit("NOT_READY_FOR_SUBMISSION", "submission"))

    def test_invalid_input_is_blocked(self):
        self.controlled_fixture()
        self.write("claims.yaml", "- [not-valid")
        self.assertIn("cannot read structured record", self.audit("BLOCKED"))

    def test_missing_science_recalculation_blocks_submission(self):
        package = self.controlled_fixture()
        package["gates"]["science_and_reproduction"]["status"] = "failed"
        self.record("submission_readiness.json", package)
        self.assertIn("science_and_reproduction: not verified",
                      self.audit("NOT_READY_FOR_SUBMISSION", "submission"))

    def test_skill_entry_and_routing(self):
        manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        skills = PLUGIN / manifest["skills"]
        self.assertTrue((skills / "idea-to-journal-paper/SKILL.md").is_file())
        router = (skills / "workflow-orchestrator/SKILL.md").read_text()
        for name in re.findall(r"\$([a-z][a-z-]+)", router):
            self.assertTrue((skills / name / "SKILL.md").is_file(), name)
        self.assertIn("claim_calibration.md", (skills / "cross-review/SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
