"""Thin DeepSeek Harness adapter must not rewrite source skills."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "hosts" / "deepseek-harness" / "sync_adapter.py"


def test_dsh_docs_are_optional_native_adapter():
    readme = (ROOT / "hosts" / "deepseek-harness" / "README.md").read_text(encoding="utf-8")
    for phrase in (
        "可选宿主适配",
        "不要把 DSH 专用 frontmatter",
        "math-modeling",
        "native-adapter",
        "仓库根目录",
    ):
        assert phrase in readme
    install = (ROOT / "docs" / "agent-skill-installation.md").read_text(encoding="utf-8")
    assert "DeepSeek Harness" in install
    assert "hosts/deepseek-harness" in install


def test_sync_mirrors_skills_without_rewriting_entrypoint(tmp_path: Path):
    target = tmp_path / "dsh-adapter"
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), "--repo", str(ROOT), "--target", str(target)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    source = ROOT / "skills" / "math-modeling" / "SKILL.md"
    mirrored = target / "skills" / "math-modeling" / "SKILL.md"
    assert mirrored.is_file()
    assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(mirrored.read_bytes()).digest()
    assert (target / "source-manifest.yaml").is_file()
    assert (target / "schemas").is_dir()
    text = result.stdout
    assert "math-modeling" in text or "ENTRY" in text
