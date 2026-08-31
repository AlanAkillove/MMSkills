from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "modeling-process-freezer"
FIXTURES = ROOT / "tests" / "fixtures" / "modeling-process-freezer"
BUILD = SKILL / "scripts" / "build_state_manifest.py"
VALIDATE = SKILL / "scripts" / "validate_state_manifest.py"


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_skill_has_append_only_and_handoff_boundaries():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "append-only",
        "不能伪装成 frozen/released",
        "不要覆盖旧 manifest",
        "上下文被截断",
        "modeling-final-preflight",
    ):
        assert phrase in text


def test_references_and_scripts_exist():
    for path in (
        SKILL / "references" / "freeze-contract.md",
        SKILL / "references" / "state-transitions.md",
        SKILL / "references" / "handoff-and-integrity.md",
        SKILL / "references" / "research-basis.md",
        BUILD,
        VALIDATE,
    ):
        assert path.exists(), path


def test_manifest_build_and_hash_validation(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "paper.md").write_text("claim v1\n", encoding="utf-8")
    manifest = project / "project_state" / "freeze_manifest.json"
    built = run_script(
        BUILD,
        "--root", str(project),
        "--output", str(manifest),
        "--snapshot-id", "SNAP-TEST",
        "--state", "frozen",
        "--purpose", "human_gate",
        "--profile-id", "fixture-profile",
        "--decision-id", "DEC-TEST",
        "--confirmed-by", "fixture-author",
        "--confirmed-date", "2026-08-31",
        "--confirmation-scope", "paper.md",
    )
    assert built.returncode == 0, built.stderr
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["snapshot_id"] == "SNAP-TEST"
    assert data["files"][0]["path"] == "paper.md"
    checked = run_script(VALIDATE, "--root", str(project), "--manifest", str(manifest))
    assert checked.returncode == 0, checked.stdout

    (project / "paper.md").write_text("claim v2\n", encoding="utf-8")
    stale = run_script(VALIDATE, "--root", str(project), "--manifest", str(manifest))
    assert stale.returncode != 0
    assert "sha256 changed" in stale.stdout


def test_frozen_build_requires_human_confirmation(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    (project / "paper.md").write_text("text\n", encoding="utf-8")
    result = run_script(
        BUILD,
        "--root", str(project),
        "--output", str(tmp_path / "manifest.json"),
        "--state", "frozen",
    )
    assert result.returncode != 0
    assert "require --confirmed-by" in result.stderr


def test_fixtures_cover_unsigned_stale_and_unsafe_states():
    for name, phrase in (
        ("negative-unsigned-freeze.md", "pending"),
        ("negative-stale-hash.md", "old-hash"),
        ("negative-unsafe-path.md", ".."),
        ("negative-state-regression.md", "覆盖为 working"),
    ):
        assert phrase in (FIXTURES / name).read_text(encoding="utf-8")
