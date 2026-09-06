"""0.3.2: problem year vs rules year, composite review, and understand routing."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "math-modeling"
RESOLVER = SKILL / "scripts" / "resolve_submission_context.py"
GATE = ROOT / "skills" / "modeling-final-preflight" / "scripts" / "check_compliance_gate.py"
CHECKER = ROOT / "skills" / "modeling-final-preflight" / "scripts" / "check_manuscript_quality.py"
FIXTURE = ROOT / "tests" / "fixtures" / "dsh-replay-2025b-cumcm2026" / "short-manuscript.tex"
WRITING = ROOT / "profiles" / "writing" / "cumcm-natural-cn.yaml"
RULES = ROOT / "references" / "rules" / "cumcm-2026.yaml"

sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(GATE.parent))
from route_role import route_query  # noqa: E402
from resolve_submission_context import resolve_submission_context  # noqa: E402
from check_compliance_gate import assess_compliance  # noqa: E402


def test_2025_problem_does_not_imply_2025_rules():
    guessed = resolve_submission_context(
        problem_competition="CUMCM",
        problem_year="2025",
        problem_code="B",
        infer_rules_from_problem=True,
    )
    assert guessed["status"] != "resolved"
    assert "rules_year_must_not_be_inferred_from_problem_year" in guessed["errors"]
    assert guessed["submission"]["rules_year"] is None

    missing = resolve_submission_context(problem_year="2025")
    assert missing["status"] == "unassessed"
    assert missing["compliance_status"] == "unassessed"

    resolved = resolve_submission_context(
        problem_competition="CUMCM",
        problem_year="2025",
        problem_code="B",
        rules_year="2026",
        rules_profile_id="cumcm-2026",
        writing_profile_id="cumcm-natural-cn",
    )
    assert resolved["status"] == "resolved"
    assert resolved["problem"]["year"] == "2025"
    assert resolved["submission"]["rules_year"] == "2026"
    assert resolved["submission"]["rules_profile_id"] == "cumcm-2026"


def test_compliance_claim_without_profile_is_illegal():
    gate = assess_compliance(claimed_status="格式合规")
    assert gate["compliance_status"] == "unassessed"
    assert gate["illegal_compliance_claim"] is True
    lied = assess_compliance(
        rules_profile_id="cumcm-2026",
        rules_year="2026",
        official_source_verified=True,
        required_checks_executed=True,
        claimed_status="passed",
    )
    assert lied["compliance_status"] == "unassessed"
    assert lied["caller_assertions_ignored"] is True


def test_compliance_gate_reads_profile_instead_of_caller_bools():
    import yaml

    draft = yaml.safe_load(RULES.read_text(encoding="utf-8"))
    blocked = assess_compliance(
        rules_profile=draft,
        official_source_verified=True,
        required_checks_executed=True,
        claimed_status="格式合规",
    )
    assert blocked["compliance_status"] == "unassessed"
    assert "profile_status_draft" in blocked["reasons"]
    assert "human_confirmation_pending" in blocked["reasons"]
    assert blocked["illegal_compliance_claim"] is True

    verified = yaml.safe_load(
        (ROOT / "tests" / "fixtures" / "compliance-gate" / "verified-profile.yaml").read_text(
            encoding="utf-8"
        )
    )
    preflight = json.loads(
        (ROOT / "tests" / "fixtures" / "compliance-gate" / "preflight-complete.json").read_text(
            encoding="utf-8"
        )
    )
    context = json.loads(
        (ROOT / "tests" / "fixtures" / "compliance-gate" / "submission-context.json").read_text(
            encoding="utf-8"
        )
    )
    passed = assess_compliance(
        rules_profile=verified,
        preflight_report=preflight,
        submission_context=context,
        claimed_status="passed",
    )
    assert passed["compliance_status"] == "passed"
    assert passed["illegal_compliance_claim"] is False


def test_understand_does_not_create_intake_or_question_map_intent():
    plan = route_query("阅读赛题内容并进行分析，让我理解主要内容、背景知识及主要问题。")
    assert plan["intent"] == "understand"
    assert plan["specialists"] == ["modeling-problem-familiarization"]
    assert plan["persist_artifacts"] is False
    assert "modeling-problem-intake" not in plan["specialists"]
    familiar = route_query("先帮我弄懂这个微通道结构。")
    assert familiar["intent"] == "understand"
    assert familiar["persist_artifacts"] is False
    assert familiar["specialists"] == ["modeling-problem-familiarization"]


def test_formal_intake_is_opt_in():
    plan = route_query("现在把已经确认的题意整理成正式问题地图")
    assert plan["intent"] == "formal_intake"
    assert plan["specialists"] == ["modeling-problem-intake"]
    assert plan["persist_artifacts"] is True


def test_composite_review_loads_writer_specialists_and_requires_subagent():
    plan = route_query(
        "从写作质量、论文结构、语言表达、术语规范、格式规范等多个方面进行审阅。"
    )
    assert plan["intent"] == "composite_review"
    assert plan["role"] == "writer"
    assert plan["review_isolation"] == "required_subagent"
    for name in (
        "modeling-paper-reviewer",
        "modeling-reader-experience-auditor",
        "modeling-terminology-auditor",
        "modeling-ai-pattern-reviewer",
        "modeling-rules-profile",
        "modeling-final-preflight",
    ):
        assert name in plan["specialists"]
    assert "modeling-paper-writer" not in plan["specialists"]
    assert "modeling-paper-naturalizer" not in plan["specialists"]
    assert len(plan["specialists"]) > 2


def test_final_review_requires_independent_subagent():
    plan = route_query("审阅论文")
    assert plan["intent"] == "review"
    assert plan["specialists"] == ["modeling-paper-reviewer"]
    assert plan["review_isolation"] == "required_subagent"


def test_sanitized_dsh_manuscript_fails_writing_profile(tmp_path: Path):
    report = tmp_path / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            str(FIXTURE),
            "--writing-profile",
            str(WRITING),
            "--rules-profile",
            str(RULES),
            "--pdf-pages",
            "11",
            "--preferred-pages",
            "26,28",
            "--output",
            str(report),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(report.read_text(encoding="utf-8"))
    categories = {item["category"] for item in payload["findings"]}
    assert payload["metrics"]["cite_keys"] == 0
    assert payload["metrics"]["bibitems"] >= 1
    for required in (
        "wrong-rules-year-page-limit",
        "english-abstract-forbidden",
        "boxed-equation",
        "unordered-list-forbidden",
        "orphan-bibliography",
        "coverage-short",
        "problem-restatement-section",
    ):
        assert required in categories


def test_resolver_and_gate_cli_roundtrip():
    resolved = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(RESOLVER),
            "--problem-year",
            "2025",
            "--rules-year",
            "2026",
            "--rules-profile-id",
            "cumcm-2026",
            "--json",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert resolved.returncode == 0, resolved.stderr
    illegal = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(GATE),
            "--claimed-status",
            "compliant",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert illegal.returncode == 1
    payload = json.loads(illegal.stdout)
    assert payload["illegal_compliance_claim"] is True
