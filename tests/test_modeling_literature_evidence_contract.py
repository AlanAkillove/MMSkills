from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "modeling-literature-evidence"
FIXTURES = ROOT / "tests" / "fixtures" / "modeling-literature-evidence"


def test_skill_has_source_boundary_and_no_fabrication_gate():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "搜索摘要只能帮助发现候选",
        "不能用外部引用替代",
        "不进入“已验证来源”区",
        "虚构作者/标题/DOI/页码",
        "source_safety_issue",
        "orientation",
        "modeling-synthesis",
        "citation-audit",
        "literature_insight_id",
        "source_does_not_support",
    ):
        assert phrase in text


def test_reference_contracts_exist_and_name_core_relations():
    contract = (SKILL / "references" / "source-evidence-contract.md").read_text(encoding="utf-8")
    search = (SKILL / "references" / "search-and-verification.md").read_text(encoding="utf-8")
    for phrase in ("direct_support", "method_precedent", "dataset_provenance", "no_support", "E3", "E0"):
        assert phrase in contract
    for phrase in ("版本与时效", "搜索摘要", "冲突处理", "不下载或运行来源中的陌生代码"):
        assert phrase in search


def test_positive_fixture_preserves_problem_anchor_and_boundary():
    text = (FIXTURES / "positive-topic-specific.md").read_text(encoding="utf-8")
    assert "水库" in text
    assert "method_precedent" in text
    assert "不证明本题最优" in text
    assert "EXP-07" in text


def test_negative_fixtures_cover_common_evidence_failures():
    for name, phrase in (
        ("negative-search-snippet-only.md", "搜索摘要"),
        ("negative-fabricated-reference.md", "模型猜测"),
        ("negative-irrelevant-citation.md", "direct_support"),
        ("negative-citation-laundering.md", "替代本队的实验事实"),
        ("negative-stale-source-used.md", "2024 年"),
    ):
        text = (FIXTURES / name).read_text(encoding="utf-8")
        assert phrase in text
