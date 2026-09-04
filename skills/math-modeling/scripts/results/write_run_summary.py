#!/usr/bin/env python3
"""Write or validate a lightweight run_summary.json. Do not emit a full experiment report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

ALLOWED_STATUS = {"ok", "failed", "unknown"}
FORBIDDEN_KEYS = {"overall_score", "award_probability", "experiment_report"}


def validate_summary(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not payload.get("run_id"):
        errors.append("missing run_id")
    status = payload.get("status")
    if status not in ALLOWED_STATUS:
        errors.append("status must be ok|failed|unknown")
    if not payload.get("outputs") and not payload.get("artifacts"):
        errors.append("need outputs or artifacts")
    for key in FORBIDDEN_KEYS:
        if key in payload:
            errors.append(f"forbidden field: {key}")
    return errors


def capture_environment(repo_root: Path | None = None) -> dict[str, Any]:
    env: dict[str, Any] = {
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python": sys.version.split()[0],
        "implementation": sys.implementation.name,
        "os": platform.platform(),
        "executable": sys.executable,
    }
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root or Path.cwd(),
            check=False,
            capture_output=True,
            text=True,
            timeout=3,
        )
        env["git_revision"] = result.stdout.strip() if result.returncode == 0 else "unknown"
    except (OSError, subprocess.SubprocessError):
        env["git_revision"] = "unknown"
    return env


def build_summary(args: argparse.Namespace) -> dict[str, Any]:
    outputs: dict[str, Any] = {}
    if args.output_json:
        parsed = json.loads(args.output_json)
        if not isinstance(parsed, dict):
            raise ValueError("--output-json must be an object")
        outputs = parsed
    artifacts = [item.strip() for item in (args.artifact or []) if item.strip()]
    summary = {
        "run_id": args.run_id,
        "model_id": args.model_id or "",
        "input_hash": args.input_hash or "",
        "parameters": json.loads(args.parameters) if args.parameters else {},
        "seed": args.seed,
        "environment": capture_environment(),
        "outputs": outputs,
        "artifacts": artifacts,
        "warnings": [item.strip() for item in (args.warning or []) if item.strip()],
        "status": args.status,
    }
    errors = validate_summary(summary)
    if errors:
        raise ValueError("; ".join(errors))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--model-id")
    parser.add_argument("--input-hash")
    parser.add_argument("--parameters")
    parser.add_argument("--seed")
    parser.add_argument("--output-json")
    parser.add_argument("--artifact", action="append")
    parser.add_argument("--warning", action="append")
    parser.add_argument("--status", choices=sorted(ALLOWED_STATUS), default="ok")
    args = parser.parse_args()
    if args.validate:
        payload = json.loads(args.validate.read_text(encoding="utf-8"))
        errors = validate_summary(payload)
        if errors:
            for item in errors:
                print(f"ERROR: {item}")
            return 1
        print("OK: run_summary is valid")
        return 0
    if not args.run_id or not args.output:
        parser.error("--run-id and --output are required unless --validate is set")
    summary = build_summary(args)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
