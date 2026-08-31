#!/usr/bin/env python3
"""Canonical registry + run profile runtime: validate state and compute an effective plan."""

from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = ROOT / "schemas" / "stage-registry.json"
STATE_SCHEMA_PATH = ROOT / "schemas" / "pipeline-state.schema.json"
PROFILE_SCHEMA_PATH = ROOT / "schemas" / "run-profile.schema.json"
PROFILE_PATHS = {
    "research-full": "profiles/research-full.yaml",
    "contest-standard": "profiles/contest-standard.yaml",
    "contest-fast": "profiles/contest-fast.yaml",
}
PROFILE_ALIASES = {
    "research/full": "research-full",
    "contest/standard": "contest-standard",
    "contest/fast": "contest-fast",
}
DEFAULT_PROFILE = "research-full"
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
POLICY_SATISFIED = {"skipped-with-policy", "not_selected"}
CONFIRMED_MARKERS = {"human-confirmed", "confirmed"}
TERMINAL_FINDING_STATUS = {"resolved", "rejected", "superseded"}
OPEN_FINDING_STATUS = {"open", "needs_human", "confirmed", "unknown"}
TERMINAL_HUMAN_STATUS = {"human-confirmed", "rejected"}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry(path: Path = REGISTRY_PATH) -> Dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("stage registry must be an object")
    order = payload.get("default_order")
    stages = payload.get("stages")
    lenses = payload.get("review_lenses")
    if not isinstance(order, list) or not isinstance(stages, dict):
        raise ValueError("stage registry needs default_order and stages")
    if set(order) != set(stages):
        raise ValueError("stage registry order and stage keys must match")
    if not isinstance(lenses, dict) or not lenses:
        raise ValueError("stage registry needs review_lenses")
    positions = {stage: index for index, stage in enumerate(order)}
    for stage in order:
        record = stages[stage]
        if not isinstance(record, dict):
            raise ValueError(f"stage {stage} must be an object")
        dependencies = record.get("depends_on")
        if not isinstance(dependencies, list) or any(dep not in stages for dep in dependencies):
            raise ValueError(f"stage {stage} has an unknown dependency")
        if any(positions[dep] >= positions[stage] for dep in dependencies):
            raise ValueError(f"stage {stage} is not topologically ordered")
        gate_type = record.get("gate_type")
        if gate_type not in {"core_decision", "review_checkpoint", "none"}:
            raise ValueError(f"stage {stage} needs a gate_type")
        if gate_type == "core_decision" and record.get("human_gate") != "required":
            raise ValueError(f"core decision stage {stage} cannot drop human_gate=required")
    for lens_name, spec in lenses.items():
        if not isinstance(spec, dict) or spec.get("stage") not in stages:
            raise ValueError(f"review lens {lens_name} must map to a registry stage")
        if spec.get("timing") not in {"pre_draft", "post_draft"}:
            raise ValueError(f"review lens {lens_name} has invalid timing")
    return payload


def load_stage_graph(path: Path = REGISTRY_PATH) -> "OrderedDict[str, Dict[str, Any]]":
    registry = load_registry(path)
    graph: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    for stage in registry["default_order"]:
        record = registry["stages"][stage]
        graph[stage] = {
            "skill": record.get("skill"),
            "depends_on": list(record.get("depends_on") or []),
            "human_gate": record.get("human_gate"),
            "gate_type": record.get("gate_type"),
            "phase": record.get("phase"),
            "notes": record.get("notes", ""),
        }
    return graph


def normalize_profile_id(value: Any) -> Optional[str]:
    if value is None:
        return None
    name = PROFILE_ALIASES.get(str(value), str(value))
    return name if name in PROFILE_PATHS else None


def load_run_profile(profile_id: Optional[str] = None, *, root: Path = ROOT) -> Dict[str, Any]:
    normalized = normalize_profile_id(profile_id) or DEFAULT_PROFILE
    path = root / PROFILE_PATHS[normalized]
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"run profile {normalized} must be an object")
    schema = _read_json(PROFILE_SCHEMA_PATH)
    errors = [err.message for err in Draft202012Validator(schema).iter_errors(payload)]
    if errors:
        raise ValueError(f"run profile {normalized} failed schema: {errors[0]}")
    if payload.get("profile_id") != normalized:
        raise ValueError(f"run profile {path} profile_id does not match {normalized}")
    return payload


def core_decision_stages(registry: Mapping[str, Any]) -> List[str]:
    return [
        stage
        for stage in registry["default_order"]
        if registry["stages"][stage].get("gate_type") == "core_decision"
    ]


def stage_record(state: Mapping[str, Any], stage: str) -> Dict[str, Any]:
    record = state.get("stages", {}).get(stage, {})
    return record if isinstance(record, dict) else {}


