#!/usr/bin/env python3
"""Run one behavioral case against a host, normalize the envelope, validate, and save results.

This is a runner, not a compatibility claim. Missing hosts and missing real responses are
recorded as not_run/error and must not be counted as a pass. Only Codex is wired so far;
Claude Code and Gemini CLI remain fixture_only in the compatibility matrix.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[2]
BEHAVIORAL = Path(__file__).resolve().parent
CASES_PATH = BEHAVIORAL / "cases.json"
VALIDATE_SCRIPT = BEHAVIORAL / "validate_behavior.py"
DEFAULT_RESULT_DIR = BEHAVIORAL / "results" / "runs"


def load_cases() -> Dict[str, Dict[str, Any]]:
    payload = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    return {str(case["case_id"]): case for case in payload}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def probe_codex() -> Dict[str, Any]:
    executable = shutil.which("codex")
    probe = {
        "host": "codex",
        "executable": executable,
        "available": executable is not None,
        "model": None,
        "model_version": None,
        "version_output": None,
    }
    if not executable:
        return probe
    try:
        result = subprocess.run(
            [executable, "--version"],
            text=True,
            capture_output=True,
            check=False,
            timeout=15,
        )
        output = (result.stdout or result.stderr or "").strip()
        probe["version_output"] = output.splitlines()[0] if output else None
        probe["model_version"] = probe["version_output"]
    except (OSError, subprocess.TimeoutExpired) as exc:
        probe["available"] = False
        probe["version_output"] = str(exc)
    return probe


def extract_json_object(text: str) -> Dict[str, Any]:
    stripped = text.strip()
    if not stripped:
        raise ValueError("host output is empty")
    try:
        payload = json.loads(stripped)
        if isinstance(payload, dict):
            return payload
    except json.JSONDecodeError:
        pass
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, flags=re.DOTALL)
    candidates = fenced or re.findall(r"(\{.*\})", stripped, flags=re.DOTALL)
    last_error = "no JSON object found in host output"
    for raw in reversed(candidates):
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            last_error = str(exc)
            continue
        if isinstance(payload, dict):
            return payload
    raise ValueError(last_error)


def normalize_envelope(payload: Dict[str, Any], case: Dict[str, Any]) -> Dict[str, Any]:
    if "response" in payload and isinstance(payload["response"], dict):
        payload = payload["response"]
    envelope = dict(payload)
    envelope.setdefault("case_id", case["case_id"])
    envelope.setdefault("human_gate", "required")
    if envelope.get("case_id") != case["case_id"]:
        raise ValueError("normalized envelope case_id does not match the scenario")
    return envelope


def validate_envelope(case_id: str, envelope: Dict[str, Any], tmp_dir: Path) -> Tuple[bool, List[str]]:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    response_path = tmp_dir / f"{case_id}.json"
    response_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT), "--case", case_id, "--response", str(response_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    problems = [line[2:] for line in output.splitlines() if line.startswith("- ")]
    if result.returncode == 0:
        return True, []
    return False, problems or [output.strip() or f"validator exited {result.returncode}"]


def write_result(path: Path, record: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def result_record(case: Dict[str, Any], host: str, **fields: Any) -> Dict[str, Any]:
    record = {
        "schema_version": "0.1",
        "case_id": case["case_id"],
        "target_skill": case["target_skill"],
        "prompt": case["prompt"],
        "host": host,
        "model": None,
        "model_version": None,
        "run_at": utc_now(),
        "status": "not_run",
        "reason": "",
        "response": None,
        "validation_problems": [],
        "does_not_verify_host_compatibility": True,
    }
    record.update(fields)
    return record


def run_codex_exec(prompt: str, executable: str) -> str:
    env = os.environ.copy()
    result = subprocess.run(
        [executable, "exec", "--skip-git-repo-check", prompt],
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
        env=env,
        cwd=str(ROOT),
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip() or f"exit {result.returncode}"
        raise RuntimeError(f"codex exec failed: {detail}")
    return result.stdout or result.stderr or ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="codex", choices=["codex"], help="currently only Codex is wired")
    parser.add_argument("--case", help="one case_id from cases.json")
    parser.add_argument("--all", action="store_true", help="run every case in cases.json")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULT_DIR)
    parser.add_argument(
        "--from-response",
        type=Path,
        help="normalize and validate an existing host/fixture response instead of invoking the host",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="actually invoke the host CLI; without this flag the runner records not_run",
    )
    return parser.parse_args()


def selected_cases(args: argparse.Namespace, cases: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    if args.case:
        if args.case not in cases:
            raise SystemExit(f"ERROR: unknown case {args.case}")
        return [cases[args.case]]
    if args.all:
        return list(cases.values())
    raise SystemExit("ERROR: provide --case or --all")


def main() -> int:
    args = parse_args()
    cases = load_cases()
    targets = selected_cases(args, cases)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    worst = 0
    for case in targets:
        output_path = args.output_dir / f"{args.host}-{case['case_id']}.json"
        if args.from_response:
            try:
                raw = json.loads(args.from_response.read_text(encoding="utf-8"))
                if not isinstance(raw, dict):
                    raise ValueError("response must be a JSON object")
                envelope = normalize_envelope(raw, case)
                ok, problems = validate_envelope(case["case_id"], envelope, args.output_dir / "_tmp")
                record = result_record(
                    case,
                    args.host,
                    status="pass" if ok else "fail",
                    reason="validated existing response" if ok else "validator rejected response",
                    response=envelope,
                    validation_problems=problems,
                    model=raw.get("model"),
                    model_version=raw.get("model_version"),
                )
                write_result(output_path, record)
                print(f"{record['status'].upper()} {case['case_id']}")
                worst = max(worst, 0 if ok else 1)
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                record = result_record(case, args.host, status="error", reason=str(exc))
                write_result(output_path, record)
                print(f"ERROR {case['case_id']}: {exc}", file=sys.stderr)
                worst = max(worst, 2)
            continue

        probe = probe_codex() if args.host == "codex" else {"available": False}
        if not args.execute:
            record = result_record(
                case,
                args.host,
                status="not_run",
                reason="host not invoked; pass --execute after a real Codex CLI is available",
                model_version=probe.get("model_version"),
            )
            write_result(output_path, record)
            print(f"NOT_RUN {case['case_id']}")
            worst = max(worst, 3)
            continue
        if not probe.get("available"):
            record = result_record(
                case,
                args.host,
                status="not_run",
                reason="codex CLI was not found on PATH",
            )
            write_result(output_path, record)
            print(f"NOT_RUN {case['case_id']}: codex CLI missing")
            worst = max(worst, 3)
            continue
        prompt = (
            "Follow the target skill and return one JSON object that satisfies the "
            "MathModelingSkills behavioral envelope. Do not invent human confirmation.\n\n"
            f"Target skill: {case['target_skill']}\n"
            f"Case ID: {case['case_id']}\n"
            f"Task: {case['prompt']}\n"
        )
        try:
            raw_text = run_codex_exec(prompt, probe["executable"])
            envelope = normalize_envelope(extract_json_object(raw_text), case)
            ok, problems = validate_envelope(case["case_id"], envelope, args.output_dir / "_tmp")
            record = result_record(
                case,
                args.host,
                status="pass" if ok else "fail",
                reason="codex exec validated" if ok else "codex exec rejected by validator",
                response=envelope,
                validation_problems=problems,
                model="codex",
                model_version=probe.get("model_version"),
            )
            write_result(output_path, record)
            print(f"{record['status'].upper()} {case['case_id']}")
            worst = max(worst, 0 if ok else 1)
        except Exception as exc:  # noqa: BLE001 - host failures must be recorded, not hidden
            record = result_record(
                case,
                args.host,
                status="error",
                reason=str(exc),
                model_version=probe.get("model_version"),
            )
            write_result(output_path, record)
            print(f"ERROR {case['case_id']}: {exc}", file=sys.stderr)
            worst = max(worst, 2)
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
