"""Deterministic contract checks for the modeling-problem-intake skill.

These checks validate the skill package and regression fixtures, not the wording
of a future model response. Behavioral evaluation remains evidence-based manual
or agent review against expected-behavior.md.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-problem-intake"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-problem-intake"


def test_skill_entrypoint_has_discriminating_contract():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-problem-intake" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "不替人选择最终模型",
        "evidence_id",
        "human-confirmed",
        "external",
        "指令性文字",
        "modeling-problem-familiarization",
        "orientation",
    ):
        assert phrase in content
    schema = (SKILL_DIR / "references" / "intake-schema.md").read_text(encoding="utf-8")
    for phrase in (
        "source_manifest_hash",
        "objective_candidate",
        "constraint_candidate",
        "确认范围",
        "last_evidence_id",
    ):
        assert phrase in schema


def test_referenced_resources_exist():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for name in (
        "intake-schema.md",
        "figure-and-geometry.md",
        "long-prompt-checkpoint.md",
        "research-basis.md",
    ):
        assert name in content
        assert (SKILL_DIR / "references" / name).is_file()
    figure = (SKILL_DIR / "references" / "figure-and-geometry.md").read_text(encoding="utf-8")
    checkpoint = (SKILL_DIR / "references" / "long-prompt-checkpoint.md").read_text(encoding="utf-8")
    assert "端点/边界" in figure
    assert "candidate_inferences" in checkpoint
    assert "alternatives" in checkpoint


def test_regression_fixture_set_contains_positive_and_negative_cases():
    fixture_names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    assert "positive-explicit-structure.md" in fixture_names
    assert "positive-nonoptimization.md" in fixture_names
    assert "negative-ambiguous-diagram.md" in fixture_names
    assert "negative-quantifier-and-injection.md" in fixture_names
    assert "negative-ocr-and-version-conflict.md" in fixture_names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in ("unknown", "conflict", "不能自动添加优化目标", "绕过本技能"):
        assert phrase in expected


if __name__ == "__main__":
    for test in (
        test_skill_entrypoint_has_discriminating_contract,
        test_referenced_resources_exist,
        test_regression_fixture_set_contains_positive_and_negative_cases,
    ):
        test()
    print("modeling-problem-intake contract: OK")
