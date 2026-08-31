"""Deterministic contract checks for the problem familiarization skill."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-problem-familiarization"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-problem-familiarization"


def test_entrypoint_requires_rounds_and_understanding_gate():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-problem-familiarization" in content
    assert "TODO" not in content
    for phrase in (
        "分轮",
        "题目背景",
        "对象与关系",
        "literature_insight_id",
        "team_restatement_or_questions",
        "understanding_checkpoint.md",
        "human-confirmed",
        "模型候选比较",
        "方法先例",
        "文献迁移边界",
    ):
        assert phrase in content


def test_reference_and_template_contracts_exist():
    contract = (SKILL_DIR / "references" / "familiarization-contract.md").read_text(
        encoding="utf-8"
    )
    research = (SKILL_DIR / "references" / "research-basis.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "object_relation",
        "measurement_data",
        "source_does_not_support",
        "non_transferable_boundary",
        "team_restatement_or_questions",
        "decision_id",
    ):
        assert phrase in contract
    assert "历史会话" in research
    for name in (
        "problem_background_map.md",
        "literature_orientation_ledger.md",
        "understanding_checkpoint.md",
        "familiarization_open_questions.md",
    ):
        assert (ROOT / "templates" / name).is_file()


def test_fixtures_cover_understanding_and_literature_boundaries():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-multi-round.md",
        "positive-literature-mapping.md",
        "negative-model-jump.md",
        "negative-abstract-only.md",
        "negative-structural-inference.md",
        "negative-vague-confirmation.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "复述",
        "纠正",
        "checkpoint",
        "摘要",
        "blocked",
        "不可迁移",
        "不能直接进入模型",
    ):
        assert phrase in expected


if __name__ == "__main__":
    for test in (
        test_entrypoint_requires_rounds_and_understanding_gate,
        test_reference_and_template_contracts_exist,
        test_fixtures_cover_understanding_and_literature_boundaries,
    ):
        test()
    print("modeling-problem-familiarization contract: OK")
