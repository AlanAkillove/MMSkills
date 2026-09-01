from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "modeling-pipeline-orchestrator"
FIXTURES = ROOT / "tests" / "fixtures" / "modeling-pipeline-orchestrator"
SCRIPT = SKILL / "scripts" / "route_pipeline.py"
RUNTIME = SKILL / "scripts" / "pipeline_runtime.py"
REGISTRY = ROOT / "schemas" / "stage-registry.json"
sys.path.insert(0, str(SKILL / "scripts"))
from pipeline_runtime import (  # noqa: E402
    build_effective_stage_policy,
    ready_stages,
    validate_state,
)


def run_route(
    input_path: Path,
    output_path: Path,
    *extra: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--input", str(input_path), "--output", str(output_path), *extra],
        text=True,
        capture_output=True,
        check=False,
    )


def test_skill_has_router_only_and_human_gate_boundary():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "不是自动作者",
        "不能自行解释题意",
        "entry_ambiguous",
        "needs_human",
        "不能把用户未回复当作确认",
        "不修改论文、模型、数据和状态",
        "core_decision",
        "review_checkpoint",
        "effective_stage_policy",
        "user intent",
        "硬依赖",
        "recommended_after",
        "暂定",
    ):
        assert phrase in text


def test_graph_and_contract_references_exist():
    for path in (
        SKILL / "references" / "pipeline-contract.md",
        SKILL / "references" / "dependency-graph.md",
        SKILL / "references" / "gates-and-handoff.md",
        SKILL / "references" / "research-basis.md",
        SCRIPT,
        RUNTIME,
    ):
        assert path.exists(), path
    graph = (SKILL / "references" / "dependency-graph.md").read_text(encoding="utf-8")
    for stage in ("topic_selection", "problem_intake", "literature_evidence", "problem_familiarization", "model_architect", "figure_design", "paper_review", "ai_disclosure", "final_preflight"):
        assert stage in graph


def test_route_finds_ready_stages_without_mutating_input(tmp_path: Path):
    source = FIXTURES / "initial_state.json"
    output = tmp_path / "run_plan.md"
    before = source.read_text(encoding="utf-8")
    result = run_route(source, output)
    assert result.returncode == 0, result.stderr
    text = output.read_text(encoding="utf-8")
    assert "problem_intake" in text
    assert "figure_design" in text
    assert "ai_disclosure" in text
    assert "does not confirm mathematical correctness" in text
    assert "Canonical dependencies are unchanged" in text
    assert source.read_text(encoding="utf-8") == before


def test_multi_topic_entry_routes_to_selection_before_intake(tmp_path: Path):
    output = tmp_path / "multi-topic.md"
    result = run_route(FIXTURES / "multi_topic_state.json", output)
    assert result.returncode == 0, result.stderr
    assert "READY: topic_selection, ai_disclosure" in result.stdout
    text = output.read_text(encoding="utf-8")
    assert "Run topic_selection through modeling-topic-selection" in text


def test_pre_model_dependencies_keep_intake_after_familiarization():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    stages = registry["stages"]
    assert stages["literature_evidence"]["depends_on"] == ["topic_selection"]
    assert stages["problem_familiarization"]["depends_on"] == ["literature_evidence", "topic_selection"]
    assert stages["problem_intake"]["depends_on"] == ["problem_familiarization", "topic_selection"]
    assert stages["distinctiveness_coach"]["depends_on"] == ["problem_intake", "problem_familiarization"]
    assert "distinctiveness_coach" in registry["default_order"]
    assert stages["topic_selection"]["gate_type"] == "core_decision"
    assert stages["terminology"]["gate_type"] == "review_checkpoint"
    assert stages["paper_architect"]["human_gate"] == "optional"
    assert stages["draft"]["skill"] == "modeling-paper-writer"
    assert stages["draft"]["depends_on"] == []
    assert "paper_architect" in stages["draft"]["recommended_after"]
    assert "experiment_validator" in stages["draft"]["recommended_after"]
    assert "claim_evidence" in stages["draft"]["recommended_after"]
    assert stages["naturalizer"]["depends_on"] == ["draft"]


def test_pre_model_graph_is_topologically_ordered():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    order = registry["default_order"]
    positions = {stage: order.index(stage) for stage in order}
    assert positions["topic_selection"] < positions["literature_evidence"]
    assert positions["literature_evidence"] < positions["problem_familiarization"]
    assert positions["problem_familiarization"] < positions["problem_intake"]
    assert positions["problem_intake"] < positions["distinctiveness_coach"] < positions["model_architect"]
    assert positions["problem_intake"] < positions["assumption_ledger"] < positions["model_architect"]


