"""Deterministic contract checks for modeling-tex-paper-production."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-tex-paper-production"
TEMPLATE_DIR = ROOT / "templates" / "tex"


def test_entrypoint_defines_tex_scope_and_human_boundary():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-tex-paper-production" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "赛事 profile",
        "相对路径",
        "真实 PDF",
        "阅读效果",
        "人类确认门",
        "P0/P1",
        "needs-human-confirmation",
        "modeling-final-preflight",
        "modeling-process-freezer",
    ):
        assert phrase in content


def test_template_contains_profile_switches_and_no_project_content():
    tex = (TEMPLATE_DIR / "main.tex").read_text(encoding="utf-8")
    for name in (
        "mmIncludeContents",
        "mmIncludeAIStatement",
        "mmIncludeCodeAppendix",
        "mmShowHeader",
        "mmIncludeBibliography",
    ):
        assert f"\\{name}" in tex
    for phrase in (
        "\\begin{abstract}",
        "\\appendix",
        "\\bibliographystyle",
        "\\bibliography{references}",
        "\\graphicspath",
        "\\label{",
    ):
        assert phrase in tex
    assert "\\mmIncludeBibliographyfalse" in tex
    assert "\\ifmmIncludeBibliography" in tex
    assert "\\nocite{*}" not in tex
    for marker in ("D:/DesktopDocs/", "C:/Users/"):
        assert marker not in tex
    assert "..\\..\\" not in tex


def test_template_support_files_are_neutral_and_present():
    assert (TEMPLATE_DIR / "references.bib").exists()
    assert (TEMPLATE_DIR / "latexmkrc").exists()
    assert (TEMPLATE_DIR / "tex-format-profile.example.yaml").exists()
    assert (TEMPLATE_DIR / "tex_build_manifest.example.yaml").exists()
    assert (TEMPLATE_DIR / "tex_layout_audit.example.md").exists()
    bib = (TEMPLATE_DIR / "references.bib").read_text(encoding="utf-8")
    assert "@comment{" in bib
    assert "@article{" not in bib
    profile = (TEMPLATE_DIR / "tex-format-profile.example.yaml").read_text(
        encoding="utf-8"
    )
    for field in (
        "engine:",
        "table_of_contents:",
        "page_count_definition:",
        "ai_disclosure:",
        "human_confirmation:",
    ):
        assert field in profile
    manifest = (TEMPLATE_DIR / "tex_build_manifest.example.yaml").read_text(
        encoding="utf-8"
    )
    for field in (
        "entrypoint:",
        "primary_command:",
        "inputs:",
        "outputs:",
        "human_confirmation:",
    ):
        assert field in manifest
    audit = (TEMPLATE_DIR / "tex_layout_audit.example.md").read_text(
        encoding="utf-8"
    )
    for phrase in ("页面抽查", "finding_id", "未评估与待确认", "needs-human-confirmation"):
        assert phrase in audit


def test_deterministic_template_checker_passes():
    checker = SKILL_DIR / "scripts" / "check_tex_template.py"
    result = subprocess.run(
        [sys.executable, str(checker), str(TEMPLATE_DIR / "main.tex")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "matches the generic TeX template contract" in result.stdout


if __name__ == "__main__":
    test_entrypoint_defines_tex_scope_and_human_boundary()
    test_template_contains_profile_switches_and_no_project_content()
    test_template_support_files_are_neutral_and_present()
    test_deterministic_template_checker_passes()
    print("modeling-tex-paper-production contract: OK")