def _lens_to_stage(registry: Mapping[str, Any]) -> Dict[str, str]:
    return {name: str(spec["stage"]) for name, spec in registry["review_lenses"].items()}


def _stage_to_lens(registry: Mapping[str, Any]) -> Dict[str, str]:
    return {str(spec["stage"]): name for name, spec in registry["review_lenses"].items()}


def _post_draft_lenses(registry: Mapping[str, Any]) -> List[str]:
    return [
        name
        for name, spec in registry["review_lenses"].items()
        if spec.get("timing") == "post_draft"
    ]


def _as_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def select_lenses(
    profile: Mapping[str, Any],
    registry: Mapping[str, Any],
    state: Mapping[str, Any],
) -> Tuple[List[str], List[str], List[str]]:
    """Return (selected, skipped_conditional, not_in_profile) lens names."""
    known = set(registry["review_lenses"])
    default = [lens for lens in _as_list(profile.get("review_policy", {}).get("lenses")) if lens in known]
    conditional = [lens for lens in _as_list(profile.get("review_policy", {}).get("conditional_lenses")) if lens in known]
    explicit = [lens for lens in _as_list(state.get("selected_lenses")) if lens in known]
    post_draft = set(_post_draft_lenses(registry))
    cap = profile.get("review_policy", {}).get("max_post_draft_lenses", "all")

    pool = list(dict.fromkeys(explicit or default))
    # Explicit selection may include conditional lenses; default selection does not.
    if explicit:
        pool = [lens for lens in pool if lens in set(default) | set(conditional) | set(explicit)]
    selected: List[str] = []
    selected_post = 0
    for lens in pool:
        is_post = lens in post_draft
        if is_post and cap != "all" and selected_post >= int(cap):
            continue
        selected.append(lens)
        if is_post:
            selected_post += 1

    if not explicit:
        selected = apply_selection_rule(profile, selected, post_draft, cap)

    selected_set = set(selected)
    skipped_conditional = [lens for lens in conditional if lens not in selected_set]
    not_in_profile = [
        lens for lens in known if lens not in set(default) | set(conditional) | selected_set
    ]
    return selected, skipped_conditional, not_in_profile


def apply_selection_rule(
    profile: Mapping[str, Any],
    selected: Sequence[str],
    post_draft: Iterable[str],
    cap: Any,
) -> List[str]:
    rule = str(profile.get("review_policy", {}).get("selection_rule") or "")
    post_draft_set = set(post_draft)
    if rule != "choose_one_highest_risk_substantive_lens_and_one_reader_or_compliance_lens":
        return list(selected)
    kept: List[str] = []
    post_kept: List[str] = []
    substantive = next((lens for lens in selected if lens == "substantive"), None)
    reader_or_compliance = next(
        (lens for lens in selected if lens in {"reader_experience", "ai_pattern", "anti_homogenization"}),
        None,
    )
    for lens in selected:
        if lens not in post_draft_set:
            kept.append(lens)
            continue
        if lens == substantive and "substantive" not in post_kept:
            post_kept.append(lens)
        elif lens == reader_or_compliance and lens not in post_kept:
            post_kept.append(lens)
    if cap != "all":
        post_kept = post_kept[: int(cap)]
    return kept + post_kept


