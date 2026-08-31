"""Deterministic package checks for modeling-rules-profile."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-rules-profile"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-rules-profile"


def test_entrypoint_sets_versioned_rule_boundary():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-rules-profile" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "规则取证和版本化",
        "不提供法律意见",
        "不把一个赛事的格式或 AI 规则泛化",
        "来源 manifest",
        "P0",
        "P1",
        "human_confirmation",
        "unknown/conflict/stale",
        'schema_version: "0.2"',
    ):
        assert phrase in content


def test_references_define_source_rule_and_freshness_schema():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "profile-schema.md",
        "source-provenance.md",
        "conflict-and-freshness.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    schema = (SKILL_DIR / "references" / "profile-schema.md").read_text(
        encoding="utf-8"
    )
    provenance = (SKILL_DIR / "references" / "source-provenance.md").read_text(
        encoding="utf-8"
    )
    freshness = (SKILL_DIR / "references" / "conflict-and-freshness.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "source_id",
        "authority",
        "content_hash",
        "rule_id",
        "evidence_anchors",
        "not_stated",
        "verified",
    ):
        assert phrase in schema
    for phrase in ("原文标题", "页码", "搜索结果标题", "来源权威级别"):
        assert phrase in provenance
    for phrase in ("scope_conflict", "version_conflict", "stale", "人工升级问题"):
        assert phrase in freshness


def test_fixture_set_covers_missing_scope_and_conflict():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-cumcm-profile.md",
        "positive-local-pdf-evidence.md",
        "negative-missing-year.md",
        "negative-search-snippet.md",
        "negative-cross-competition-copy.md",
        "negative-source-conflict.md",
        "negative-stale-profile.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "官方来源",
        "文本/视觉交叉核验",
        "P0/blocked",
        "搜索摘要",
        "跨赛事复制",
        "conflict",
        "stale",
        "evidence anchor",
    ):
        assert phrase in expected
    conflict = (FIXTURE_DIR / "negative-source-conflict.md").read_text(encoding="utf-8")
    assert "两个来源" in conflict and "PDF" in conflict


if __name__ == "__main__":
    for test in (
        test_entrypoint_sets_versioned_rule_boundary,
        test_references_define_source_rule_and_freshness_schema,
        test_fixture_set_covers_missing_scope_and_conflict,
    ):
        test()
    print("modeling-rules-profile contract: OK")
