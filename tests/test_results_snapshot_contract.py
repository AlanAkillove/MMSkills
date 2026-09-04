"""Frozen result snapshots must go stale when the source file changes."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "math-modeling" / "scripts" / "results"
FIXTURES = ROOT / "tests" / "fixtures" / "math-modeling"


def test_stale_source_hash_is_detected(tmp_path: Path):
    snapshot = tmp_path / "snapshot.json"
    freeze = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "freeze_results.py"),
            "--source",
            str(FIXTURES / "metrics-old.json"),
            "--locator",
            "$.thermal_resistance",
            "--claim-id",
            "thermal_resistance",
            "--unit",
            "K/W",
            "--scope",
            "Q3",
            "--output",
            str(snapshot),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert freeze.returncode == 0, freeze.stderr
    payload = json.loads(snapshot.read_text(encoding="utf-8"))
    claim = payload["claims"][0]
    assert claim["value"] == 2.4
    assert claim["status"] == "snapshot"
    assert claim["human_status"] == "unreviewed"
    assert claim["decision_id"] is None
    assert claim["source_file"] == "tests/fixtures/math-modeling/metrics-old.json"
    fresh = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "check_result_freshness.py"),
            "--snapshot",
            str(snapshot),
            "--source",
            str(FIXTURES / "metrics-old.json"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert fresh.returncode == 0, fresh.stdout + fresh.stderr
    stale = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "check_result_freshness.py"),
            "--snapshot",
            str(snapshot),
            "--source",
            str(FIXTURES / "metrics-new.json"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert stale.returncode == 1
    assert "stale snapshot" in stale.stdout


def test_frozen_status_requires_human_decision_id(tmp_path: Path):
    snapshot = tmp_path / "snapshot.json"
    blocked = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "freeze_results.py"),
            "--source",
            str(FIXTURES / "metrics-old.json"),
            "--locator",
            "$.thermal_resistance",
            "--claim-id",
            "thermal_resistance",
            "--status",
            "frozen",
            "--output",
            str(snapshot),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert blocked.returncode != 0
    assert not snapshot.exists()
    wrote = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "freeze_results.py"),
            "--source",
            str(FIXTURES / "metrics-old.json"),
            "--locator",
            "$.thermal_resistance",
            "--claim-id",
            "thermal_resistance",
            "--status",
            "frozen",
            "--decision-id",
            "DEC-freeze-1",
            "--output",
            str(snapshot),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert wrote.returncode == 0, wrote.stderr
    claim = json.loads(snapshot.read_text(encoding="utf-8"))["claims"][0]
    assert claim["status"] == "frozen"
    assert claim["decision_id"] == "DEC-freeze-1"
    assert claim["human_status"] == "confirmed"


def test_source_outside_repo_requires_explicit_allow(tmp_path: Path):
    outside = tmp_path / "metrics.json"
    outside.write_bytes((FIXTURES / "metrics-old.json").read_bytes())
    snapshot = tmp_path / "snapshot.json"
    blocked = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "freeze_results.py"),
            "--source",
            str(outside),
            "--locator",
            "$.thermal_resistance",
            "--claim-id",
            "thermal_resistance",
            "--repo-root",
            str(ROOT),
            "--output",
            str(snapshot),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert blocked.returncode == 2
    assert "outside repo root" in blocked.stdout
    assert not snapshot.exists()
    allowed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "freeze_results.py"),
            "--source",
            str(outside),
            "--locator",
            "$.thermal_resistance",
            "--claim-id",
            "thermal_resistance",
            "--repo-root",
            str(ROOT),
            "--allow-external-source",
            "--output",
            str(snapshot),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert allowed.returncode == 0, allowed.stderr
    source_file = json.loads(snapshot.read_text(encoding="utf-8"))["claims"][0]["source_file"]
    assert Path(source_file).is_absolute()
