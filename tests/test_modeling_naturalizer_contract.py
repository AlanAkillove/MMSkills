"""Deterministic package checks for modeling-paper-naturalizer."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-paper-naturalizer"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-paper-naturalizer"


def test_entrypoint_declares_naturalization_boundary_and_handoff():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-paper-naturalizer" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "不以规避任何检测器为功能目标",
        "minimal-edit",
        "diagnose-only",
        "preservation_report.md",
        "P0",
        "P1",
        "human-confirmed",
        "不全局替换术语",
    ):
        assert phrase in content


def test_references_cover_revision_contract_and_protected_syntax():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    required_refs = {
        "revision-contract.md",
        "naturalization-patterns.md",
        "protected-syntax.md",
        "research-basis.md",
    }
    assert required_refs <= {
        path.name for path in (SKILL_DIR / "references").glob("*.md")
    }
    for name in required_refs:
        assert name in content
    assert "防御性声明处理协议" in content
    assert (ROOT / "references" / "defensive-statement-protocol.md").is_file()
    contract = (SKILL_DIR / "references" / "revision-contract.md").read_text(
        encoding="utf-8"
    )
    protected = (SKILL_DIR / "references" / "protected-syntax.md").read_text(
        encoding="utf-8"
    )
    patterns = (SKILL_DIR / "references" / "naturalization-patterns.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "source_manifest_hash",
        "locked:",
        "semantic_change",
        "structure_preserving",
        "长文续接",
    ):
        assert phrase in contract
    for phrase in ("\\cite", "\\ref", "token", "哈希", "人工确认"):
        assert phrase in protected
    for phrase in ("对象—动作—结果", "高承诺词", "摘要/结论模板", "防御性声明", "证据在哪里"):
        assert phrase in patterns


def test_fixture_set_covers_safe_edits_and_semantic_drift():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-conservative-method.md",
        "positive-topic-specific-results.md",
        "negative-template-introduction.md",
        "negative-meaning-drift.md",
        "negative-protected-latex.md",
        "negative-missing-evidence.md",
        "negative-terminology-drift.md",
        "negative-redundant-defensive-statements.md",
        "positive-required-limitation.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "18.4/21.0 min",
        "表 3",
        "潮汐窗口",
        "P0/P1",
        "LaTeX",
        "缺证据",
        "术语漂移",
    ):
        assert phrase in expected
    drift = (FIXTURE_DIR / "negative-meaning-drift.md").read_text(encoding="utf-8")
    assert "导致" in drift and "全局最优" in drift
    latex = (FIXTURE_DIR / "negative-protected-latex.md").read_text(encoding="utf-8")
    for token in (r"\ref{eq:flow}", r"\cite{smith2024}", r"x_i", r"x_i\ge 0"):
        assert token in latex


if __name__ == "__main__":
    for test in (
        test_entrypoint_declares_naturalization_boundary_and_handoff,
        test_references_cover_revision_contract_and_protected_syntax,
        test_fixture_set_covers_safe_edits_and_semantic_drift,
    ):
        test()
    print("modeling-paper-naturalizer contract: OK")
