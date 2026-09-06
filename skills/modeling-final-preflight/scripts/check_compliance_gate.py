#!/usr/bin/env python3
"""Compliance claims require a resolved rules profile. Missing profile is
unassessed, never passed.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Optional, Sequence


FORBIDDEN_WHEN_UNASSESSED = (
    "compliant",
    "compliance_passed",
    "ready",
    "submission-ready",
    "ready_for_human_submission",
    "格式合规",
    "提交稿",
    "符合赛事格式",
)


def assess_compliance(
    *,
    rules_profile_id: Optional[str] = None,
    rules_year: Optional[str] = None,
    official_source_verified: bool = False,
    required_checks_executed: bool = False,
    required_unassessed: Optional[Sequence[str]] = None,
    claimed_status: Optional[str] = None,
) -> dict[str, Any]:
    unresolved = not rules_profile_id or not rules_year
    required_unassessed = list(required_unassessed or [])
    if unresolved:
        status = "unassessed"
        reason = "rules_profile_unresolved"
    elif not official_source_verified:
        status = "unassessed"
        reason = "official_source_unverified"
    elif not required_checks_executed or required_unassessed:
        status = "unassessed"
        reason = "required_checks_incomplete"
    else:
        status = "passed"
        reason = "resolved"
    claim = (claimed_status or "").strip()
    illegal_claim = False
    if status != "passed" and claim:
        lowered = claim.lower()
        illegal_claim = any(token.lower() in lowered for token in FORBIDDEN_WHEN_UNASSESSED)
        if claim in FORBIDDEN_WHEN_UNASSESSED:
            illegal_claim = True
    return {
        "compliance_status": status,
        "reason": reason,
        "rules_profile_id": rules_profile_id,
        "rules_year": rules_year,
        "illegal_compliance_claim": illegal_claim,
        "claimed_status": claim or None,
        "allowed_labels": ["unassessed"] if status != "passed" else ["passed"],
        "note": (
            "Drafting and compiling are allowed without a profile. "
            "Saying compliant, ready, or submission-ready is not."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules-profile-id")
    parser.add_argument("--rules-year")
    parser.add_argument("--official-source-verified", action="store_true")
    parser.add_argument("--required-checks-executed", action="store_true")
    parser.add_argument("--required-unassessed", action="append", default=[])
    parser.add_argument("--claimed-status")
    args = parser.parse_args()
    payload = assess_compliance(
        rules_profile_id=args.rules_profile_id,
        rules_year=args.rules_year,
        official_source_verified=args.official_source_verified,
        required_checks_executed=args.required_checks_executed,
        required_unassessed=args.required_unassessed,
        claimed_status=args.claimed_status,
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if payload["illegal_compliance_claim"]:
        return 1
    if payload["compliance_status"] != "passed":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
