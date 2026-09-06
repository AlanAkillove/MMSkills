"""Deterministic package checks for modeling-paper-reviewer."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-paper-reviewer"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-paper-reviewer"


def test_entrypoint_preserves_reviewer_role_boundary():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-paper-reviewer" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "投稿前自审/竞赛论文预评阅",
        "不输出 AI 率",
        "不直接修改论文",
        "alternative_explanation",
        "acceptance_test",
        "human_decision_queue.md",
        "竞赛保密窗口",
        "独立 Subagent",
    ):
        assert phrase in content


def test_references_define_lenses_and_finding_contract():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "review-contract.md",
        "review-lenses.md",
        "review-workflow.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "review-contract.md").read_text(
        encoding="utf-8"
    )
    lenses = (SKILL_DIR / "references" / "review-lenses.md").read_text(
        encoding="utf-8"
    )
    workflow = (SKILL_DIR / "references" / "review-workflow.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "source_manifest_hash",
        "evidence_anchors",
        "confidence",
        "acceptance_test",
        "P0",
        "P1",
        "accepted-risk",
    ):
        assert phrase in contract
    for phrase in (
        "题意与任务忠实度",
        "模型、数学与算法适配性",
        "数据、实验与可复现性",
        "主张、证据与结论边界",
        "阅读体验与表达",
        "竞赛规则、身份与材料边界",
    ):
        assert phrase in lenses
    for phrase in ("故事线", "独立审查", "冻结", "去重", "验收标准"):
        assert phrase in workflow


def test_fixture_set_covers_false_positive_and_blocking_cases():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-clear-scope.md",
        "negative-question-mismatch.md",
        "negative-assumption-silent.md",
        "negative-model-evidence.md",
        "negative-causal-overclaim.md",
        "negative-results-repro.md",
        "negative-reader-path.md",
        "negative-unauthorized-similarity.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "不因模型常见",
        "题面条件/子任务",
        "全局最优",
        "缺测试集/版本/种子/代码入口",
        "未授权相似性",
        "evidence_anchors",
        "unknown",
    ):
        assert phrase in expected
    causal = (FIXTURE_DIR / "negative-causal-overclaim.md").read_text(encoding="utf-8")
    assert "导致" in causal and "全局最优" in causal


if __name__ == "__main__":
    for test in (
        test_entrypoint_preserves_reviewer_role_boundary,
        test_references_define_lenses_and_finding_contract,
        test_fixture_set_covers_false_positive_and_blocking_cases,
    ):
        test()
    print("modeling-paper-reviewer contract: OK")
