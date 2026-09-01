#!/usr/bin/env python3
"""Compute a conservative next-step plan from a structured pipeline state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from pipeline_runtime import (
    ACTION_LEVELS,
    COLLABORATION_MODES,
    USER_INTENTS,
    WORKING_DEPTHS,
    PROFILE_ALIASES,
    build_effective_stage_policy,
    normalize_profile_id,
    plan_markdown,
    ready_stages,
    validate_state,
)


def read_state(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("state must be an object")
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="structured state JSON")
    parser.add_argument("--output", required=True, type=Path, help="Markdown plan output")
    parser.add_argument(
        "--profile",
        help="optional run-profile override for this plan; it does not modify the input state",
    )
    parser.add_argument(
        "--policy-json",
        type=Path,
        help="optional JSON file for the computed effective_stage_policy",
    )
    parser.add_argument(
        "--intent",
        choices=sorted(USER_INTENTS),
        help="optional user goal override; it only changes routing priority",
    )
    parser.add_argument(
        "--requested-stage",
        help="optional explicit stage requested by the user",
    )
    parser.add_argument(
        "--collaboration-mode",
        choices=sorted(COLLABORATION_MODES),
        help="optional alias of working depth; adaptive uses the profile default",
    )
    parser.add_argument(
        "--working-depth",
        choices=sorted(WORKING_DEPTHS),
        help="optional working depth: light, standard, or full",
    )
    parser.add_argument(
        "--action",
        choices=sorted(ACTION_LEVELS),
        help="optional action level: explain/explore/propose may proceed provisionally; adopt/freeze/submit require adoption_requires",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        state = read_state(args.input)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: cannot read state: {exc}", file=sys.stderr)
        return 2
    if args.profile:
        state = dict(state)
        state["run_profile"] = PROFILE_ALIASES.get(args.profile, args.profile)
        if normalize_profile_id(state["run_profile"]) is None:
            print("FAIL", file=sys.stderr)
            print(f"- unknown run profile: {state['run_profile']}", file=sys.stderr)
            return 1
    if args.intent or args.requested_stage or args.action:
        state = dict(state)
        intent = dict(state.get("user_intent") or {})
        if args.intent:
            intent["goal"] = args.intent
        if args.requested_stage:
            intent["requested_stage"] = args.requested_stage
        if args.action:
            intent["action"] = args.action
        intent.setdefault("goal", "unknown")
        state["user_intent"] = intent
    if args.working_depth or args.collaboration_mode:
        state = dict(state)
        if args.working_depth:
            state["working_depth"] = args.working_depth
            state["collaboration_mode"] = args.working_depth
        elif args.collaboration_mode:
            state["collaboration_mode"] = args.collaboration_mode
    errors = validate_state(state)
    if errors:
        print("FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    policy = build_effective_stage_policy(state)
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(plan_markdown(state, policy=policy), encoding="utf-8")
        if args.policy_json:
            args.policy_json.parent.mkdir(parents=True, exist_ok=True)
            serializable = dict(policy)
            serializable["stages"] = dict(policy["stages"])
            args.policy_json.write_text(
                json.dumps(serializable, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    except OSError as exc:
        print(f"ERROR: cannot write plan: {exc}", file=sys.stderr)
        return 2
    print(f"WROTE: {args.output}")
    print(f"READY: {', '.join(ready_stages(state, policy=policy)) or 'none'}")
    print(f"PROFILE: {policy['profile_id']}")
    print(f"LENSES: {', '.join(policy['selected_lenses']) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
