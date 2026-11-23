#!/usr/bin/env python3
"""Exercise a real-data package locally, without journal or author attestations."""
import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from decimal import Decimal
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pypdf import PdfReader


URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
PLUGIN = Path(os.environ.get("PAPER_WORKFLOW_PLUGIN", Path(__file__).resolve().parents[1]))
ANALYSIS = '''\
import csv
import hashlib
import json
from pathlib import Path
from scipy.stats import ttest_ind

def main():
    path = Path(__file__).resolve().parent / "data/gistemp.csv"
    with path.open(newline="", encoding="utf-8") as stream:
        next(stream)
        rows = {int(row["Year"]): float(row["J-D"]) for row in csv.DictReader(stream)
                if 1981 <= int(row["Year"]) <= 2020}
    early = [rows[year] for year in range(1981, 2001)]
    late = [rows[year] for year in range(2001, 2021)]
    test = ttest_ind(late, early, equal_var=False)
    ci = test.confidence_interval()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps({"result_id": "R001", "variable": "Annual GISTEMP anomaly",
        "unit": "deg C", "region": "global", "season": "annual", "contrast": "late minus early",
        "window": "1981-2000 and 2001-2020", "n": len(early) + len(late),
        "estimate": sum(late)/len(late) - sum(early)/len(early),
        "ci_low": float(ci.low), "ci_high": float(ci.high), "p_exact": float(test.pvalue),
        "test": "Welch t-test (nominal only, not temporal-dependence adjusted)",
        "script_path": "analyze.py", "input_files": {"data/gistemp.csv": digest},
        "input_hash": digest, "status": "verified"}))

if __name__ == "__main__":
    main()
'''


