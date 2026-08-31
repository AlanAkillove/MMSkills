"""Deterministic package checks for modeling-paper-architect."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-paper-architect"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-paper-architect"


def test_entrypoint_is_contract_before_prose():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-paper-architect" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "差异化账本、模型注册、实验和主张证据",
        "不先套模板",
        "section_contract",
        "paper_blueprint.md",
        "argument_map.md",
        "人工确认门",
        "P0",
        "P1",
    ):
        assert phrase in content


def test_references_define_blueprint_and_argument_mapping():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "blueprint-contract.md",
        "argument-mapping.md",
        "section-and-paragraph-functions.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "blueprint-contract.md").read_text(
        encoding="utf-8"
    )
    mapping = (SKILL_DIR / "references" / "argument-mapping.md").read_text(
        encoding="utf-8"
    )
    functions = (SKILL_DIR / "references" / "section-and-paragraph-functions.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "question_ids",
        "claim_ids",
        "evidence_ids",
        "paragraph_functions",
        "must_not_invent",
        "human_status",
    ):
        assert phrase in contract
    for phrase in ("主线图", "篇幅预算", "摘要与结论回归", "结构反模板检查"):
        assert phrase in mapping
    for phrase in ("题目/问题分析", "模型建立", "结果/验证", "段落最小单元"):
        assert phrase in functions


def test_fixture_set_covers_structure_and_unconfirmed_content():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-evidence-led-blueprint.md",
        "positive-standard-sections.md",
        "negative-template-outline.md",
        "negative-abstract-before-evidence.md",
        "negative-missing-subproblem.md",
        "negative-paragraph-list.md",
        "negative-figure-decoration.md",
        "negative-unconfirmed-content.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "题目子问题",
        "不因目录常见",
        "固定填充",
        "普适最优",
        "子问题断链",
        "段落功能",
        "claim ID",
        "candidate/planned",
    ):
        assert phrase in expected
    positive = (FIXTURE_DIR / "positive-evidence-led-blueprint.md").read_text(
        encoding="utf-8"
    )
    assert "EXP-03" in positive and "图 4" in positive and "claim ID" in positive


if __name__ == "__main__":
    for test in (
        test_entrypoint_is_contract_before_prose,
        test_references_define_blueprint_and_argument_mapping,
        test_fixture_set_covers_structure_and_unconfirmed_content,
    ):
        test()
    print("modeling-paper-architect contract: OK")
