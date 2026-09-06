"""Deterministic package checks for modeling-figure-designer."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-figure-designer"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-figure-designer"


def test_entrypoint_defines_design_scope_and_human_boundary():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-figure-designer" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "读者任务",
        "证据角色",
        "美观",
        "没有源数据时只能做版式/可读性",
        "不替代图表事实审计",
        "五秒",
        "unassessed",
        "modeling-figure-table-auditor",
        "P0/P1",
        "diagnostic",
        "placement",
        "visual-first",
        "visual brief",
    ):
        assert phrase in content


def test_references_and_templates_define_production_contract():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    required_refs = {
        "design-contract.md",
        "chart-selection.md",
        "visual-system.md",
        "production-and-handoff.md",
        "research-basis.md",
    }
    assert required_refs <= {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    for name in required_refs:
        assert name in content
    contract = (SKILL_DIR / "references" / "design-contract.md").read_text(encoding="utf-8")
    chart = (SKILL_DIR / "references" / "chart-selection.md").read_text(encoding="utf-8")
    visual = (SKILL_DIR / "references" / "visual-system.md").read_text(encoding="utf-8")
    handoff = (SKILL_DIR / "references" / "production-and-handoff.md").read_text(encoding="utf-8")
    for phrase in (
        "figure_id",
        "figure_question",
        "claim_ids",
        "source_data_ids",
        "input_manifest_hash",
        "output_hashes",
        "needs-confirmation",
    ):
        assert phrase in contract
    for phrase in ("变量关系", "约束与可行域", "敏感性与稳健性", "彩虹色带"):
        assert phrase in chart
    for phrase in ("目标页面", "颜色", "灰度", "多面板", "题目特异性"):
        assert phrase in visual
    for phrase in ("input_manifest_hash", "输出 hash", "page_render_status", "下游路由"):
        assert phrase in handoff
    for name in ("figure_design_brief.md", "figure_storyboard.md", "figure_design_manifest.yaml"):
        assert (ROOT / "templates" / name).exists()


def test_fixture_set_covers_evidence_design_and_visual_failure_modes():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-evidence-led-plot.md",
        "positive-model-flow.md",
        "negative-decorative-dashboard.md",
        "negative-wrong-chart-type.md",
        "negative-rainbow-and-color-only.md",
        "negative-copy-template.md",
        "negative-multi-panel-duplication.md",
        "negative-unverified-annotation.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "读者任务",
        "证据角色",
        "错误图型",
        "彩虹色带",
        "只靠颜色",
        "题目特异性",
        "多面板重复",
        "未经核实的标注",
        "交给图表审计",
    ):
        assert phrase in expected
    positive = (FIXTURE_DIR / "positive-evidence-led-plot.md").read_text(encoding="utf-8")
    assert "FIG-07" in positive and "claim_ids" in positive and "SVG" in positive


if __name__ == "__main__":
    for test in (
        test_entrypoint_defines_design_scope_and_human_boundary,
        test_references_and_templates_define_production_contract,
        test_fixture_set_covers_evidence_design_and_visual_failure_modes,
    ):
        test()
    print("modeling-figure-designer contract: OK")
