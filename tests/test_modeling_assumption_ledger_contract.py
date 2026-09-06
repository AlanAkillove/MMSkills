"""Deterministic package checks for modeling-assumption-ledger."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-assumption-ledger"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-assumption-ledger"


def test_entrypoint_has_scope_and_human_gate():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-assumption-ledger" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "problem_fact",
        "team_assumption",
        "证据状态",
        "needs-human-confirmation",
        "Research Chair/用户批准",
        "不伪造",
        "Assumption Challenger",
    ):
        assert phrase in content


def test_references_define_impact_and_lifecycle():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for name in (
        "assumption-schema.md",
        "impact-and-validation.md",
        "research-basis.md",
    ):
        assert name in content
        assert (SKILL_DIR / "references" / name).is_file()
    schema = (SKILL_DIR / "references" / "assumption-schema.md").read_text(encoding="utf-8")
    guide = (SKILL_DIR / "references" / "impact-and-validation.md").read_text(encoding="utf-8")
    for phrase in ("assumption_id", "accepted_with_limits", "decision_id", "evidence_status", "assumption_checkpoint", "P0", "P1"):
        assert phrase in schema
    for phrase in ("题意/结构影响", "反事实问题", "not-run", "inconclusive"):
        assert phrase in guide


def test_fixture_set_covers_common_assumption_failures():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "positive-explicit-assumptions.md",
        "positive-nonoptimization-boundary.md",
        "negative-silent-topic-change.md",
        "negative-unverified-independence.md",
        "negative-code-paper-conflict.md",
        "negative-unsupported-sensitivity.md",
        "expected-behavior.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in ("阻断", "不伪造", "论文和代码证据", "人工确认门"):
        assert phrase in expected


if __name__ == "__main__":
    for test in (
        test_entrypoint_has_scope_and_human_gate,
        test_references_define_impact_and_lifecycle,
        test_fixture_set_covers_common_assumption_failures,
    ):
        test()
    print("modeling-assumption-ledger contract: OK")
