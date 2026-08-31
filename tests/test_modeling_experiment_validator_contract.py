"""Deterministic package checks for modeling-experiment-validator."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-experiment-validator"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-experiment-validator"


def test_entrypoint_requires_registered_and_reproducible_experiments():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-experiment-validator" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "可复核实验",
        "不替作者挑最好结果",
        "baseline_comparison",
        "sensitivity",
        "uncertainty_or_repetition",
        "output_hashes",
        "validation_status",
        "unverified/unknown",
    ):
        assert phrase in content


def test_references_define_experiment_and_uncertainty_contract():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "experiment-contract.md",
        "validation-matrix.md",
        "uncertainty-and-sensitivity.md",
        "reproducibility.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "experiment-contract.md").read_text(
        encoding="utf-8"
    )
    matrix = (SKILL_DIR / "references" / "validation-matrix.md").read_text(
        encoding="utf-8"
    )
    uncertainty = (SKILL_DIR / "references" / "uncertainty-and-sensitivity.md").read_text(
        encoding="utf-8"
    )
    repro = (SKILL_DIR / "references" / "reproducibility.md").read_text(encoding="utf-8")
    for phrase in (
        "experiment_id",
        "experiment_family",
        "random_seed",
        "output_hashes",
        "result_status",
        "validation_status",
    ):
        assert phrase in contract
    for phrase in ("主张—风险—实验矩阵", "公平比较", "预先定义判据", "证据类型"):
        assert phrase in matrix
    for phrase in ("测量误差", "参数不确定性", "敏感性实验", "稳健性用语", "失败"):
        assert phrase in uncertainty
    for phrase in ("复现 manifest", "代码入口", "output_hashes", "not_run/unknown"):
        assert phrase in repro


def test_fixture_set_covers_cherry_picking_and_reproduction():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-registered-comparison.md",
        "positive-constraint-check.md",
        "negative-best-run-only.md",
        "negative-posthoc-split.md",
        "negative-missing-seed-and-output.md",
        "negative-robustness-claim.md",
        "negative-no-baseline.md",
        "negative-failed-run-deleted.md",
        "negative-paper-output-conflict.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "全量预先定义",
        "最终留出",
        "partial/unverified",
        "扰动集合",
        "不公平基线",
        "恢复失败",
        "conflict",
        "not_run/unknown",
    ):
        assert phrase in expected
    positive = (FIXTURE_DIR / "positive-constraint-check.md").read_text(encoding="utf-8")
    assert "容量不超过 6 艘" in positive and "全局最优" in positive


if __name__ == "__main__":
    for test in (
        test_entrypoint_requires_registered_and_reproducible_experiments,
        test_references_define_experiment_and_uncertainty_contract,
        test_fixture_set_covers_cherry_picking_and_reproduction,
    ):
        test()
    print("modeling-experiment-validator contract: OK")
