"""Deterministic package checks for modeling-figure-table-auditor."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-figure-table-auditor"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-figure-table-auditor"


def test_entrypoint_requires_evidence_and_visual_boundaries():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-figure-table-auditor" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "证据角色",
        "数据/单位/图例/标签",
        "不把装饰图当证据",
        "unassessed",
        "输出 hash",
        "claim_ids",
        "P0",
        "P1",
    ):
        assert phrase in content


def test_references_define_traceability_and_visual_checks():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "figure-contract.md",
        "data-and-claim-checks.md",
        "visual-checks.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "figure-contract.md").read_text(
        encoding="utf-8"
    )
    checks = (SKILL_DIR / "references" / "data-and-claim-checks.md").read_text(
        encoding="utf-8"
    )
    visual = (SKILL_DIR / "references" / "visual-checks.md").read_text(encoding="utf-8")
    for phrase in (
        "figure_id",
        "question_ids",
        "claim_ids",
        "source_data_ids",
        "output_hash",
        "unassigned",
    ):
        assert phrase in contract
    for phrase in ("溯源链", "数值与单位", "主张边界", "全局最优"):
        assert phrase in checks
    for phrase in ("有渲染件才判断页面", "unassessed", "图表裁切", "可读性与证据分流"):
        assert phrase in visual


def test_fixture_set_covers_mismatch_and_missing_render():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-traceable-figure.md",
        "positive-boundary-plot.md",
        "negative-decorative-figure.md",
        "negative-number-unit-mismatch.md",
        "negative-hidden-unfavorable.md",
        "negative-unsupported-claim.md",
        "negative-missing-source-code.md",
        "negative-unassessed-render.md",
        "negative-identity-leak.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "figure/claim/evidence/experiment/data ID",
        "全局最优证明",
        "unassigned/decorative",
        "数字单位冲突",
        "隐藏结果/截轴",
        "只有 PNG",
        "unassessed",
        "身份泄露",
    ):
        assert phrase in expected
    positive = (FIXTURE_DIR / "positive-traceable-figure.md").read_text(encoding="utf-8")
    assert "FIG-04" in positive and "EXP-03" in positive and "艘" in positive


if __name__ == "__main__":
    for test in (
        test_entrypoint_requires_evidence_and_visual_boundaries,
        test_references_define_traceability_and_visual_checks,
        test_fixture_set_covers_mismatch_and_missing_render,
    ):
        test()
    print("modeling-figure-table-auditor contract: OK")
