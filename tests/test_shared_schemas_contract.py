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
    for stage, record in registry["stages"].items():
        assert all(positions[dependency] < positions[stage] for dependency in record["depends_on"])
        assert record["human_gate"] == "required"
    assert positions["distinctiveness_coach"] < positions["model_architect"]


def test_run_profiles_have_ids_core_principles_and_human_gates():
    expected_ids = {"research-full", "contest-standard", "contest-fast"}
    profile_ids = set()
    for path in (ROOT / "profiles").glob("*.yaml"):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        profile_ids.add(payload["profile_id"])
        assert payload["profile_id"] in expected_ids
        assert payload["principles_preserved"]
        assert payload["human_gates"]
        assert {"human_decision_gates", "evidence_before_prose", "truthful_ai_disclosure"}.issubset(payload["principles_preserved"])
    assert profile_ids == expected_ids


def test_finding_merge_preserves_sources_and_collapses_same_issue(tmp_path: Path):
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
    merge_report = json.loads(report.read_text(encoding="utf-8"))
    assert merge_report["input_record_count"] == 2
    assert merge_report["groups"][0]["action"] == "supplement_merged"
