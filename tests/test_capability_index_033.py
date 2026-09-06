"""0.3.3 capability index: recall first, then min-cover, without loading full skills."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "math-modeling"
sys.path.insert(0, str(SKILL / "scripts"))
from route_capabilities import retrieve_capabilities, working_set_status  # noqa: E402
from route_role import route_query  # noqa: E402


CAP_DIR = SKILL / "references" / "capabilities"


def test_capability_index_is_part_of_router_contract():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    progressive = (SKILL / "references" / "progressive-disclosure.md").read_text(
        encoding="utf-8"
    )
    writer = (SKILL / "references" / "roles" / "writer.md").read_text(encoding="utf-8")
    assert "route_capabilities.py" in text
    assert "L1.5" in progressive
    assert "问题维度" in writer
    for name in ("writer.yaml", "modeler.yaml", "computationalist.yaml", "critical.yaml", "quality-policy.yaml"):
        assert (CAP_DIR / name).is_file()


def test_cards_stay_compact():
    writer = (CAP_DIR / "writer.yaml").read_text(encoding="utf-8")
    assert len(writer) < 8000
    assert "modeling-paper-reviewer" in writer
    assert "mandatory_when" in writer or "mandatory_consideration" in (
        CAP_DIR / "critical.yaml"
    ).read_text(encoding="utf-8")


def test_rewrite_abstract_does_not_fan_out():
    plan = route_query("重写摘要")
    assert plan["specialists"] == ["modeling-paper-writer"]
    assert "modeling-paper-reviewer" not in plan["specialists"]


def test_microchannel_structure_is_not_writer_structure():
    plan = route_query("先帮我弄懂这个微通道结构。")
    assert plan["intent"] == "understand"
    assert plan["role"] == "modeler"
    assert plan["specialists"] == ["modeling-problem-familiarization"]
    assert "structure" not in plan["task_facets"]
    assert "modeling-paper-architect" not in plan["specialists"]


def test_unnamed_composite_review_fans_out_via_facets():
    plan = route_query("把全文审一遍，尤其看术语、写作、结构和格式")
    assert plan["role"] == "writer"
    assert plan["review_isolation"] == "required_subagent"
    for name in (
        "modeling-paper-reviewer",
        "modeling-terminology-auditor",
        "modeling-rules-profile",
    ):
        assert name in plan["specialists"]
    assert "modeling-paper-writer" not in plan["specialists"]
    assert "modeling-paper-naturalizer" not in plan["specialists"]
    assert len(plan["specialists"]) > 2
    assert set(plan["task_facets"]) >= {"review", "terminology", "format"}


def test_dsh_dimensions_still_cover_writer_review_set():
    plan = route_query(
        "从写作质量、论文结构、语言表达、术语规范、格式规范等多个方面进行审阅。"
    )
    for name in (
        "modeling-paper-reviewer",
        "modeling-reader-experience-auditor",
        "modeling-terminology-auditor",
        "modeling-ai-pattern-reviewer",
        "modeling-rules-profile",
        "modeling-final-preflight",
    ):
        assert name in plan["specialists"]
    assert "modeling-rules-profile" in plan["mandatory_consideration"]
    assert "modeling-final-preflight" in plan["mandatory_consideration"]


def test_final_review_keeps_precision():
    plan = route_query("审阅论文")
    assert plan["specialists"] == ["modeling-paper-reviewer"]
    assert "modeling-paper-reviewer" in plan["mandatory_consideration"]
    assert "modeling-paper-reviewer" in plan["capability_candidates"]


def test_final_submission_draft_enters_candidate_set_without_forcing_load():
    retrieval = retrieve_capabilities("这是最终提交稿，帮我看看。")
    assert "modeling-rules-profile" in retrieval["mandatory_consideration"]
    assert "modeling-final-preflight" in retrieval["mandatory_consideration"]
    assert "modeling-rules-profile" in retrieval["candidates"]
    assert "modeling-final-preflight" in retrieval["candidates"]
    plan = route_query("这是最终提交稿，帮我看看。")
    assert "modeling-rules-profile" in plan["capability_candidates"]
    assert "modeling-final-preflight" in plan["capability_candidates"]
    assert "modeling-rules-profile" not in plan["specialists"]
    assert "modeling-final-preflight" not in plan["specialists"]


def test_modeler_composite_is_not_precision_locked():
    plan = route_query("结合这些论文推模型，同时把新的物理量和术语统一一下。")
    assert plan["role"] == "modeler"
    assert "modeling-model-architect" in plan["specialists"]
    assert "modeling-literature-evidence" in plan["specialists"]
    assert "modeling-terminology-auditor" in plan["specialists"]
    retrieval = retrieve_capabilities(
        "结合这些论文推模型，同时把新的物理量和术语统一一下。",
        role="modeler",
        intent="model_from_literature",
    )
    assert retrieval["precision_locked"] is False
    assert len(retrieval["task_facets"]) >= 2


def test_computationalist_composite_covers_experiment_and_figure():
    plan = route_query("跑一下参数敏感性，同时把结果图画出来并检查图中单位。")
    assert plan["role"] == "computationalist"
    assert "modeling-experiment-validator" in plan["specialists"]
    assert "modeling-figure-designer" in plan["specialists"]
    assert "modeling-figure-table-auditor" in plan["specialists"]


def test_working_set_hit_does_not_reload_catalog():
    working_set = {
        "active_working_set": {
            "role": "writer",
            "recent_capabilities": ["draft"],
            "recently_loaded": ["modeling-paper-writer"],
        }
    }
    cache = working_set_status(
        "继续问题三",
        role="writer",
        facets=[],
        working_set=working_set,
    )
    assert cache["hit"] is True
    miss = working_set_status(
        "重新研究一下问题三的物理模型",
        role="writer",
        facets=["model"],
        working_set=working_set,
    )
    assert miss["hit"] is False
    assert miss["reason"] == "invalidated"


def test_physical_model_shifts_off_writer_working_set():
    retrieval = retrieve_capabilities(
        "重新研究一下问题三的物理模型",
        role="writer",
        intent="continue_local",
        working_set={
            "active_working_set": {
                "role": "writer",
                "recent_capabilities": ["draft"],
            }
        },
    )
    assert retrieval["working_set"]["hit"] is False
    plan = route_query("重新研究一下问题三的物理模型")
    assert plan["role"] == "modeler"
    assert "modeling-model-architect" in plan["specialists"]
    assert "modeling-paper-writer" not in plan["specialists"]
