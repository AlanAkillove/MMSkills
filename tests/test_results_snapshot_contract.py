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
    assert payload["value"] == 2.4
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