def test_route_reports_blocked_stage_and_rejects_unknown_stage(tmp_path: Path):
    blocked_output = tmp_path / "blocked.md"
    result = run_route(FIXTURES / "blocked_state.json", blocked_output)
    assert result.returncode == 0
    text = blocked_output.read_text(encoding="utf-8")
    assert "题面图示关系未确认" in text
    assert "Blocked or recheck" in text
    assert "Run ai_disclosure through modeling-ai-use-disclosure" in text
    assert "Open the ready stage's input artifacts" in text

    invalid_output = tmp_path / "invalid.md"
    invalid = run_route(FIXTURES / "invalid_state.json", invalid_output)
    assert invalid.returncode != 0
    assert "unknown stage" in invalid.stderr


def test_route_rejects_schema_invalid_and_human_confirmed_without_decision(tmp_path: Path):
    schema_invalid = run_route(FIXTURES / "invalid_schema_state.json", tmp_path / "schema.md")
    assert schema_invalid.returncode != 0
    assert "schema" in schema_invalid.stderr

    confirmed = run_route(
        FIXTURES / "invalid_confirmed_without_decision.json",
        tmp_path / "confirmed.md",
    )
    assert confirmed.returncode != 0
    assert "decision_id" in confirmed.stderr


def test_route_uses_human_gate_action_when_no_stage_is_ready(tmp_path: Path):
    output = tmp_path / "needs-human.md"
    result = run_route(FIXTURES / "needs_human_state.json", output)
    assert result.returncode == 0
    text = output.read_text(encoding="utf-8")
    assert "READY: none" in result.stdout
    assert "Resolve the listed human gates" in text
    assert "Open the ready stage's input artifacts" not in text


def test_route_rejects_unknown_run_profile(tmp_path: Path):
    source = FIXTURES / "initial_state.json"
    output = tmp_path / "unknown-profile.md"
    result = run_route(source, output, "--profile", "made-up-profile")
    assert result.returncode != 0
    assert "unknown run profile" in result.stderr


def test_contest_fast_changes_effective_graph_without_rewriting_dependencies(tmp_path: Path):
    source = FIXTURES / "post_draft_state.json"
    full_output = tmp_path / "full.md"
    fast_output = tmp_path / "fast.md"
    policy_json = tmp_path / "fast_policy.json"
    full = run_route(source, full_output, "--profile", "research-full")
    fast = run_route(
        source,
        fast_output,
        "--profile",
        "contest-fast",
        "--policy-json",
        str(policy_json),
    )
    assert full.returncode == 0, full.stderr
    assert fast.returncode == 0, fast.stderr
    assert "paper_review" in full.stdout
    assert "ai_pattern" in full.stdout
    assert "anti_homogenization" in full.stdout
    assert "reader" in full.stdout
    assert "READY:" in fast.stdout
    assert "paper_review" in fast.stdout
    assert "reader" in fast.stdout
    assert "ai_pattern" not in fast.stdout.split("READY:", 1)[1]
    assert "anti_homogenization" not in fast.stdout.split("READY:", 1)[1]
    policy = json.loads(policy_json.read_text(encoding="utf-8"))
    assert policy["canonical_dependencies_unchanged"] is True
    assert policy["stages"]["naturalizer"]["depends_on"] == ["draft"]
    assert set(policy["stages"]["naturalizer"]["recommended_after"]) == {
        "paper_review",
        "ai_pattern",
        "anti_homogenization",
        "reader",
    }
    assert policy["stages"]["ai_pattern"]["execution"] == "skipped-with-policy"
    assert policy["stages"]["anti_homogenization"]["execution"] == "skipped-with-policy"
    assert policy["stages"]["paper_review"]["execution"] == "selected"
    assert policy["stages"]["reader"]["execution"] == "selected"
    assert policy["stages"]["model_architect"]["blocking"] is True
    assert policy["stages"]["terminology"]["blocking"] is False
    fast_text = fast_output.read_text(encoding="utf-8")
    assert "compact" in fast_text
    assert "Deferred review checkpoints" in fast_text


