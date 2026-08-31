"""Deterministic package checks for modeling-claim-evidence-audit."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-claim-evidence-audit"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-claim-evidence-audit"
MATRIX = ROOT / "templates" / "claim_evidence_matrix.csv"


def test_entrypoint_has_evidence_boundary_and_human_gate():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-claim-evidence-audit" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "claim",
        "evidence",
        "不编造",
        "最优",
        "因果",
        "human-confirmed",
        "Research Chair/用户",
    ):
        assert phrase in content


def test_references_define_claim_schema_and_calibration():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for name in (
        "claim-schema.md",
        "strength-calibration.md",
        "audit-workflow.md",
        "research-basis.md",
    ):
        assert name in content
        assert (SKILL_DIR / "references" / name).is_file()
    schema = (SKILL_DIR / "references" / "claim-schema.md").read_text(encoding="utf-8")
    calibration = (SKILL_DIR / "references" / "strength-calibration.md").read_text(encoding="utf-8")
    for phrase in ("claim_id", "evidence_ids", "evidence_scope", "contradicted", "human_verified"):
        assert phrase in schema
    for phrase in ("全局最优", "因果", "鲁棒", "普适"):
        assert phrase in calibration


def test_shared_matrix_header_matches_claim_schema():
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    header = rows[0]
    for field in (
        "claim_id",
        "claim_text",
        "claim_role",
        "evidence_ids",
        "evidence_status",
        "evidence_scope",
        "verdict",
        "severity",
        "audit_confidence",
        "human_verified",
    ):
        assert field in header
    assert len(rows[1]) == len(header)


def test_fixture_set_covers_strength_and_conflict_failures():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "positive-within-scope.md",
        "positive-limited-claim.md",
        "negative-causal-overclaim.md",
        "negative-optimality-overclaim.md",
        "negative-robustness-overclaim.md",
        "negative-accuracy-mismatch.md",
        "negative-evidence-conflict.md",
        "expected-behavior.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in ("补证据", "限缩主张", "contradictory", "不得编造"):
        assert phrase in expected


if __name__ == "__main__":
    for test in (
        test_entrypoint_has_evidence_boundary_and_human_gate,
        test_references_define_claim_schema_and_calibration,
        test_shared_matrix_header_matches_claim_schema,
        test_fixture_set_covers_strength_and_conflict_failures,
    ):
        test()
    print("modeling-claim-evidence-audit contract: OK")
