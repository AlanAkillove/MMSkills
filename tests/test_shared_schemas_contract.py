from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FINDING_FIXTURES = ROOT / "tests" / "fixtures" / "finding-protocol"
MERGE_SCRIPT = ROOT / "skills" / "modeling-pipeline-orchestrator" / "scripts" / "merge_findings.py"
PROFILE_SCHEMA = json.loads((SCHEMAS / "run-profile.schema.json").read_text(encoding="utf-8"))


def test_shared_schema_files_are_valid_json_and_have_contract_metadata():
    expected = {
        "stage-registry.schema.json",
        "pipeline-state.schema.json",
        "decision.schema.json",
        "evidence.schema.json",
        "finding.schema.json",
        "model.schema.json",
        "experiment.schema.json",
        "ai-use-event.schema.json",
        "run-profile.schema.json",
    }
    for name in expected:
        payload = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
        assert payload["$schema"].startswith("https://json-schema.org/")
        assert payload["type"] == "object"
        assert payload.get("required")
        Draft202012Validator.check_schema(payload)


def test_canonical_registry_and_finding_examples_validate_against_machine_schemas():
    registry_schema = json.loads((SCHEMAS / "stage-registry.schema.json").read_text(encoding="utf-8"))
    registry = json.loads((SCHEMAS / "stage-registry.json").read_text(encoding="utf-8"))
    assert not list(Draft202012Validator(registry_schema).iter_errors(registry))

    finding_schema = json.loads((SCHEMAS / "finding.schema.json").read_text(encoding="utf-8"))
    finding_validator = Draft202012Validator(finding_schema)
    example = json.loads((ROOT / "templates" / "finding_record.json").read_text(encoding="utf-8"))
    assert not list(finding_validator.iter_errors(example))
    for path in FINDING_FIXTURES.glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line:
                assert not list(finding_validator.iter_errors(json.loads(line)))


def test_stage_registry_is_the_ordered_and_topological_source_of_truth():
    registry = json.loads((SCHEMAS / "stage-registry.json").read_text(encoding="utf-8"))
    order = registry["default_order"]
    assert set(order) == set(registry["stages"])
    positions = {stage: index for index, stage in enumerate(order)}
    gate_types = set()
    for stage, record in registry["stages"].items():
        assert all(positions[dependency] < positions[stage] for dependency in record["depends_on"])
        assert record["gate_type"] in {"core_decision", "review_checkpoint", "none"}
        gate_types.add(record["gate_type"])
        if record["gate_type"] == "core_decision":
            assert record["human_gate"] == "required"
    assert {"core_decision", "review_checkpoint"} <= gate_types
    assert positions["distinctiveness_coach"] < positions["model_architect"]
    for lens_name, spec in registry["review_lenses"].items():
        assert spec["stage"] in registry["stages"], lens_name


def test_run_profiles_cross_validate_against_registry_and_schema():
    registry = json.loads((SCHEMAS / "stage-registry.json").read_text(encoding="utf-8"))
    known_stages = set(registry["stages"])
    known_lenses = set(registry["review_lenses"])
    core_decisions = {
        stage for stage, record in registry["stages"].items() if record["gate_type"] == "core_decision"
    }
    expected_ids = {"research-full", "contest-standard", "contest-fast"}
    profile_ids = set()
    validator = Draft202012Validator(PROFILE_SCHEMA)
    for path in (ROOT / "profiles").glob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert not list(validator.iter_errors(payload)), path
        profile_ids.add(payload["profile_id"])
        assert payload["profile_id"] in expected_ids
        assert payload["principles_preserved"]
        assert {"human_decision_gates", "evidence_before_prose", "truthful_ai_disclosure"}.issubset(
            payload["principles_preserved"]
        )
        unknown_gates = [gate for gate in payload["human_gates"] if gate not in known_stages]
        assert unknown_gates == [], unknown_gates
        missing_core = sorted(core_decisions - set(payload["human_gates"]))
        assert missing_core == [], missing_core
        review_policy = payload["review_policy"]
        for lens in review_policy["lenses"] + review_policy.get("conditional_lenses", []):
            assert lens in known_lenses, lens
    assert profile_ids == expected_ids


def test_finding_merge_groups_by_issue_key_and_unions_distinct_anchors(tmp_path: Path):
    output = tmp_path / "finding_register.jsonl"
    report = tmp_path / "merge_report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(MERGE_SCRIPT),
            "--input",
            str(FINDING_FIXTURES / "review_findings.jsonl"),
            "--input",
            str(FINDING_FIXTURES / "reader_findings.jsonl"),
            "--output",
            str(output),
            "--report",
            str(report),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines() if line]
    assert len(records) == 1
    assert records[0]["source_record_count"] == 2
    assert set(records[0]["source_skills"]) == {"modeling-paper-reviewer", "modeling-reader-experience-auditor"}
    assert records[0]["deduplication"]["relation"] == "supplement"
    anchor_ids = {anchor["anchor_id"] for anchor in records[0]["evidence_anchors"]}
    assert anchor_ids == {"p3-table2", "fig4-y", "fig4-caption"}
    assert set(records[0]["related_claim_ids"]) == {"claim-metric-1"}
    assert set(records[0]["related_term_ids"]) == {"term-metric"}
    assert set(records[0]["related_figure_ids"]) == {"fig4"}
    merge_report = json.loads(report.read_text(encoding="utf-8"))
    assert merge_report["grouping_key"] == "canonical_issue_key"
    assert merge_report["input_record_count"] == 2
    assert merge_report["groups"][0]["action"] == "supplement_merged"


def test_finding_merge_does_not_take_first_record_status_when_open_and_resolved_conflict(tmp_path: Path):
    output = tmp_path / "conflict_register.jsonl"
    report = tmp_path / "conflict_report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(MERGE_SCRIPT),
            "--input",
            str(FINDING_FIXTURES / "conflict_status_findings.jsonl"),
            "--output",
            str(output),
            "--report",
            str(report),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines() if line]
    assert len(records) == 1
    assert records[0]["status"] == "needs_human"
    assert records[0]["human_status"] == "needs-human-confirmation"
    assert records[0]["deduplication"]["relation"] == "conflict"
    anchor_ids = {anchor["anchor_id"] for anchor in records[0]["evidence_anchors"]}
    assert anchor_ids == {"sec5-p2", "matrix-row-12"}
    merge_report = json.loads(report.read_text(encoding="utf-8"))
    assert merge_report["groups"][0]["action"] == "human_review_required"
    assert "resolved" in merge_report["groups"][0]["statuses"]
    assert "open" in merge_report["groups"][0]["statuses"]
