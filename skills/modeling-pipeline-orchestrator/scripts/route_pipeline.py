#!/usr/bin/env python3
"""Compute a conservative next-step plan from a structured pipeline state."""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Tuple


STAGE_GRAPH = OrderedDict(
    [
        ("rules_profile", ("modeling-rules-profile", [], "required")),
        ("problem_intake", ("modeling-problem-intake", ["rules_profile"], "required")),
        ("assumption_ledger", ("modeling-assumption-ledger", ["problem_intake"], "required")),
        ("literature_evidence", ("modeling-literature-evidence", ["problem_intake"], "required")),
        ("data_audit", ("modeling-data-audit", ["problem_intake"], "required")),
        ("model_architect", ("modeling-model-architect", ["problem_intake", "assumption_ledger", "data_audit"], "required")),
        ("experiment_validator", ("modeling-experiment-validator", ["model_architect"], "required")),
        ("paper_architect", ("modeling-paper-architect", ["problem_intake", "model_architect", "experiment_validator"], "required")),
        ("figure_design", ("modeling-figure-designer", ["paper_architect", "experiment_validator"], "required")),
        ("figure_table", ("modeling-figure-table-auditor", ["experiment_validator", "figure_design"], "required")),
        ("claim_evidence", ("modeling-claim-evidence-audit", ["paper_architect", "experiment_validator"], "required")),
        ("terminology", ("modeling-terminology-auditor", ["paper_architect"], "required")),
        ("draft", ("author/agent writing", ["paper_architect", "figure_design", "claim_evidence", "terminology"], "required")),
        ("paper_review", ("modeling-paper-reviewer", ["draft"], "required")),
        ("ai_pattern", ("modeling-ai-pattern-reviewer", ["draft"], "required")),
        ("anti_homogenization", ("modeling-anti-homogenization-auditor", ["draft"], "required")),
        ("reader", ("modeling-reader-experience-auditor", ["draft"], "required")),
        ("naturalizer", ("modeling-paper-naturalizer", ["paper_review", "ai_pattern", "reader"], "required")),
        ("support", ("modeling-support-materials-auditor", ["draft", "figure_table"], "required")),
        ("ai_disclosure", ("modeling-ai-use-disclosure", ["rules_profile"], "required")),
        ("final_preflight", ("modeling-final-preflight", ["naturalizer", "support", "ai_disclosure"], "required")),
        ("process_freezer", ("modeling-process-freezer", ["final_preflight"], "required")),
    ]
)
STATUSES = {
    "not_started",
    "ready",
    "in_progress",
    "needs_human",
    "passed",
    "blocked",
    "stale",
    "skipped",
    "superseded",
}
SATISFIED = {"passed", "skipped"}


def read_state(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("state must be an object")
    return data


def stage_record(state: Dict[str, Any], stage: str) -> Dict[str, Any]:
    record = state.get("stages", {}).get(stage, {})
    return record if isinstance(record, dict) else {}


def validate_state(state: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not isinstance(state.get("stages"), dict):
        return ["stages must be an object"]
    for stage, record in state["stages"].items():
        if stage not in STAGE_GRAPH:
            errors.append(f"unknown stage: {stage}")
            continue
        if not isinstance(record, dict):
            errors.append(f"stage {stage} must be an object")
            continue
        if record.get("status", "not_started") not in STATUSES:
            errors.append(f"stage {stage} has invalid status")
        if record.get("status") == "skipped" and not record.get("reason"):
            errors.append(f"skipped stage {stage} needs a reason")
    return errors


def dependency_state(state: Dict[str, Any], dependency: str) -> str:
    return stage_record(state, dependency).get("status", "not_started")


def ready_stages(state: Dict[str, Any]) -> List[str]:
    result = []
    for stage, (_, dependencies, _) in STAGE_GRAPH.items():
        status = stage_record(state, stage).get("status", "not_started")
        if status not in {"not_started", "ready", "stale"}:
            continue
        if all(dependency_state(state, dep) in SATISFIED for dep in dependencies):
            result.append(stage)
    return result


def plan_markdown(state: Dict[str, Any]) -> str:
    lines = [
        "# Pipeline run plan",
        "",
        f"Mode: {state.get('mode', 'unknown')}",
        f"Entry: {state.get('entry_status', 'unknown')}",
        f"Current stage: {state.get('current_stage', 'unknown')}",
        f"Snapshot: {state.get('last_snapshot_id', 'unknown')}",
        "",
        "This is a routing proposal. It does not confirm mathematical correctness, human decisions, or submission readiness.",
        "",
        "## Stage status",
        "",
        "| stage | skill | status | dependencies | human gate |",
        "|---|---|---|---|---|",
    ]
    for stage, (skill, dependencies, gate) in STAGE_GRAPH.items():
        status = stage_record(state, stage).get("status", "not_started")
        lines.append(f"| {stage} | {skill} | {status} | {', '.join(dependencies) or '-'} | {gate} |")

    ready = ready_stages(state)
    lines.extend(["", "## Ready next", ""])
    if ready:
        lines.extend(f"- Run {stage} through {STAGE_GRAPH[stage][0]}; verify its inputs and write its output artifact." for stage in ready)
    else:
        lines.append("- No stage is ready. Inspect human gates, blocked dependencies, stale snapshots, or incomplete state.")

    needs_human = [
        stage for stage in STAGE_GRAPH
        if stage_record(state, stage).get("status") == "needs_human"
    ]
    blocked = [
        stage for stage in STAGE_GRAPH
        if stage_record(state, stage).get("status") in {"blocked", "stale", "superseded"}
    ]
    lines.extend(["", "## Human gates", ""])
    if needs_human:
        lines.extend(f"- {stage}: {stage_record(state, stage).get('reason', 'record the decision and scope')}" for stage in needs_human)
    else:
        lines.append("- No explicit needs_human stage is recorded; this does not mean human gates are complete.")
    lines.extend(["", "## Blocked or recheck", ""])
    if blocked:
        lines.extend(f"- {stage}: {stage_record(state, stage).get('reason', 'inspect its issue and upstream evidence')}" for stage in blocked)
    else:
        lines.append("- None recorded.")
    if ready:
        safe_action = (
            "Open the ready stage's input artifacts, check the latest process-freezer manifest, "
            "then run only that stage."
        )
    elif needs_human:
        safe_action = "Resolve the listed human gates and record decision IDs before rerunning downstream stages."
    elif blocked:
        safe_action = "Inspect the listed blocked or stale stages and their upstream evidence before rerunning anything."
    else:
        safe_action = "Inspect the incomplete state and latest process-freezer manifest before selecting the next stage."
    lines.extend(
        [
            "",
            "## Safe next action",
            "",
            safe_action + " Do not alter a core model, assumption, result, conclusion, or disclosure record without a human decision event.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="structured state JSON")
    parser.add_argument("--output", required=True, type=Path, help="Markdown plan output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        state = read_state(args.input)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: cannot read state: {exc}", file=sys.stderr)
        return 2
    errors = validate_state(state)
    if errors:
        print("FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(plan_markdown(state), encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot write plan: {exc}", file=sys.stderr)
        return 2
    print(f"WROTE: {args.output}")
    print(f"READY: {', '.join(ready_stages(state)) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
