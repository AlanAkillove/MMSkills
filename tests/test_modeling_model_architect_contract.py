"""Deterministic package checks for modeling-model-architect."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-model-architect"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-model-architect"


def test_entrypoint_is_baseline_first_and_human_led():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-model-architect" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "可解释基线",
        "不替人选择最终模型",
        "不把算法名称当创新",
        "baseline",
        "candidate",
        "adopted",
        "human_status",
        "用户层",
        "不使用总分",
        "未回复",
        "理解校验",
        "understanding_check",
        "model_candidate_cards.md",
        "model_decision_brief.md",
        "problem_familiarization",
        "literature_orientation_ledger",
        "P0",
        "P1",
    ):
        assert phrase in content


def test_references_define_registry_fit_and_validation():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "model-contract.md",
        "baseline-and-fit.md",
        "user-decision-support.md",
        "validation-readiness.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "model-contract.md").read_text(
        encoding="utf-8"
    )
    fit = (SKILL_DIR / "references" / "baseline-and-fit.md").read_text(encoding="utf-8")
    validation = (SKILL_DIR / "references" / "validation-readiness.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "model_id",
        "objective",
        "constraints",
        "fit_to_problem",
        "validation_plan_ids",
        "decision_id",
    ):
        assert phrase in contract
    for phrase in ("基线最低要求", "适配矩阵", "复杂度", "失败边界"):
        assert phrase in fit
    for phrase in ("进入实验前", "预测", "优化/决策", "极端情形", "判据"):
        assert phrase in validation
    support = (SKILL_DIR / "references" / "user-decision-support.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "一句话层",
        "比较层",
        "不使用",
            "潜在收益",
            "未回复",
            "用自己的话",
            "理解校验",
            "understanding_check",
            "comprehension_status",
        "adopt | reject | continue-validation",
    ):
        assert phrase in support
    for name in ("model_candidate_cards.md", "model_decision_brief.md"):
        assert (ROOT / "templates" / name).exists()


def test_fixture_set_covers_model_choice_failure_modes():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-baseline-and-candidate.md",
        "positive-common-model-fit.md",
        "negative-model-name-only.md",
        "negative-no-task-boundary.md",
        "negative-overcomplex.md",
        "negative-hidden-assumptions.md",
        "negative-no-baseline.md",
        "negative-code-paper-conflict.md",
        "positive-user-friendly-evaluation.md",
        "negative-black-box-score.md",
        "negative-jargon-only.md",
        "negative-passive-consent.md",
        "negative-overconfident-evaluation.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "baseline/candidate",
        "常见模型",
        "不直接选择 LSTM",
        "停止强行加模块",
        "i.i.d./正态/因果",
        "可解释基线",
        "conflict",
        "候选未确认",
        "分项评估",
        "总分",
        "用户沉默",
        "不熟悉",
        "理解",
        "用户用自己的话",
    ):
        assert phrase in expected
    conflict = (FIXTURE_DIR / "negative-code-paper-conflict.md").read_text(encoding="utf-8")
    assert "c\\le 6" in conflict and "c\\le 10" in conflict


if __name__ == "__main__":
    for test in (
        test_entrypoint_is_baseline_first_and_human_led,
        test_references_define_registry_fit_and_validation,
        test_fixture_set_covers_model_choice_failure_modes,
    ):
        test()
    print("modeling-model-architect contract: OK")
