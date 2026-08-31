from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "modeling-pipeline-orchestrator"
FIXTURES = ROOT / "tests" / "fixtures" / "modeling-pipeline-orchestrator"
SCRIPT = SKILL / "scripts" / "route_pipeline.py"


def run_route(input_path: Path, output_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--input", str(input_path), "--output", str(output_path)],
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
    ):
        assert phrase in text


def test_graph_and_contract_references_exist():
    for path in (
        SKILL / "references" / "pipeline-contract.md",
        SKILL / "references" / "dependency-graph.md",
        SKILL / "references" / "gates-and-handoff.md",
        SKILL / "references" / "research-basis.md",
        SCRIPT,
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
    assert source.read_text(encoding="utf-8") == before


def test_multi_topic_entry_routes_to_selection_before_intake(tmp_path: Path):
    output = tmp_path / "multi-topic.md"
    result = run_route(FIXTURES / "multi_topic_state.json", output)
    assert result.returncode == 0, result.stderr
    assert "READY: topic_selection, ai_disclosure" in result.stdout
    text = output.read_text(encoding="utf-8")
    assert "Run topic_selection through modeling-topic-selection" in text


def test_pre_model_dependencies_keep_intake_after_familiarization():
    source = (SKILL / "scripts" / "route_pipeline.py").read_text(encoding="utf-8")
    assert '"literature_evidence", ("modeling-literature-evidence", ["topic_selection"]' in source
    assert '"problem_familiarization", ("modeling-problem-familiarization", ["literature_evidence", "topic_selection"]' in source
    assert '"problem_intake", ("modeling-problem-intake", ["problem_familiarization", "topic_selection"]' in source


def test_pre_model_graph_is_topologically_ordered():
    source = (SKILL / "scripts" / "route_pipeline.py").read_text(encoding="utf-8")
    positions = {
        stage: source.index(f'("{stage}",')
        for stage in (
            "topic_selection",
            "literature_evidence",
            "problem_familiarization",
            "problem_intake",
            "assumption_ledger",
            "data_audit",
            "model_architect",
        )
    }
    assert positions["topic_selection"] < positions["literature_evidence"]
    assert positions["literature_evidence"] < positions["problem_familiarization"]
    assert positions["problem_familiarization"] < positions["problem_intake"]
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


def test_route_uses_human_gate_action_when_no_stage_is_ready(tmp_path: Path):
    output = tmp_path / "needs-human.md"
    result = run_route(FIXTURES / "needs_human_state.json", output)
    assert result.returncode == 0
    text = output.read_text(encoding="utf-8")
    assert "READY: none" in result.stdout
    assert "Resolve the listed human gates" in text
    assert "Open the ready stage's input artifacts" not in text


def test_negative_fixtures_are_explicit():
    assert "不代表真实项目状态" in (FIXTURES / "README.md").read_text(encoding="utf-8")
    for phrase, name in (
        ("不能作为通过条件", "expected-behavior.md"),
        ("未知 stage", "expected-behavior.md"),
        ("题意解释被阻断", "README.md"),
    ):
        assert phrase in (FIXTURES / name).read_text(encoding="utf-8")
