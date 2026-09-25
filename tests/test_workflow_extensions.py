#!/usr/bin/env python3
"""End-to-end checks for manuscript reconstruction and figure optimization assets."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "research-paper-workflow"
SCRIPTS = PLUGIN / "scripts"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPTS / name), *args], text=True, capture_output=True)


class WorkflowExtensionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "analysis_results.json").write_text(json.dumps({
            "schema_version": "1.0",
            "results": [{
                "result_id": "R001",
                "variable": "response",
                "unit": "mg",
                "region": "all",
                "season": "annual",
                "contrast": "A-B",
                "window": "2020-2024",
                "n": 20,
                "estimate": 4.2,
                "ci_low": 3.1,
                "ci_high": 5.0,
                "test": "Welch t-test",
                "p_exact": 0.03,
                "script_path": "runs/analyze.py",
                "input_hash": "abc123",
                "status": "verified"
            }]
        }, indent=2), encoding="utf-8")
        (self.root / "claims.yaml").write_text(
            "- claim_id: C001\n"
            "  text: \"The response differs between groups.\"\n"
            "  evidence_ids: [E001]\n"
            "  result_ids: [R001]\n"
            "  figure_ids: [F001]\n"
            "  evidence_level: source-backed\n"
            "  status: verified\n", encoding="utf-8")
        (self.root / "figure_manifest.yaml").write_text(
            "figures:\n"
            "  - figure_id: F001\n"
            "    role: primary_result\n"
            "    reader_question: What differs between groups?\n"
            "    title: Response by group\n"
            "    caption: Figure 1. (A) Response by group in mg; n=20; error bars show 95% confidence intervals; p=0.03.\n"
            "    primary_claim_id: C001\n"
            "    secondary_claim_ids: []\n"
            "    result_ids: [R001]\n"
            "    panel_roles: [A: primary comparison]\n"
            "    source_files: [data/response.csv]\n"
            "    analysis_script: runs/analyze.py\n"
            "    data_transform: group mean\n"
            "    sample_unit: participant\n"
            "    denominator: 20\n"
            "    time_window: 2020-2024\n"
            "    comparison_baseline: group B\n"
            "    units: [mg]\n"
            "    uncertainty_definition: 95% confidence interval\n"
            "    statistical_annotation: p=0.03\n"
            "    color_encoding: group\n"
            "    accessibility_check: passed\n"
            "    grayscale_check: passed\n"
            "    manuscript_locations: [Results 1]\n"
            "    main_or_supplement: main\n"
            "    journal_constraints: []\n"
            "    status: verified\n", encoding="utf-8")
        (self.root / "figure_plan.yaml").write_text(
            "schema_version: \"1.0\"\n"
            "status: verified\n"
            "figure_sequence:\n"
            "  - figure_id: F001\n"
            "    role: primary_result\n"
            "    reader_question: What differs between groups?\n"
            "    primary_claim_id: C001\n"
            "    result_ids: [R001]\n"
            "    panel_order: [A]\n"
            "    main_or_supplement: main\n"
            "    manuscript_locations: [Results 1]\n"
            "    rationale: Establishes the main group contrast.\n", encoding="utf-8")
        (self.root / "story_spine.yaml").write_text(
            "schema_version: \"1.0\"\n"
            "status: verified\n"
            "core_question: Does the response differ between groups?\n"
            "core_claim: The response differs between groups.\n"
            "evidence_sequence:\n"
            "  - step_id: S001\n"
            "    question: What differs between groups?\n"
            "    result_ids: [R001]\n"
            "    figure_ids: [F001]\n"
            "    claim_ids: [C001]\n", encoding="utf-8")
        (self.root / "manuscript_source.md").write_text(
            "# Source\n\nThe response differs between groups [from: R001] [claim: C001]. "
            "The estimate is 4.2 mg (95% CI 3.1–5.0, n=20, p=0.03).\n", encoding="utf-8")
        (self.root / "manuscript_reconstructed.md").write_text(
            "# Reconstructed\n\nThe response differs between groups [from: R001] [claim: C001]. "
            "The estimate is 4.2 mg (95% CI 3.1–5.0, n=20, p=0.03).\n", encoding="utf-8")
        (self.root / "reconstruction_config.yaml").write_text(
            "mode: reconstruction\nreconstruction_approval: approved\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_positive_traceability_and_reconstruction(self):
        checks = [
            run_script("validate_story_traceability.py", str(self.root / "story_spine.yaml"), str(self.root / "analysis_results.json"), str(self.root / "claims.yaml"), str(self.root / "figure_manifest.yaml")),
            run_script("validate_figure_plan.py", str(self.root / "figure_plan.yaml")),
            run_script("validate_figure_manifest.py", str(self.root / "figure_manifest.yaml"), "--strict"),
            run_script("validate_figure_caption.py", str(self.root / "figure_manifest.yaml")),
            run_script("validate_fact_preservation.py", str(self.root / "manuscript_source.md"), str(self.root / "manuscript_reconstructed.md")),
            run_script("validate_reconstruction_output.py", str(self.root / "manuscript_source.md"), str(self.root / "manuscript_reconstructed.md"), "--config", str(self.root / "reconstruction_config.yaml")),
        ]
        for result in checks:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_drift_and_caption_fail(self):
        bad = self.root / "bad.md"
        bad.write_text("The response causes a new mechanism; estimate 4.2 mg and p=0.03.", encoding="utf-8")
        result = run_script("validate_reconstruction_output.py", str(self.root / "manuscript_source.md"), str(bad), "--config", str(self.root / "reconstruction_config.yaml"))
        self.assertNotEqual(result.returncode, 0)
        manifest = self.root / "bad_manifest.yaml"
        manifest.write_text((self.root / "figure_manifest.yaml").read_text(encoding="utf-8").replace("in mg;", "in units;"), encoding="utf-8")
        result = run_script("validate_figure_caption.py", str(manifest))
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
