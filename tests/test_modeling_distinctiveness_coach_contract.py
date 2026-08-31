"""Deterministic package checks for modeling-distinctiveness-coach."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-distinctiveness-coach"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-distinctiveness-coach"


def test_entrypoint_sets_human_led_distinctiveness_boundary():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-distinctiveness-coach" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "合理但千篇一律",
        "不替作者决定核心模型",
        "不输出原创度/相似度/AI 率",
        "anchor",
        "forced_novelty_risk",
        "人工确认",
    ):
        assert phrase in content


def test_references_define_anchor_path_and_forced_novelty_guards():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "distinctiveness-contract.md",
        "anchor-and-path.md",
        "forced-novelty-guards.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "distinctiveness-contract.md").read_text(
        encoding="utf-8"
    )
    path = (SKILL_DIR / "references" / "anchor-and-path.md").read_text(
        encoding="utf-8"
    )
    guards = (SKILL_DIR / "references" / "forced-novelty-guards.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "evidence_ids",
        "team_decision",
        "modeling_mapping",
        "validation_mapping",
        "human_confirmation_required",
    ):
        assert phrase in contract
    for phrase in ("题目锚点", "路径比较表", "四联链", "题目特异性覆盖检查"):
        assert phrase in path
    for phrase in ("强行创新护栏", "基线", "高承诺名字", "复杂模块"):
        assert phrase in guards


def test_fixture_set_covers_real_difference_and_forced_novelty():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-anchor-driven.md",
        "positive-common-model-valid.md",
        "negative-model-name-novelty.md",
        "negative-complexity-without-data.md",
        "negative-deleted-failure.md",
        "negative-generic-template.md",
        "negative-unsupported-innovation.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "锚点—决策—验证—发现",
        "不称原创算法",
        "数据和验证能力不足",
        "失败",
        "题面脱节",
        "普适创新",
        "不输出原创度",
    ):
        assert phrase in expected
    positive = (FIXTURE_DIR / "positive-common-model-valid.md").read_text(
        encoding="utf-8"
    )
    assert "标准线性规划" in positive and "适配理由" in positive


if __name__ == "__main__":
    for test in (
        test_entrypoint_sets_human_led_distinctiveness_boundary,
        test_references_define_anchor_path_and_forced_novelty_guards,
        test_fixture_set_covers_real_difference_and_forced_novelty,
    ):
        test()
    print("modeling-distinctiveness-coach contract: OK")