def test_effective_policy_treats_unselected_lenses_as_satisfied_for_dependents():
    state = json.loads((FIXTURES / "post_draft_state.json").read_text(encoding="utf-8"))
    state["run_profile"] = "contest-fast"
    state["stages"]["paper_review"] = {"status": "passed", "reason": "fixture substantive lens"}
    state["stages"]["reader"] = {"status": "passed", "reason": "fixture reader lens"}
    policy = build_effective_stage_policy(state)
    ready = ready_stages(state, policy=policy)
    assert "naturalizer" in ready
    assert "ai_pattern" not in ready
    assert policy["stages"]["naturalizer"]["depends_on"] == ["draft"]


def test_explicit_user_intent_prioritizes_ready_stage_without_changing_hard_dependencies(tmp_path: Path):
    output = tmp_path / "intent.md"
    result = run_route(
        FIXTURES / "post_draft_state.json",
        output,
        "--intent",
        "revise",
        "--collaboration-mode",
        "light",
    )
    assert result.returncode == 0, result.stderr
    assert "Collaboration mode: light" in output.read_text(encoding="utf-8")
    assert "User intent: revise" in output.read_text(encoding="utf-8")
    assert "Intent target: naturalizer" in output.read_text(encoding="utf-8")
    assert "recommended_after entries are advisory" in output.read_text(encoding="utf-8")


def test_draft_is_ready_without_optional_review_reports():
    state = json.loads((FIXTURES / "post_draft_state.json").read_text(encoding="utf-8"))
    state["stages"]["draft"] = {"status": "not_started"}
    for stage in ("figure_design", "figure_table", "claim_evidence", "terminology"):
        state["stages"][stage] = {"status": "not_started"}
    state["run_profile"] = "contest-standard"
    policy = build_effective_stage_policy(state)
    assert "draft" in ready_stages(state, policy=policy)


def test_validate_state_rejects_registry_dependency_conflict():
    state = json.loads((FIXTURES / "initial_state.json").read_text(encoding="utf-8"))
    state["stages"]["problem_intake"] = {
        "status": "not_started",
        "depends_on": ["model_architect"],
    }
    errors = validate_state(state)
    assert any("depends_on conflicts with the registry" in item for item in errors)


def test_negative_fixtures_are_explicit():
    assert "不代表真实项目状态" in (FIXTURES / "README.md").read_text(encoding="utf-8")
    for phrase, name in (
        ("不能作为通过条件", "expected-behavior.md"),
        ("未知 stage", "expected-behavior.md"),
        ("题意解释被阻断", "README.md"),
        ("schema 必填", "README.md"),
        ("contest-fast", "README.md"),
    ):
        assert phrase in (FIXTURES / name).read_text(encoding="utf-8")


def test_unready_intent_focuses_ready_hard_prerequisites():
    state = json.loads((FIXTURES / "post_draft_state.json").read_text(encoding="utf-8"))
    state["user_intent"] = {"goal": "revise"}
    state["stages"]["draft"] = {"status": "not_started"}
    state["stages"]["naturalizer"] = {"status": "not_started"}
    policy = build_effective_stage_policy(state)
    assert ready_stages(state, policy=policy) == ["draft"]


def test_collaboration_mode_overrides_optional_depth_but_not_core_gates():
    state = json.loads((FIXTURES / "post_draft_state.json").read_text(encoding="utf-8"))
    state["collaboration_mode"] = "light"
    light = build_effective_stage_policy(state)
    assert light["collaboration_mode"] == "light"
    assert light["stages"]["model_architect"]["blocking"] is True
    assert set(light["review_gates"]) <= {"paper_review", "reader", "naturalizer"}
    assert "reader_experience" in light["selected_lenses"]
    assert light["stages"]["paper_architect"]["artifact_projection"] == "compact"

    state["collaboration_mode"] = "full"
    full = build_effective_stage_policy(state)
    assert full["collaboration_mode"] == "full"
    assert set(full["selected_lenses"]) == set(full["review_policy"]["lenses"])
    assert full["stages"]["paper_architect"]["artifact_projection"] == "full"
    assert full["stages"]["ai_pattern"]["blocking"] is True


def test_explicit_draft_intent_can_bootstrap_without_state_artifact(tmp_path: Path):
    output = tmp_path / "draft.md"
    result = run_route(FIXTURES / "initial_state.json", output, "--intent", "draft")
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("WROTE:")
    assert "READY: draft" in result.stdout
    assert "Intent target: draft" in output.read_text(encoding="utf-8")
