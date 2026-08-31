from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEHAVIORAL = ROOT / "tests" / "behavioral"
SCRIPT = BEHAVIORAL / "validate_behavior.py"
CASES = json.loads((BEHAVIORAL / "cases.json").read_text(encoding="utf-8"))


def run(case_id: str, kind: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--case",
            case_id,
            "--response",
            str(BEHAVIORAL / kind / f"{case_id}.json"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def test_behavioral_case_inventory_is_unique_and_has_prompts():
    ids = [case["case_id"] for case in CASES]
    assert len(ids) == len(set(ids))
    assert all(case.get("prompt") and case.get("target_skill") for case in CASES)
    assert (BEHAVIORAL / "response-envelope.schema.json").exists()


def test_positive_behavioral_responses_pass_structural_checks():
    for case in CASES:
        result = run(case["case_id"], "positive")
        assert result.returncode == 0, result.stdout + result.stderr
        assert f"PASS {case['case_id']}" in result.stdout


def test_negative_behavioral_responses_are_rejected():
    for case in CASES:
        result = run(case["case_id"], "negative")
        assert result.returncode != 0
        assert f"FAIL {case['case_id']}" in result.stdout


def test_missing_external_agent_responses_are_not_counted_as_pass(tmp_path: Path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--responses-dir", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 3
    assert "MISSING RESPONSES" in result.stderr
