#!/usr/bin/env python3
"""Validate a cheap feasibility probe record. This is not a model score."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ALLOWED_VERDICTS = {"feasible_to_try", "not_now", "unknown"}
ALLOWED_RESULTS = {"pass", "fail", "unknown"}
FORBIDDEN = {"overall_score", "award_probability", "total_score", "rank"}


def validate_probe(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not payload.get("candidate_id"):
        errors.append("missing candidate_id")
    if payload.get("verdict") not in ALLOWED_VERDICTS:
        errors.append("verdict must be feasible_to_try|not_now|unknown")
    for key in FORBIDDEN:
        if key in payload:
            errors.append(f"forbidden scoring field: {key}")
    checks = payload.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty list")
    else:
        for index, check in enumerate(checks):
            if not isinstance(check, dict) or not check.get("name"):
                errors.append(f"checks[{index}] needs a name")
                continue
            if check.get("result") not in ALLOWED_RESULTS:
                errors.append(f"{check['name']}: result must be pass|fail|unknown")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.probe.read_text(encoding="utf-8"))
    errors = validate_probe(payload)
    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    print("OK: feasibility probe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
