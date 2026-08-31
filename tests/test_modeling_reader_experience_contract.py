"""Deterministic package checks for modeling-reader-experience-auditor."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-reader-experience-auditor"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-reader-experience-auditor"


def test_entrypoint_defines_three_reader_paths_and_scope():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-reader-experience-auditor" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "快速评阅者",
        "技术复核者",
        "非本专业读者",
        "不以增加篇幅或华丽表达为目标",
        "unassessed",
        "reader_cost",
        "acceptance_test",
        "防御性声明",
    ):
        assert phrase in content


def test_references_define_reader_tasks_and_visual_boundary():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "reader-contract.md",
        "reader-paths.md",
        "visual-and-navigation-checks.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "reader-contract.md").read_text(
        encoding="utf-8"
    )
    paths = (SKILL_DIR / "references" / "reader-paths.md").read_text(encoding="utf-8")
    visual = (SKILL_DIR / "references" / "visual-and-navigation-checks.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "source_manifest_hash",
        "reader_task",
        "reader_finding",
        "backtrack_count",
        "unassessed",
        "friction_type",
    ):
        assert phrase in contract
    for phrase in ("快速评阅者", "技术复核者", "非本专业读者", "信息负担"):
        assert phrase in paths
    for phrase in ("标题孤行", "渲染件", "图例", "公式被裁切"):
        assert phrase in visual


def test_fixture_set_covers_navigation_and_unassessed_render():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-navigable.md",
        "negative-abstract-no-answer.md",
        "negative-symbol-first-use.md",
        "negative-figure-detached.md",
        "negative-cross-section-backtrack.md",
        "negative-overexplained-background.md",
        "negative-defensive-load.md",
        "negative-unassessed-render.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "快速评阅",
        "技术复原",
        "extra_backtrack",
        "图例",
        "防御性声明",
        "unassessed",
        "reader_path",
        "不输出",
    ):
        assert phrase in expected
    positive = (FIXTURE_DIR / "positive-navigable.md").read_text(encoding="utf-8")
    assert "表 3" in positive and "图 4" in positive and "箱/小时" in positive


if __name__ == "__main__":
    for test in (
        test_entrypoint_defines_three_reader_paths_and_scope,
        test_references_define_reader_tasks_and_visual_boundary,
        test_fixture_set_covers_navigation_and_unassessed_render,
    ):
        test()
    print("modeling-reader-experience-auditor contract: OK")
