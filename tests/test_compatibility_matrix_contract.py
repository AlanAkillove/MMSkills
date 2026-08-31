from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "tests" / "compatibility" / "host-matrix.yaml"


def test_compatibility_matrix_is_capability_based_and_conservative():
    payload = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
    assert payload["source_contract"]["required_files"] == ["SKILL.md", "references", "schemas", "profiles"]
    required_states = set(payload["source_contract"]["required_states"])
    assert {"partial", "blocked", "verified"}.issubset(required_states)
    hosts = payload["hosts"]
    assert {host["host_id"] for host in hosts} == {"codex", "claude-code", "gemini-cli", "generic-agent"}
    for host in hosts:
        assert host["status"] == "fixture_only"
        assert "report_missing_capabilities" in host["smoke_actions"] or "verify_artifact" in host["smoke_actions"]
