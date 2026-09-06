#!/usr/bin/env python3
"""Resolve contest problem identity vs submission rules. Never copy problem year
onto rules year.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RULES = ROOT / "references" / "rules" / "cumcm-2026.yaml"
DEFAULT_WRITING = ROOT / "profiles" / "writing" / "cumcm-natural-cn.yaml"


def resolve_submission_context(
    *,
    problem_competition: Optional[str] = None,
    problem_year: Optional[str] = None,
    problem_code: Optional[str] = None,
    rules_year: Optional[str] = None,
    rules_profile_id: Optional[str] = None,
    writing_profile_id: Optional[str] = None,
    infer_rules_from_problem: bool = False,
) -> dict[str, Any]:
    """Return a submission context. Guessing rules_year from problem_year is forbidden."""
    errors: list[str] = []
    if infer_rules_from_problem:
        errors.append("rules_year_must_not_be_inferred_from_problem_year")
    if rules_year is None and problem_year is not None and not rules_profile_id:
        errors.append("rules_year_missing; do not copy problem_year")
    if rules_year is not None and problem_year is not None and str(rules_year) == str(problem_year):
        # Same year can be valid, but only when explicitly supplied.
        pass
    if rules_profile_id is None or rules_year is None:
        status = "unassessed"
        if not errors:
            errors.append("rules_profile_unresolved")
    else:
        status = "resolved"
    if errors and status == "resolved":
        status = "conflict"
    return {
        "schema_version": "0.3.2",
        "problem": {
            "competition": problem_competition,
            "year": problem_year,
            "problem": problem_code,
        },
        "submission": {
            "competition": problem_competition,
            "rules_year": rules_year,
            "rules_profile_id": rules_profile_id,
            "writing_profile_id": writing_profile_id,
        },
        "status": status,
        "errors": errors,
        "compliance_status": "unassessed" if status != "resolved" else "pending_checks",
        "note": (
            "problem.year identifies the contest statement. "
            "submission.rules_year identifies the rules used to write the paper. "
            "A 2025 problem may be written under cumcm-2026."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--problem-competition")
    parser.add_argument("--problem-year")
    parser.add_argument("--problem-code")
    parser.add_argument("--rules-year")
    parser.add_argument("--rules-profile-id")
    parser.add_argument("--writing-profile-id")
    parser.add_argument(
        "--infer-rules-from-problem",
        action="store_true",
        help="Illegal flag used only to prove the resolver rejects year copying",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = resolve_submission_context(
        problem_competition=args.problem_competition,
        problem_year=args.problem_year,
        problem_code=args.problem_code,
        rules_year=args.rules_year,
        rules_profile_id=args.rules_profile_id,
        writing_profile_id=args.writing_profile_id,
        infer_rules_from_problem=args.infer_rules_from_problem,
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if payload["status"] != "resolved":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
