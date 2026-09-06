"""0.3.6 quality boundary resolver, shared retrieval, and compliance gate edges."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "math-modeling"
GATE = ROOT / "skills" / "modeling-final-preflight" / "scripts"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(GATE))
from check_compliance_gate import assess_compliance  # noqa: E402
from resolve_quality import resolve_quality_requirements  # noqa: E402
from route_role import route_query  # noqa: E402


def test_resolver_blocks_adopt_without_independent_review():
    blocked = resolve_quality_requirements(
        "model_candidate",
        "candidate",
        "adopted",
        artifact_hash="abc",
    )
    assert blocked["allowed"] is False
    assert blocked["allow_discussion"] is True
    assert "missing_review" in blocked["gaps"]
    assert blocked["requirements"]["review"]["required"] is True

    passing = resolve_quality_requirements(
        "model_candidate",
        "candidate",
        "adopted",
        artifact_hash="abc",
        quality_evidence={
            "audit": {"status": "pass", "artifact_hash": "abc", "source": "probe"},
            "review": {
                "status": "pass",
                "isolation": "fresh_subagent",
                "artifact_hash": "abc",
                "findings_open": [],
            },
            "human_decision": {"status": "confirmed", "decision_id": "DEC-1"},
        },
    )
    assert passing["allowed"] is True
    stale = resolve_quality_requirements(
        "model_candidate",
        "candidate",
        "adopted",
        artifact_hash="abc",
        quality_evidence={
            "audit": {"status": "pass", "artifact_hash": "old", "source": "probe"},
            "review": {
                "status": "pass",
                "isolation": "fresh_subagent",
                "artifact_hash": "old",
            },
            "human_decision": {"status": "confirmed", "decision_id": "DEC-1"},
        },
    )
    assert stale["allowed"] is False
    assert "review_stale_hash" in stale["gaps"] or "audit_stale_hash" in stale["gaps"]


def test_high_risk_model_requires_challenge():
    result = resolve_quality_requirements(
        "model_candidate",
        "candidate",
        "adopted",
        risk="high",
        artifact_hash="abc",
        quality_evidence={
            "audit": {"status": "pass", "artifact_hash": "abc"},
            "review": {
                "status": "pass",
                "isolation": "fresh_subagent",
                "artifact_hash": "abc",
            },
            "human_decision": {"status": "confirmed"},
        },
    )
    assert result["requirements"]["challenge"]["required"] is True
    assert result["allowed"] is False
    assert "missing_challenge" in result["gaps"]


def test_conceptual_figure_uses_semantic_audit():
    result = resolve_quality_requirements(
        "paper_figure",
        "diagnostic",
        "paper",
        figure_kind="conceptual",
        artifact_hash="fig",
    )
    assert "semantic_geometry_audit" in result["requirements"]["audit"]["checks"]
    assert "data_unit_audit" not in result["requirements"]["audit"]["checks"]
    assert result["review_unit"]["one_subagent"] is True


def test_section_review_uses_question_bundle():
    result = resolve_quality_requirements(
        "manuscript_section",
        "candidate",
        "accepted-for-assembly",
        bundle={"kind": "question_bundle", "members": ["q2-text", "fig-4", "result-q2"]},
    )
    assert result["review_unit"]["kind"] == "question_bundle"
    assert result["review_unit"]["members"] == ["q2-text", "fig-4", "result-q2"]
    assert result["allowed"] is False


def test_shared_figure_designer_joins_modeler_query():
    plan = route_query("讨论一下模型结构，并设计一张模型示意图")
    assert "modeling-figure-designer" in plan["specialists"]
    assert "modeling-figure-designer" in plan["capability_candidates"]


def test_rewrite_abstract_still_does_not_load_figure_designer():
    plan = route_query("重写摘要")
    assert plan["specialists"] == ["modeling-paper-writer"]
    assert "modeling-figure-designer" not in plan["specialists"]


def test_compliance_gate_rejects_preflight_errors():
    verified = yaml.safe_load(
        (ROOT / "tests" / "fixtures" / "compliance-gate" / "verified-profile.yaml").read_text(
            encoding="utf-8"
        )
    )
    preflight = json.loads(
        (ROOT / "tests" / "fixtures" / "compliance-gate" / "preflight-with-errors.json").read_text(
            encoding="utf-8"
        )
    )
    context = json.loads(
        (ROOT / "tests" / "fixtures" / "compliance-gate" / "submission-context.json").read_text(
            encoding="utf-8"
        )
    )
    blocked = assess_compliance(
        rules_profile=verified,
        preflight_report=preflight,
        submission_context=context,
    )
    assert blocked["compliance_status"] == "unassessed"
    assert "preflight_errors" in blocked["reasons"]


def test_compliance_gate_rejects_profile_context_mismatch():
    verified = yaml.safe_load(
        (ROOT / "tests" / "fixtures" / "compliance-gate" / "verified-profile.yaml").read_text(
            encoding="utf-8"
        )
    )
    preflight = json.loads(
        (ROOT / "tests" / "fixtures" / "compliance-gate" / "preflight-complete.json").read_text(
            encoding="utf-8"
        )
    )
    mismatched = {
        "status": "resolved",
        "submission": {"rules_year": "2026", "rules_profile_id": "cumcm-2026"},
    }
    blocked = assess_compliance(
        rules_profile=verified,
        preflight_report=preflight,
        submission_context=mismatched,
    )
    assert blocked["compliance_status"] == "unassessed"
    assert "rules_profile_id_mismatch" in blocked["reasons"]
