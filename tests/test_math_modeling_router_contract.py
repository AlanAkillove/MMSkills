"""Contract checks for the math-modeling role router."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "math-modeling"
SCRIPT = SKILL / "scripts" / "route_role.py"
sys.path.insert(0, str(SKILL / "scripts"))
from route_role import route_query  # noqa: E402


def test_entrypoint_is_a_thin_router():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "Never preload the workflow",
        "建模手",
        "编程手",
        "论文手",
        "不从算法名称",
        "modeling-pipeline-orchestrator",
        "adopt / freeze / submit",
    ):
        assert phrase in text
    assert "RULES_PROFILE" not in text
    assert (SKILL / "references" / "roles" / "modeler.md").is_file()
    assert (SKILL / "references" / "roles" / "computationalist.md").is_file()
    assert (SKILL / "references" / "roles" / "writer.md").is_file()
    assert (SKILL / "references" / "specialist-routing.yaml").is_file()
    assert (SKILL / "references" / "progressive-disclosure.md").is_file()


def test_local_continue_does_not_preload_orchestrator_or_registry():
    plan = route_query("继续问题三")
    assert plan["intent"] == "continue_local"
    assert plan["role"] == "unknown"
    assert plan["requires_context"] is True
    assert plan["confidence"] == "low"
    assert plan["matched_rule"] == "continue_local"
    assert plan["load_orchestrator"] is False
    assert plan["load_stage_registry"] is False
    assert plan["persist_artifacts"] is False
    assert "modeling-pipeline-orchestrator" not in plan["loaded"]
    assert "modeling-process-freezer" not in plan["loaded"]
    assert "role:modeler" not in plan["loaded"]


def test_local_continue_inherits_current_role_instead_of_guessing_modeler():
    writer = route_query("继续问题三", current_role="writer")
    assert writer["role"] == "writer"
    assert writer["requires_context"] is False
    assert writer["load_orchestrator"] is False
    compute = route_query("继续问题三", current_role="computationalist")
    assert compute["role"] == "computationalist"
    inspect = route_query("检查图 8")
    assert inspect["role"] == "unknown"
    assert inspect["requires_context"] is True
    assert inspect["matched_rule"] == "figure_inspect"
    inspect_writer = route_query("检查图 8", current_role="writer")
    assert inspect_writer["role"] == "writer"
    numeric = route_query("看一下数值")
    assert numeric["role"] == "unknown"
    assert numeric["requires_context"] is True


def test_compare_models_routes_to_modeler_without_algorithm_catalog():
    plan = route_query("直接比较这几个模型")
    assert plan["role"] == "modeler"
    assert plan["specialists"] == ["modeling-model-architect"]
    assert plan["load_orchestrator"] is False


def test_rewrite_abstract_routes_to_writer():
    plan = route_query("重写摘要")
    assert plan["role"] == "writer"
    assert "modeling-paper-writer" in plan["specialists"]
    assert plan["load_orchestrator"] is False


def test_resume_may_load_orchestrator():
    plan = route_query("恢复会话并检查 process-freezer")
    assert plan["load_orchestrator"] is True
    assert "modeling-pipeline-orchestrator" in plan["loaded"]


def test_continue_from_papers_is_modeler_and_polish_section_is_writer():
    model = route_query("根据这些论文继续推模型")
    assert model["role"] == "modeler"
    assert model["requires_context"] is False
    assert model["load_orchestrator"] is False
    polish = route_query("精修 5.3")
    assert polish["role"] == "writer"
    assert polish["load_orchestrator"] is False


def test_cli_json_roundtrip():
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), "--query", "继续问题三", "--json"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["load_orchestrator"] is False
    assert payload["role"] == "unknown"
    assert payload["requires_context"] is True
