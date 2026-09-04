"""Contract checks for 0.3.0 workbench tools: runs, figures, citations, probes, preflight glue."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "math-modeling" / "scripts"
FIXTURES = ROOT / "tests" / "fixtures" / "math-modeling"
PREFLIGHT = ROOT / "skills" / "modeling-final-preflight" / "scripts"
sys.path.insert(0, str(SCRIPTS / "figures"))
from check_figure_placement import write_png  # noqa: E402


def run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(script), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_run_summary_rejects_scores_and_accepts_outputs(tmp_path: Path):
    script = SCRIPTS / "results" / "write_run_summary.py"
    good = tmp_path / "run.json"
    wrote = run(
        script,
        "--run-id",
        "r1",
        "--status",
        "ok",
        "--output-json",
        '{"rmse": 2.18}',
        "--output",
        str(good),
    )
    assert wrote.returncode == 0, wrote.stderr
    env = json.loads(good.read_text(encoding="utf-8"))["environment"]
    assert env["python"]
    assert env["os"]
    assert "git_revision" in env
    assert json.loads(good.read_text(encoding="utf-8"))["outputs"]["rmse"] == 2.18
    bad = tmp_path / "scored.json"
    bad.write_text(
        json.dumps({"run_id": "r2", "status": "ok", "outputs": {"x": 1}, "overall_score": 99}),
        encoding="utf-8",
    )
    rejected = run(script, "--validate", str(bad))
    assert rejected.returncode == 1
    assert "overall_score" in rejected.stdout


def test_diagnostic_figure_cannot_enter_body_and_png_geometry_is_read(tmp_path: Path):
    script = SCRIPTS / "figures" / "check_figure_placement.py"
    blocked = run(script, "--manifest", str(FIXTURES / "figure-diagnostic-in-body.yaml"))
    assert blocked.returncode == 1
    assert "diagnostic" in blocked.stdout
    allowed = run(script, "--manifest", str(FIXTURES / "figure-paper.yaml"))
    assert allowed.returncode == 0, allowed.stderr
    png = tmp_path / "tiny.png"
    write_png(png, 12, 8)
    geo = run(
        script,
        "--manifest",
        str(FIXTURES / "figure-paper.yaml"),
        "--image",
        str(png),
        "--min-width",
        "20",
        "--json-out",
        str(tmp_path / "geo.json"),
    )
    assert geo.returncode == 1
    payload = json.loads((tmp_path / "geo.json").read_text(encoding="utf-8"))
    assert payload["images"][0]["width"] == 12
    assert payload["images"][0]["height"] == 8


def test_doi_normalize_and_local_citation_compare():
    script = SCRIPTS / "evidence" / "citations.py"
    doi = run(script, "normalize-doi", "https://doi.org/10.1234/Example.Paper")
    assert doi.returncode == 0
    assert doi.stdout.strip() == "10.1234/example.paper"
    matched = run(
        script,
        "compare",
        "--claimed",
        str(FIXTURES / "citation-claimed.json"),
        "--fetched",
        str(FIXTURES / "citation-fetched.json"),
    )
    assert matched.returncode == 0, matched.stdout + matched.stderr
    mismatched = run(
        script,
        "compare",
        "--claimed",
        str(FIXTURES / "citation-claimed.json"),
        "--fetched",
        str(FIXTURES / "citation-mismatch.json"),
    )
    assert mismatched.returncode == 1
    assert "title mismatch" in mismatched.stdout
    official = run(
        script,
        "compare",
        "--claimed",
        str(FIXTURES / "citation-no-doi-claimed.json"),
        "--fetched",
        str(FIXTURES / "citation-no-doi-fetched.json"),
    )
    assert official.returncode == 0, official.stdout + official.stderr
    assert "DOI absent" in official.stdout


def test_feasibility_probe_rejects_scoring():
    script = SCRIPTS / "model" / "check_feasibility_probe.py"
    ok = run(script, "--probe", str(FIXTURES / "feasibility-ok.json"))
    assert ok.returncode == 0, ok.stderr
    scored = run(script, "--probe", str(FIXTURES / "feasibility-scored.json"))
    assert scored.returncode == 1
    assert "overall_score" in scored.stdout


def test_preflight_workbench_glue_flags_stale_numbers_and_wrapper_terms(
    tmp_path: Path,
):
    snapshot = tmp_path / "snapshot.json"
    freeze = run(
        SCRIPTS / "results" / "freeze_results.py",
        "--source",
        str(FIXTURES / "metrics-old.json"),
        "--locator",
        "$.thermal_resistance",
        "--claim-id",
        "thermal_resistance",
        "--unit",
        "K/W",
        "--output",
        str(snapshot),
    )
    assert freeze.returncode == 0, freeze.stderr
    term_dir = ROOT / "tests" / "fixtures" / "modeling-terminology-auditor"
    result = run(
        PREFLIGHT / "check_workbench_artifacts.py",
        "--snapshot",
        str(snapshot),
        "--snapshot-source",
        str(FIXTURES / "metrics-new.json"),
        "--terminology-table",
        str(term_dir / "table-flow-maldistribution.md"),
        "--manuscript",
        str(term_dir / "manuscript-wrapper-term.tex"),
        "--figure-manifest",
        str(FIXTURES / "figure-diagnostic-in-body.yaml"),
        "--claimed-citation",
        str(FIXTURES / "citation-claimed.json"),
        "--fetched-citation",
        str(FIXTURES / "citation-fetched.json"),
        "--json-out",
        str(tmp_path / "preflight.json"),
    )
    assert result.returncode == 1
    payload = json.loads((tmp_path / "preflight.json").read_text(encoding="utf-8"))
    blob = " ".join(payload["errors"])
    assert "stale snapshot" in blob
    assert "diagnostic" in blob
    assert "terminology" in blob


def test_preflight_glue_zero_checks_is_unassessed_not_ok():
    result = run(PREFLIGHT / "check_workbench_artifacts.py")
    assert result.returncode == 2
    assert "UNASSESSED" in result.stdout
    assert "OK: workbench artifacts" not in result.stdout
    assert "checks_run" in result.stdout
