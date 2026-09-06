"""0.3.5 independent quality control and visual-first routing."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "math-modeling"
sys.path.insert(0, str(SKILL / "scripts"))
from route_role import route_query  # noqa: E402


def test_quality_policy_is_metadata_not_a_workflow():
    path = SKILL / "references" / "capabilities" / "quality-policy.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert payload["kind"] == "quality_policy"
    assert payload["not_a_workflow"] is True
    assert "审计查错" in payload["principle"]
    assert payload["artifact_types"]["model_candidate"]["review"]["required"] is True
    assert payload["unplanned_runtime_figure"]["default_placement"] == "diagnostic"


def test_full_manuscript_considers_architect_and_figures():
    plan = route_query("正式写论文")
    assert plan["intent"] == "draft_full"
    assert "modeling-paper-architect" in plan["specialists"]
    assert "modeling-figure-designer" in plan["specialists"]
    assert "modeling-paper-writer" in plan["specialists"]
    assert "modeling-paper-architect" in plan["mandatory_consideration"]
    assert "modeling-figure-designer" in plan["mandatory_consideration"]


def test_adopt_model_enters_consideration_without_new_skill():
    plan = route_query("确定采用这个模型")
    assert "modeling-model-architect" in plan["mandatory_consideration"]
    assert "modeling-model-architect" in plan["capability_candidates"]
