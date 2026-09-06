#!/usr/bin/env python3
"""Compliance claims require a resolved, non-draft rules profile and executed
checks. Caller booleans are not evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


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
READY_PROFILE_STATUSES = {"verified", "active", "confirmed"}
READY_HUMAN_STATUSES = {"confirmed", "signed", "complete", "approved"}


def _load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to read a rules profile")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a mapping")
    return payload


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object")
    return payload


def inspect_rules_profile(profile: dict[str, Any]) -> dict[str, Any]:
    human = profile.get("human_confirmation") or {}
    sources = profile.get("sources") or []
    official = [
        source
        for source in sources
        if isinstance(source, dict)
        and source.get("authority") == "official_organizing_committee"
    ]
    status = str(profile.get("status") or "unknown")
    human_required = bool(human.get("required"))
    human_status = str(human.get("status") or "unknown")
    return {
        "profile_id": profile.get("profile_id"),
        "rules_year": (profile.get("competition") or {}).get("year"),
        "profile_status": status,
        "profile_ready": status in READY_PROFILE_STATUSES,
        "human_confirmation_required": human_required,
        "human_confirmation_status": human_status,
        "human_ready": (not human_required) or human_status in READY_HUMAN_STATUSES,
        "official_source_count": len(official),
        "official_sources_present": bool(official),
    }


def inspect_preflight(report: Optional[dict[str, Any]]) -> dict[str, Any]:
    if not report:
        return {
            "present": False,
            "checks_run": [],
            "required_unassessed": ["preflight_report_missing"],
        }
    checks = report.get("checks_run") or report.get("checks") or []
    if isinstance(checks, dict):
        checks = list(checks.keys())
    unassessed = list(report.get("required_unassessed") or [])
    return {
        "present": True,
        "checks_run": list(checks),
        "required_unassessed": unassessed,
    }


def inspect_submission_context(context: Optional[dict[str, Any]]) -> dict[str, Any]:
    if not context:
        return {"present": False, "status": None}
    submission = context.get("submission") or {}
    return {
        "present": True,
        "status": context.get("status"),
        "rules_profile_id": submission.get("rules_profile_id"),
        "rules_year": submission.get("rules_year"),
    }


def _illegal_claim(status: str, claimed_status: Optional[str]) -> bool:
    claim = (claimed_status or "").strip()
    if status == "passed" or not claim:
        return False
    lowered = claim.lower()
    return any(token.lower() in lowered for token in FORBIDDEN_WHEN_UNASSESSED) or (
        claim in FORBIDDEN_WHEN_UNASSESSED
    )


def assess_compliance(
    *,
    rules_profile: Optional[dict[str, Any]] = None,
    preflight_report: Optional[dict[str, Any]] = None,
    submission_context: Optional[dict[str, Any]] = None,
    claimed_status: Optional[str] = None,
    rules_profile_id: Optional[str] = None,
    rules_year: Optional[str] = None,
    official_source_verified: bool = False,
    required_checks_executed: bool = False,
    required_unassessed: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Evaluate compliance from artifacts. Caller booleans never produce passed."""
    profile_facts = inspect_rules_profile(rules_profile) if rules_profile else None
    preflight_facts = inspect_preflight(preflight_report)
    context_facts = inspect_submission_context(submission_context)
    caller_id = (profile_facts or {}).get("profile_id") or rules_profile_id
    caller_year = (profile_facts or {}).get("rules_year") or rules_year
    if caller_year is not None:
        caller_year = str(caller_year)

    reasons: list[str] = []
    if profile_facts is None:
        reasons.append("rules_profile_unresolved")
    else:
        if not profile_facts["profile_ready"]:
            reasons.append(f"profile_status_{profile_facts['profile_status']}")
        if not profile_facts["human_ready"]:
            reasons.append("human_confirmation_pending")
        if not profile_facts["official_sources_present"]:
            reasons.append("official_source_missing")
    if context_facts["present"] and context_facts.get("status") not in {None, "resolved"}:
        reasons.append("submission_context_unresolved")
    if not preflight_facts["present"] or not preflight_facts["checks_run"] or preflight_facts["required_unassessed"]:
        reasons.append("required_checks_incomplete")
    if official_source_verified or required_checks_executed or required_unassessed is not None:
        # Keep the fields visible, but they cannot clear a failed artifact check.
        pass
    if not reasons:
        status = "passed"
        reason = "resolved"
    else:
        status = "unassessed"
        reason = reasons[0]
    claim = (claimed_status or "").strip()
    return {
        "compliance_status": status,
        "reason": reason,
        "reasons": reasons,
        "rules_profile_id": caller_id,
        "rules_year": caller_year,
        "profile": profile_facts,
        "preflight": preflight_facts,
        "submission_context": context_facts,
        "caller_assertions_ignored": bool(
            official_source_verified or required_checks_executed
        ),
        "illegal_compliance_claim": _illegal_claim(status, claim),
        "claimed_status": claim or None,
        "allowed_labels": ["unassessed"] if status != "passed" else ["passed"],
        "note": (
            "Drafting and compiling are allowed without a profile. "
            "Saying compliant, ready, or submission-ready is not. "
            "Caller booleans are not evidence; the gate reads the profile and preflight."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules-profile", type=Path, help="rules profile YAML to inspect")
    parser.add_argument("--preflight-report", type=Path, help="preflight JSON report")
    parser.add_argument("--submission-context", type=Path, help="submission context JSON")
    parser.add_argument("--rules-profile-id", help="ignored unless no --rules-profile is given")
    parser.add_argument("--rules-year")
    parser.add_argument(
        "--official-source-verified",
        action="store_true",
        help="deprecated; cannot produce passed",
    )
    parser.add_argument(
        "--required-checks-executed",
        action="store_true",
        help="deprecated; cannot produce passed",
    )
    parser.add_argument("--required-unassessed", action="append", default=None)
    parser.add_argument("--claimed-status")
    args = parser.parse_args()
    profile = _load_yaml(args.rules_profile) if args.rules_profile else None
    preflight = _load_json(args.preflight_report) if args.preflight_report else None
    context = _load_json(args.submission_context) if args.submission_context else None
    payload = assess_compliance(
        rules_profile=profile,
        preflight_report=preflight,
        submission_context=context,
        claimed_status=args.claimed_status,
        rules_profile_id=args.rules_profile_id,
        rules_year=args.rules_year,
        official_source_verified=args.official_source_verified,
        required_checks_executed=args.required_checks_executed,
        required_unassessed=args.required_unassessed,
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