def build_effective_stage_policy(
    state: Mapping[str, Any],
    *,
    registry: Optional[Mapping[str, Any]] = None,
    profile: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    registry = registry or load_registry()
    profile_id = normalize_profile_id(state.get("run_profile")) or DEFAULT_PROFILE
    profile = profile or load_run_profile(profile_id)
    selected, skipped_conditional, not_in_profile = select_lenses(profile, registry, state)
    selected_set = set(selected)
    skipped_set = set(skipped_conditional)
    absent_set = set(not_in_profile)
    stage_to_lens = _stage_to_lens(registry)
    blocking_gates = set(_as_list(profile.get("human_gates")))
    stages: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    for stage in registry["default_order"]:
        spec = registry["stages"][stage]
        gate_type = spec["gate_type"]
        lens = stage_to_lens.get(stage)
        reason = None
        if lens and lens in selected_set:
            execution = "selected"
        elif lens and lens in skipped_set:
            execution = "skipped-with-policy"
            reason = (
                f"{profile_id} left conditional lens {lens} unselected; "
                "canonical dependencies are unchanged"
            )
        elif lens and lens in absent_set:
            execution = "not_selected"
            reason = f"{profile_id} does not include lens {lens}"
        else:
            execution = "selected"
        if gate_type == "core_decision":
            blocking = True
        elif gate_type == "review_checkpoint":
            blocking = stage in blocking_gates
        else:
            blocking = False
        artifact_mode = profile.get("artifact_policy", {}).get("state")
        compact = artifact_mode not in {None, "separate_stage_artifacts"}
        stages[stage] = {
            "skill": spec["skill"],
            "depends_on": list(spec["depends_on"]),
            "gate_type": gate_type,
            "human_gate": spec["human_gate"],
            "blocking": blocking,
            "execution": execution,
            "lens": lens,
            "artifact_projection": "compact" if compact else "full",
            "reason": reason,
        }
    return {
        "profile_id": profile_id,
        "profile_path": PROFILE_PATHS[profile_id],
        "artifact_policy": profile.get("artifact_policy", {}),
        "review_policy": profile.get("review_policy", {}),
        "human_gates": list(profile.get("human_gates") or []),
        "selected_lenses": selected,
        "skipped_lenses": skipped_conditional + not_in_profile,
        "canonical_dependencies_unchanged": True,
        "stages": stages,
    }


def _format_schema_error(error: Any) -> str:
    path = ".".join(str(part) for part in error.absolute_path) or "<root>"
    return f"schema {path}: {error.message}"


def _has_confirmed_marker(value: Any) -> bool:
    if isinstance(value, str):
        return value in CONFIRMED_MARKERS
    return False


def _decision_ids(record: Mapping[str, Any]) -> List[str]:
    values: List[str] = []
    if record.get("decision_id"):
        values.append(str(record["decision_id"]))
    extra = record.get("decision_ids")
    if isinstance(extra, list):
        values.extend(str(item) for item in extra if item)
    return values


def validate_state(
    state: Mapping[str, Any],
    *,
    registry: Optional[Mapping[str, Any]] = None,
    schema: Optional[Mapping[str, Any]] = None,
) -> List[str]:
    errors: List[str] = []
    schema = schema or _read_json(STATE_SCHEMA_PATH)
    errors.extend(_format_schema_error(err) for err in Draft202012Validator(schema).iter_errors(state))
    registry = registry or load_registry()
    stages = registry["stages"]
    run_profile = state.get("run_profile")
    if run_profile is not None and normalize_profile_id(run_profile) is None:
        errors.append(f"unknown run profile: {run_profile}")
    current_stage = state.get("current_stage")
    if isinstance(current_stage, str) and current_stage not in stages:
        errors.append(f"current_stage is not in the registry: {current_stage}")
    selected = state.get("selected_lenses")
    if selected is not None:
        known_lenses = set(registry["review_lenses"])
        if not isinstance(selected, list):
            errors.append("selected_lenses must be an array")
        else:
            for lens in selected:
                if lens not in known_lenses:
                    errors.append(f"unknown review lens: {lens}")
    if not isinstance(state.get("stages"), dict):
        return errors or ["stages must be an object"]
    for stage, record in state["stages"].items():
        if stage not in stages:
            errors.append(f"unknown stage: {stage}")
            continue
        if not isinstance(record, dict):
            errors.append(f"stage {stage} must be an object")
            continue
        if record.get("status", "not_started") not in STATUSES:
            errors.append(f"stage {stage} has invalid status")
        if record.get("status") == "skipped" and not record.get("reason"):
            errors.append(f"skipped stage {stage} needs a reason")
        depends_on = record.get("depends_on")
        if depends_on is not None:
            canonical = list(stages[stage].get("depends_on") or [])
            if not isinstance(depends_on, list) or [str(item) for item in depends_on] != canonical:
                errors.append(f"stage {stage} depends_on conflicts with the registry")
        if _has_confirmed_marker(record.get("human_status")) and not _decision_ids(record):
            errors.append(f"human-confirmed stage {stage} needs a decision_id")
    for index, gate in enumerate(state.get("gates") or []):
        if not isinstance(gate, dict):
            continue
        confirmed = _has_confirmed_marker(gate.get("human_status")) or _has_confirmed_marker(gate.get("status"))
        if confirmed and not (gate.get("decision_id") or gate.get("decision_ids")):
            errors.append(f"human-confirmed gate[{index}] needs a decision_id")
    try:
        profile = load_run_profile(normalize_profile_id(run_profile) or DEFAULT_PROFILE)
        missing_core = [
            stage
            for stage in core_decision_stages(registry)
            if stage not in set(_as_list(profile.get("human_gates")))
        ]
        if missing_core:
            errors.append("run profile omits core decision gates: " + ", ".join(missing_core))
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def dependency_satisfied(state: Mapping[str, Any], policy: Mapping[str, Any], dependency: str) -> bool:
    status = stage_record(state, dependency).get("status", "not_started")
    if status in SATISFIED:
        return True
    execution = policy["stages"][dependency]["execution"]
    return execution in POLICY_SATISFIED and status in {"not_started", "ready", "skipped"}


def ready_stages(
    state: Mapping[str, Any],
    *,
    policy: Optional[Mapping[str, Any]] = None,
    registry: Optional[Mapping[str, Any]] = None,
) -> List[str]:
    registry = registry or load_registry()
    policy = policy or build_effective_stage_policy(state, registry=registry)
    result = []
    for stage in registry["default_order"]:
        execution = policy["stages"][stage]["execution"]
        if execution in POLICY_SATISFIED | {"conditional"}:
            continue
        status = stage_record(state, stage).get("status", "not_started")
        if status not in {"not_started", "ready", "stale"}:
            continue
        dependencies = registry["stages"][stage]["depends_on"]
        if all(dependency_satisfied(state, policy, dep) for dep in dependencies):
            result.append(stage)
    return result


def plan_markdown(
    state: Mapping[str, Any],
    *,
    policy: Optional[Mapping[str, Any]] = None,
    registry: Optional[Mapping[str, Any]] = None,
) -> str:
    registry = registry or load_registry()
    policy = policy or build_effective_stage_policy(state, registry=registry)
    artifact_policy = policy.get("artifact_policy") or {}
    lines = [
        "# Pipeline run plan",
        "",
        f"Mode: {state.get('mode', 'unknown')}",
        f"Run profile: {policy['profile_id']}",
        f"Profile policy: {policy['profile_path']}",
        f"Entry: {state.get('entry_status', 'unknown')}",
        f"Current stage: {state.get('current_stage', 'unknown')}",
        f"Snapshot: {state.get('last_snapshot_id', 'unknown')}",
        f"Selected lenses: {', '.join(policy['selected_lenses']) or '-'}",
        f"Skipped lenses: {', '.join(policy['skipped_lenses']) or '-'}",
        f"Artifact projection: {artifact_policy.get('state', 'unknown')}",
        "",
        "This is a routing proposal. It does not confirm mathematical correctness, human decisions, or submission readiness.",
        "Canonical dependencies are unchanged; the run profile only produces an effective stage policy.",
        "",
        "## Stage status",
        "",
        "| stage | skill | status | execution | gate type | blocking | dependencies |",
        "|---|---|---|---|---|---|---|",
    ]
    for stage in registry["default_order"]:
        spec = registry["stages"][stage]
        status = stage_record(state, stage).get("status", "not_started")
        effective = policy["stages"][stage]
        dependencies = ", ".join(spec["depends_on"]) or "-"
        lines.append(
            f"| {stage} | {spec['skill']} | {status} | {effective['execution']} | "
            f"{effective['gate_type']} | {'yes' if effective['blocking'] else 'deferred'} | {dependencies} |"
        )

    ready = ready_stages(state, policy=policy, registry=registry)
    lines.extend(["", "## Ready next", ""])
    if ready:
        for stage in ready:
            skill = registry["stages"][stage]["skill"]
            projection = policy["stages"][stage]["artifact_projection"]
            gate = "blocking core/review gate" if policy["stages"][stage]["blocking"] else "deferred review checkpoint"
            lines.append(
                f"- Run {stage} through {skill}; verify its inputs and write a {projection} artifact; {gate}."
            )
    else:
        lines.append("- No stage is ready. Inspect human gates, blocked dependencies, stale snapshots, or incomplete state.")

    needs_human = [
        stage
        for stage in registry["default_order"]
        if stage_record(state, stage).get("status") == "needs_human"
    ]
    blocked = [
        stage
        for stage in registry["default_order"]
        if stage_record(state, stage).get("status") in {"blocked", "stale", "superseded"}
    ]
    skipped_policy = [
        stage
        for stage, rec in policy["stages"].items()
        if rec["execution"] in POLICY_SATISFIED
    ]
    deferred = [
        stage
        for stage, rec in policy["stages"].items()
        if rec["gate_type"] == "review_checkpoint" and not rec["blocking"]
    ]
    lines.extend(["", "## Human gates", ""])
    lines.append("Core decision gates cannot be cancelled by a run profile. Review checkpoints may be deferred until final adoption.")
    if needs_human:
        lines.extend(
            f"- {stage}: {stage_record(state, stage).get('reason', 'record the decision and scope')}"
            for stage in needs_human
        )
    else:
        lines.append("- No explicit needs_human stage is recorded; this does not mean blocking gates are complete.")
    lines.extend(["", "## Deferred review checkpoints", ""])
    if deferred:
        lines.extend(f"- {stage}: Agent may continue; human review is required before final adoption." for stage in deferred)
    else:
        lines.append("- None. Every review checkpoint is currently blocking.")
    lines.extend(["", "## Policy-skipped stages", ""])
    if skipped_policy:
        for stage in skipped_policy:
            reason = policy["stages"][stage].get("reason") or "skipped by run profile"
            lines.append(f"- {stage}: {reason}")
    else:
        lines.append("- None.")
    lines.extend(["", "## Blocked or recheck", ""])
    if blocked:
        lines.extend(
            f"- {stage}: {stage_record(state, stage).get('reason', 'inspect its issue and upstream evidence')}"
            for stage in blocked
        )
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
