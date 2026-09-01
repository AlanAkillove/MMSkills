"""CUMCM 2026 AI policy must not silently carry 2025 bibliography/body-mark rules."""

from __future__ import annotations

import yaml
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "references" / "rules" / "cumcm-2026.yaml"
SNAPSHOT = ROOT / "references" / "rules" / "cumcm-2026.md"


def test_cumcm_2026_profile_drops_2025_bibliography_and_body_marks():
    payload = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    disclosure = payload["disclosure"]
    assert disclosure["declaration"]["location"] == "before_references"
    assert "详细使用情况见支撑材料" in disclosure["declaration"]["used"]
    assert disclosure["declaration"]["unused"] == "本参赛队在竞赛过程中未使用任何AI工具。"
    assert disclosure["citation_of_ai_in_references"] is False
    assert disclosure["in_text_annotation_of_ai_content"] is False
    assert disclosure["unused_declaration_after_references"] is False
    assert disclosure["full_raw_log_required"] is False
    assert disclosure["typical_interaction_examples_allowed"] is True
    superseded = disclosure["superseded_prior_year_requirements"]
    assert superseded["year"] == 2025
    joined = " ".join(superseded["items"])
    assert "参考文献" in joined and "正文" in joined
    assert payload["ai_policy"]["core_modeling_and_analysis"] == "must_be_team_led"
    rule_ids = {rule["rule_id"] for rule in payload["rules"]}
    assert "CUMCM-AI-NO-2025-BIBLIOGRAPHY-OR-BODY-MARK" in rule_ids
    source_ids = {source["source_id"] for source in payload["sources"]}
    assert {"CUMCM-AI-2026-CN", "CUMCM-AI-2026-LOCAL", "CUMCM-AI-2025-CN"} <= source_ids


def test_cumcm_2026_snapshot_tells_agents_not_to_cite_ai_tools():
    text = SNAPSHOT.read_text(encoding="utf-8")
    for phrase in (
            "把 AI 工具写入参考文献",
            "正文相应位置标注",
        "参考文献之前",
        "主导",
        "第 6 条",
        "不得再执行的 2025 条款",
        "不得因为“往年如此”",
    ):
        assert phrase in text, phrase
