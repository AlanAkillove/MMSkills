"""Deterministic package checks for modeling-terminology-auditor."""

from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-terminology-auditor"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-terminology-auditor"
TEMPLATE = ROOT / "templates" / "terminology_ledger.md"


def test_entrypoint_has_term_boundaries():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-terminology-auditor" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "standard",
        "project-defined",
        "同义漂移",
        "生造",
        "高级感",
        "不机械全局替换",
        "Research Chair/用户",
        "establish",
        "audit",
        "terminology_table.md",
    ):
        assert phrase in content


def test_references_define_schema_rubric_and_cross_checks():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for name in (
        "terminology-schema.md",
        "term-decision-rubric.md",
        "cross-artifact-consistency.md",
        "research-basis.md",
    ):
        assert name in content
        assert (SKILL_DIR / "references" / name).is_file()
    schema = (SKILL_DIR / "references" / "terminology-schema.md").read_text(encoding="utf-8")
    rubric = (SKILL_DIR / "references" / "term-decision-rubric.md").read_text(encoding="utf-8")
    cross = (SKILL_DIR / "references" / "cross-artifact-consistency.md").read_text(encoding="utf-8")
    for phrase in ("concept_id", "canonical_term", "unit/dimension", "term_candidate"):
        assert phrase in schema
    for phrase in ("明确指称", "鲁棒", "最优"):
        assert phrase in rubric
    for phrase in ("数据字典", "代码", "图表", "主张矩阵"):
        assert phrase in cross


def test_shared_terminology_template_is_present():
    content = TEMPLATE.read_text(encoding="utf-8")
    for phrase in ("Concept register", "canonical_term", "Human decisions", "K-001"):
        assert phrase in content
    table = (ROOT / "templates" / "terminology_table.md").read_text(encoding="utf-8")
    for phrase in ("zh_canonical", "en_canonical", "ambiguous_or_deprecated", "domain_range"):
        assert phrase in table


def test_fixture_set_covers_term_drift_and_conflicts():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "positive-standard-and-defined-term.md",
        "positive-valid-alias.md",
        "negative-synonym-drift.md",
        "negative-invented-high-register.md",
        "negative-symbol-unit-conflict.md",
        "negative-cross-artifact-drift.md",
        "expected-behavior.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in ("标准术语", "高级感", "P0/P1", "不能全局替换"):
        assert phrase in expected


def test_drift_scanner_flags_unregistered_wrapper_terms(tmp_path: Path):
    script = SKILL_DIR / "scripts" / "check_terminology_drift.py"
    report = tmp_path / "drift.json"
    bad = subprocess.run(
        [
            sys.executable,
            str(script),
            "--table",
            str(FIXTURE_DIR / "table-flow-maldistribution.md"),
            "--manuscript",
            str(FIXTURE_DIR / "manuscript-wrapper-term.tex"),
            "--json-out",
            str(report),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert bad.returncode == 1, bad.stdout + bad.stderr
    kinds = {item["kind"] for item in json.loads(report.read_text(encoding="utf-8"))}
    assert "deprecated-or-ambiguous-alias" in kinds or "unregistered-wrapper" in kinds
    good = subprocess.run(
        [
            sys.executable,
            str(script),
            "--table",
            str(FIXTURE_DIR / "table-flow-maldistribution.md"),
            "--manuscript",
            str(FIXTURE_DIR / "manuscript-canonical.tex"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert good.returncode == 0, good.stdout + good.stderr


if __name__ == "__main__":
    for test in (
        test_entrypoint_has_term_boundaries,
        test_references_define_schema_rubric_and_cross_checks,
        test_shared_terminology_template_is_present,
        test_fixture_set_covers_term_drift_and_conflicts,
    ):
        test()
    print("modeling-terminology-auditor contract: OK")