def pdf(path, title, text, figure=None):
    with PdfPages(path) as output:
        page = plt.figure(figsize=(8.27, 11.69))
        page.text(0.1, 0.95, title, size=13, va="top")
        body = "\n\n".join(textwrap.fill(paragraph, 85) for paragraph in text.split("\n\n"))
        page.text(0.1, 0.9, body, va="top", size=10, linespacing=1.5)
        output.savefig(page)
        plt.close(page)
        if figure is not None:
            output.savefig(figure)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="A new directory for the smoke test")
    root = parser.parse_args().output.resolve()
    root.mkdir()

    def write(rel, text):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")

    def record(rel, value):
        write(rel, json.dumps(value, indent=2))

    def run(rel, *args, check=True):
        return subprocess.run([sys.executable, str(rel), *map(str, args)],
                              cwd=root, text=True, capture_output=True, check=check)

    def audit(stage, expected):
        result = run(PLUGIN / "scripts/build_workflow_report.py", root, "--stage", stage, check=False)
        if not result.stdout:
            raise RuntimeError(result.stderr)
        report = json.loads(result.stdout)
        assert report["status"] == expected, report
        record(f"acceptance/{stage}-{expected}.json", report)
        print(f"{stage}: {expected}")
        return report["blockers"]

    write("research_question.md", "In GISTEMP v4, how much higher or lower is the global annual "
          "mean anomaly in 2001-2020 than 1981-2000? Compare period means; only describe this record.")
    audit("review", "BLOCKED")
    assert not (root / "draft.md").exists()
    raw = root / "data/gistemp.csv"
    raw.parent.mkdir()
    subprocess.run(["curl", "-fsSL", "--max-time", "30", "--output", str(raw), URL], check=True)
    write("analyze.py", ANALYSIS)
    result = json.loads(run(root / "analyze.py").stdout)

    # Independently recalculate the point estimate using decimal CSV columns.
    with raw.open(newline="", encoding="utf-8") as stream:
        next(stream)
        columns = csv.reader(stream)
        annual = next(columns).index("J-D")
        series = [(int(row[0]), Decimal(row[annual])) for row in columns if 1981 <= int(row[0]) <= 2020]
    assert len(series) == 40
    means = [sum(value for year, value in series if start <= year <= end) / 20
             for start, end in ((1981, 2000), (2001, 2020))]
    difference = means[1] - means[0]
    assert abs(difference - Decimal(str(result["estimate"]))) < Decimal("0.000000001")
    claim = f"The 2001-2020 period mean is {difference:+.3f} deg C relative to 1981-2000 in this GISTEMP snapshot."
    record("analysis_results.json", {"results": [result]})
    record("project_manifest.yaml", {"project_id": "public-data-smoke", "research_question": "How do the period means differ?",
            "target_journal": "Local smoke-test target, not a real submission", "article_type": "Research note",
            "data_boundary": "local-only-until-authorized", "status": "READY_FOR_REVIEW"})
    write("provenance.md", f"Public GISTEMP v4 CSV: {URL}\n\nInput SHA-256: {result['input_hash']}")
    record("claims.yaml", [{"claim_id": "C001", "text": claim, "evidence_level": "source-backed",
            "evidence_ids": ["E001"], "result_ids": ["R001"], "figure_ids": ["F001"], "status": "verified"}])
    record("figure_manifest.yaml", {"figures": [{"figure_id": "F001", "primary_claim_id": "C001",
            "result_ids": ["R001"], "caption": "Annual global anomalies and period means.",
            "artifact_path": "figures/F001.pdf", "status": "verified"}]})
    write("section_traceability.md", "Results [from:R001] [claim:C001] [figure:F001].")

    body = (f"Abstract. {claim}\n\n"
            "Introduction. This example compares two fixed time windows in a public climate record. "
            "It is a workflow validation, not an original scientific contribution.\n\n"
            "Methods. We compare the published J-D annual anomalies, using 20 years in each period. "
            "The contrast is the later arithmetic mean minus the earlier arithmetic mean.\n\n"
            f"Results. The period means are {means[0]:.3f} and {means[1]:.3f} deg C. See Figure 1.\n\n"
            "Discussion. The selected windows and product define the result. The nominal Welch statistics "
            "in the reproducibility records do not account for temporal dependence and are not used for attribution.\n\n"
            f"Data and code. NASA GISS GISTEMP v4: {URL}. See the bundled CSV, script and environment record.")
    write("draft.md", body + "\n\nResults trace: [from:R001] [claim:C001] [figure:F001].")
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    ax.plot([year for year, _ in series], [float(value) for _, value in series], color="#25566c")
    ax.hlines(list(map(float, means)), [1981, 2001], [2000, 2020], color="#bb4d24", linewidth=2)
    ax.set(xlabel="Year", ylabel="Annual anomaly (deg C)", title="Figure 1. Annual anomalies and period means")
    (root / "figures").mkdir()
    fig.savefig(root / "figures/F001.pdf")
    (root / "submission").mkdir()
    pdf(root / "submission/manuscript.pdf", "Global temperature period comparison", body, fig)
    plt.close(fig)
    pdf(root / "submission/SI.pdf", "Supporting Information", f"CSV SHA-256: {result['input_hash']}\n\n"
        f"Nominal Welch interval: {result['ci_low']:.3f} to {result['ci_high']:.3f} deg C. "
        "This is not corrected for serial dependence. The point estimate is verified by an independent decimal recalculation.")
    write("submission/cover-letter.txt", "Local software acceptance only. Do not send to a journal.")
    import scipy

    write("reproduction-requirements.txt", f"scipy=={scipy.__version__}")
    package_files = ("analyze.py", "data/gistemp.csv", "analysis_results.json", "provenance.md",
                     "reproduction-requirements.txt")
    zip_path = root / "submission/reproduction.zip"
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as bundle:
        for rel in package_files:
            bundle.write(root / rel, rel)
    with tempfile.TemporaryDirectory() as temp, ZipFile(zip_path) as bundle:
        assert bundle.testzip() is None
        bundle.extractall(temp)
        assert json.loads(run(Path(temp) / "analyze.py").stdout) == result
    assert len(PdfReader(root / "submission/manuscript.pdf").pages) == 2
    assert f"{difference:+.3f}" in PdfReader(root / "submission/manuscript.pdf").pages[0].extract_text()
    assert "Welch" in PdfReader(root / "submission/SI.pdf").pages[0].extract_text()

    package = json.loads((PLUGIN / "assets/submission-readiness-template.json").read_text())
    package["version"] = "public-data-smoke-v1"
    for role, name in zip(package["package"], ("manuscript.pdf", "SI.pdf", "reproduction.zip", "cover-letter.txt")):
        package["package"][role]["path"] = f"submission/{name}"
    package["sha256"] = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in root.rglob("*") if path.is_file() and path.parts[-2] != "acceptance"
                         and not path.name.startswith("workflow_report.")}
    record("submission_readiness.json", package)
    audit("review", "READY_FOR_REVIEW")
    blockers = audit("submission", "NOT_READY_FOR_SUBMISSION")
    assert "reviewer_access: not verified" in blockers and "author_confirmation: not verified" in blockers
    saved = raw.with_suffix(".disabled")
    raw.rename(saved)
    try:
        blockers = audit("submission", "NOT_READY_FOR_SUBMISSION")
        assert any("data/gistemp.csv: missing or empty" in error for error in blockers)
        (root / "acceptance/submission-NOT_READY_FOR_SUBMISSION.json").rename(root / "acceptance/missing-input.json")
    finally:
        saved.rename(raw)
    audit("submission", "NOT_READY_FOR_SUBMISSION")
    print(f"Independent GISTEMP contrast: {difference:+.3f} deg C. Verified PDFs and clean ZIP replay: {root}")


if __name__ == "__main__":
    main()
