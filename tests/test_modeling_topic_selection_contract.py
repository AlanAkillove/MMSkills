"""Deterministic contract checks for the multi-topic selection skill."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-topic-selection"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-topic-selection"


def test_entrypoint_is_full_inventory_and_human_led():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-topic-selection" in content
    assert "TODO" not in content
    for phrase in (
        "全部候选题",
        "分项比较",
        "不生成黑箱总分",
        "不替团队自动决定题目",
        "statement_snapshot_id",
        "human-confirmed",
        "decision_id",
        "最早验证任务",
        "模型流行",
        "获奖预测",
    ):
        assert phrase in content


def test_reference_and_template_contracts_exist():
    reference = (SKILL_DIR / "references" / "selection-contract.md").read_text(
        encoding="utf-8"
    )
    research = (SKILL_DIR / "references" / "research-basis.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "problem_comprehension",
        "background_load",
        "validation_feasibility",
        "topic_specificity",
        "reasoning",
        "reversal_conditions",
    ):
        assert phrase in reference
    assert "历史项目" in research
    for name in ("topic_cards.md", "topic_selection_brief.md"):
        assert (ROOT / "templates" / name).is_file()


def test_fixtures_cover_selection_failure_modes():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-complete-comparison.md",
        "positive-user-friendly-evaluation.md",
        "negative-incomplete-inventory.md",
        "negative-total-score.md",
        "negative-default-recommendation.md",
        "negative-unconfirmed-selection.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "全量",
        "unknown",
        "分项",
        "总分",
        "默认推荐",
        "人工选题门",
        "备选",
    ):
        assert phrase in expected


if __name__ == "__main__":
    for test in (
        test_entrypoint_is_full_inventory_and_human_led,
        test_reference_and_template_contracts_exist,
        test_fixtures_cover_selection_failure_modes,
    ):
        test()
    print("modeling-topic-selection contract: OK")
