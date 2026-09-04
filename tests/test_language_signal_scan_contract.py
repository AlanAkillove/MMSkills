"""Mechanical language-signal scan emits candidates only, and must not flag academic folklore."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "modeling-ai-pattern-reviewer" / "scripts" / "scan_language_signals.py"
FIXTURES = ROOT / "tests" / "fixtures" / "modeling-ai-pattern-reviewer"
PREFLIGHT = ROOT / "skills" / "modeling-final-preflight" / "scripts"
sys.path.insert(0, str(SCRIPT.parent))
from scan_language_signals import scan_text  # noqa: E402


def test_false_positive_academic_constructions_are_not_candidates():
    text = (FIXTURES / "negative-false-positive-language.md").read_text(encoding="utf-8")
    ids = {item["signal_id"] for item in scan_text(text)}
    assert ids == set()


def test_positive_template_frames_are_candidates():
    reframe = scan_text((FIXTURES / "positive-reframe-packaging.md").read_text(encoding="utf-8"))
    empty = scan_text((FIXTURES / "positive-empty-colon.md").read_text(encoding="utf-8"))
    iso = scan_text((FIXTURES / "positive-iso-sentences.md").read_text(encoding="utf-8"))
    assert {item["signal_id"] for item in reframe} == {"SYN-REFRAME"}
    assert {item["signal_id"] for item in empty} == {"SYN-EMPTY-COLON"}
    assert {item["signal_id"] for item in iso} == {"SYN-ISO-SENT"}
    assert all(item["status"] == "candidate" for item in reframe + empty + iso)


def test_cli_and_preflight_glue_never_fail_on_candidates(tmp_path: Path):
    report = tmp_path / "signals.json"
    cli = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(SCRIPT),
            "--manuscript",
            str(FIXTURES / "positive-iso-sentences.md"),
            "--json-out",
            str(report),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert cli.returncode == 0, cli.stderr
    assert json.loads(report.read_text(encoding="utf-8"))[0]["status"] == "candidate"
    glue = tmp_path / "preflight.json"
    preflight = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(PREFLIGHT / "check_workbench_artifacts.py"),
            "--language-scan",
            str(FIXTURES / "positive-iso-sentences.md"),
            "--json-out",
            str(glue),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert preflight.returncode == 0, preflight.stdout + preflight.stderr
    assert "OK: workbench artifacts" in preflight.stdout
    payload = json.loads(glue.read_text(encoding="utf-8"))
    assert payload["errors"] == []
    assert payload["language_signal_candidates"]
    assert "SYN-ISO-SENT" in payload["warnings"][0]
