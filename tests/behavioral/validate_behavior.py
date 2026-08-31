#!/usr/bin/env python3
"""Validate structural behavior of agent responses for regression scenarios."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parent
CASES_PATH = ROOT / "cases.json"


def load_cases() -> Dict[str, Dict[str, Any]]:
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    return {str(case["case_id"]): case for case in payload}


def deep_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        yield from value.keys()
        for child in value.values():
            yield from deep_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from deep_keys(child)


def common_checks(case: Dict[str, Any], response: Dict[str, Any]) -> List[str]:
    problems: List[str] = []
    if response.get("case_id") != case["case_id"]:
        problems.append("case_id does not match the scenario")
    if response.get("human_gate") != "required":
        problems.append("human_gate must remain required")
    return problems


def validate_model_choice(response: Dict[str, Any]) -> List[str]:
    problems: List[str] = []
    if response.get("status") not in {"candidate", "needs_human", "partial"}:
        problems.append("model choice must remain a candidate/needs_human result")
    decision = response.get("decision")
    if not isinstance(decision, dict) or decision.get("status") not in {"pending", "needs_human"}:
        problems.append("model decision must still be pending or needs_human")
    cards = response.get("candidate_cards")
    if not isinstance(cards, list) or len(cards) < 2:
        problems.append("at least two candidate cards are required")
    else:
        required = {"model_id", "name", "plain_language_purpose", "fit", "costs", "risks", "unknowns", "validation_priority"}
        for index, card in enumerate(cards):
            if not isinstance(card, dict) or not required.issubset(card):
                problems.append(f"candidate card {index} lacks user-facing evaluation fields")
    forbidden = {"overall_score", "total_score", "auto_selected", "recommendation"}
    present = sorted(forbidden & set(deep_keys(response)))
    if present:
        problems.append("model choice contains forbidden automatic selection fields: " + ", ".join(present))
    return problems


def validate_topic_selection(response: Dict[str, Any]) -> List[str]:
    problems: List[str] = []
    cards = response.get("topic_cards")
    if response.get("all_topics_read") is not True:
        problems.append("all_topics_read must be true before comparing topics")
    if not isinstance(cards, list) or len(cards) < 2:
        problems.append("full topic inventory is missing")
    else:
        required = {"topic_id", "observed_evidence", "fit", "risks", "unknowns", "workload"}
        for index, card in enumerate(cards):
            if not isinstance(card, dict) or not required.issubset(card):
                problems.append(f"topic card {index} lacks evidence/risk/unknown fields")
    decision = response.get("selection_decision")
    if not isinstance(decision, dict) or decision.get("status") not in {"pending", "needs_human"}:
        problems.append("topic selection must remain a human decision")
    forbidden = {"recommendation", "winner", "total_score", "overall_score", "auto_selected"}
    present = sorted(forbidden & set(deep_keys(response)))
    if present:
        problems.append("topic selection contains automatic-choice fields: " + ", ".join(present))
    return problems


def validate_familiarization(response: Dict[str, Any]) -> List[str]:
    problems: List[str] = []
    if response.get("status") not in {"partial", "needs_human"}:
        problems.append("familiarization must not be marked complete before understanding confirmation")
    if response.get("understanding_status") not in {"partial", "needs_human"}:
        problems.append("understanding status must expose unresolved understanding")
    if response.get("model_selection_started") is not False:
        problems.append("model selection must not start during incomplete familiarization")
    rounds = response.get("rounds")
    if not isinstance(rounds, list) or len(rounds) < 2:
        problems.append("at least two rounds of team restatement are required")
    else:
        for index, round_record in enumerate(rounds):
            required = {"round_id", "team_restatement", "differences", "corrections", "open_questions"}
            if not isinstance(round_record, dict) or not required.issubset(round_record):
                problems.append(f"familiarization round {index} lacks continuation fields")
    boundary = response.get("source_boundary")
    if not isinstance(boundary, dict) or not boundary:
        problems.append("source boundary and unread materials must be explicit")
    return problems


def validate_finding_deduplication(response: Dict[str, Any]) -> List[str]:
    problems: List[str] = []
    records = response.get("finding_records")
    canonicals = response.get("canonical_findings")
    if not isinstance(records, list) or len(records) < 2:
        problems.append("multiple source findings are required for this scenario")
    if not isinstance(canonicals, list) or len(canonicals) != 1:
        problems.append("the common issue must have exactly one canonical finding")
    if response.get("open_record_count") != 1:
        problems.append("duplicate open finding count must collapse to one")
    if isinstance(records, list):
        keys = {record.get("canonical_issue_key") for record in records if isinstance(record, dict)}
        if len(keys) != 1:
            problems.append("source records do not identify the same canonical issue")
        if any(record.get("relation") not in {"new", "supplement", "upgrade", "downgrade", "conflict", "duplicate"} for record in records if isinstance(record, dict)):
            problems.append("source finding relation is invalid")
    if isinstance(canonicals, list) and canonicals:
        canonical = canonicals[0]
        if canonical.get("status") not in {"open", "needs_human", "confirmed"}:
            problems.append("canonical finding has an invalid closure state")
        if len(canonical.get("source_record_ids", [])) < 2 or len(canonical.get("source_skills", [])) < 2:
            problems.append("canonical finding must preserve source records and skills")
        if not canonical.get("evidence_anchor_ids"):
            problems.append("canonical finding must preserve evidence anchors")
    return problems


VALIDATORS = {
    "model_choice": validate_model_choice,
    "topic_selection": validate_topic_selection,
    "familiarization": validate_familiarization,
    "finding_deduplication": validate_finding_deduplication,
}


def validate(case: Dict[str, Any], response: Dict[str, Any]) -> List[str]:
    if not isinstance(response, dict):
        return ["response must be a JSON object"]
    problems = common_checks(case, response)
    validator = VALIDATORS[case["behavior"]]
    problems.extend(validator(response))
    return problems


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--response", type=Path, help="one response JSON")
    group.add_argument("--responses-dir", type=Path, help="directory containing <case_id>.json for all cases")
    parser.add_argument("--case", help="case ID when --response is used")
    return parser.parse_args()


def load_response(path: Path) -> Dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("response must be a JSON object")
    return payload


def main() -> int:
    args = parse_args()
    cases = load_cases()
    if args.response:
        if not args.case or args.case not in cases:
            print("ERROR: --case must name a case in cases.json", file=sys.stderr)
            return 2
        targets = [(cases[args.case], args.response)]
    else:
        targets = []
        missing = []
        for case_id, case in cases.items():
            path = args.responses_dir / f"{case_id}.json"
            if not path.exists():
                missing.append(str(path))
            else:
                targets.append((case, path))
        if missing:
            print("MISSING RESPONSES:", file=sys.stderr)
            for path in missing:
                print(f"- {path}", file=sys.stderr)
            return 3

    failed = False
    for case, path in targets:
        try:
            problems = validate(case, load_response(path))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            problems = [str(exc)]
        if problems:
            failed = True
            print(f"FAIL {case['case_id']}")
            for problem in problems:
                print(f"- {problem}")
        else:
            print(f"PASS {case['case_id']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
