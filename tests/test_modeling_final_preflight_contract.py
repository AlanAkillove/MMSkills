"""Deterministic package checks for modeling-final-preflight."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-final-preflight"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-final-preflight"


def test_entrypoint_is_status_aggregator_not_compliance_guarantee():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-final-preflight" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "提交前状态汇总和阻断器",
        "不替团队决定模型",
        "pass/fail/unknown",
        "rules_profile",
        "human_signoff.md",
        "P0",
        "P1",
        "ready_for_human_submission",
        "成文清洁",
        "check_manuscript_quality.py",
    ):
        assert phrase in content


def test_references_define_check_layers_and_signoff():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "preflight-contract.md",
        "check-catalog.md",
        "blocking-and-signoff.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "preflight-contract.md").read_text(
        encoding="utf-8"
    )
    checks = (SKILL_DIR / "references" / "check-catalog.md").read_text(encoding="utf-8")
    blocking = (SKILL_DIR / "references" / "blocking-and-signoff.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "release_manifest",
        "input_hashes",
        "output_hashes",
        "overall_status",
        "ready-for-human-submission",
        "unknown",
    ):
        assert phrase in contract
    for phrase in ("身份与范围", "论文结构与格式", "内容与证据", "AI 披露"):
        assert phrase in checks
    for phrase in ("P0/P1", "accepted-risk", "frozen", "decision ID"):
        assert phrase in blocking
    assert (SKILL_DIR / "scripts" / "check_manuscript_quality.py").is_file()


def test_fixture_set_covers_blocking_unknown_and_freeze():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-ready-for-human-signoff.md",
        "positive-frozen-manifest.md",
        "negative-profile-stale.md",
        "negative-p1-claim-open.md",
        "negative-unknown-render.md",
        "negative-ai-disclosure-open.md",
        "negative-support-identity.md",
        "negative-version-conflict.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "needs-human-signoff",
        "frozen",
        "过期 profile",
        "主张 P1",
        "unknown/unassessed",
        "AI 披露",
        "支撑身份",
        "版本冲突",
        "不输出通过率",
    ):
        assert phrase in expected
    positive = (FIXTURE_DIR / "positive-frozen-manifest.md").read_text(encoding="utf-8")
    assert "P0/P1 清零" in positive and "P2/P3" in positive


if __name__ == "__main__":
    for test in (
        test_entrypoint_is_status_aggregator_not_compliance_guarantee,
        test_references_define_check_layers_and_signoff,
        test_fixture_set_covers_blocking_unknown_and_freeze,
    ):
        test()
    print("modeling-final-preflight contract: OK")
