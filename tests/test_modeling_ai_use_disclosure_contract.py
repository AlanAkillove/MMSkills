from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "modeling-ai-use-disclosure"
FIXTURES = ROOT / "tests" / "fixtures" / "modeling-ai-use-disclosure"


def test_skill_has_scope_and_human_control_gates():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "明确授权",
        "不能猜填",
        "human_confirmation_queue.md",
        "--final",
        "隐藏思维过程",
        "不得生成 final",
    ):
        assert phrase in text
    assert "AI 使用率" in text


def test_supporting_references_and_scripts_exist():
    for path in (
        SKILL / "references" / "event-schema.md",
        SKILL / "references" / "reconciliation-and-privacy.md",
        SKILL / "references" / "profile-to-pdf.md",
        SKILL / "references" / "research-basis.md",
        SKILL / "scripts" / "build_disclosure_pdf.py",
        SKILL / "scripts" / "validate_disclosure.py",
    ):
        assert path.exists(), path


def test_event_schema_covers_the_new_pre_model_stages():
    schema = (SKILL / "references" / "event-schema.md").read_text(encoding="utf-8")
    for phrase in ("topic_selection", "literature_evidence", "problem_familiarization"):
        assert phrase in schema


def test_fixture_separates_adoption_edit_and_verification():
    data = json.loads((FIXTURES / "final_input.json").read_text(encoding="utf-8"))
    assert data["confirmation"]["status"] == "confirmed"
    assert data["record_completeness"] == "complete"
    for event in data["events"]:
        assert event["adoption"]
        assert event["human_modification"]
        assert event["human_verification"]
        assert event["evidence_level"] in {"E3", "E2", "E1", "E0"}
        assert event["record_status"] == "confirmed"


def test_script_contract_mentions_pdf_and_final_gate():
    build = (SKILL / "scripts" / "build_disclosure_pdf.py").read_text(encoding="utf-8")
    validate = (SKILL / "scripts" / "validate_disclosure.py").read_text(encoding="utf-8")
    assert "STSong-Light" in build
    assert "confirmation.status=confirmed" in build
    assert "render_status" in validate
    assert re.search(r"PLACEHOLDER_RE", validate)
