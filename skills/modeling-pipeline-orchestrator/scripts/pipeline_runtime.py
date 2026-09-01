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
DEFAULT_PROFILE = "contest-standard"
WORKING_DEPTHS = {"light", "standard", "full"}
COLLABORATION_MODES = {"adaptive", "light", "standard", "full"}
ACTION_LEVELS = {
    "explain",
    "explore",
    "propose",
    "execute_reversible",
    "adopt",
    "freeze",
    "submit",
}
EXPLORATORY_ACTIONS = {"explain", "explore", "propose", "execute_reversible"}
ADOPTION_ACTIONS = {"adopt", "freeze", "submit"}
ACTION_GATE_VALUES = {"none", "optional", "required"}
FALLBACK_ACTION_GATES = {
    "core_decision": {
        "explain": "none",
        "explore": "none",
        "propose": "none",
        "execute_reversible": "none",
        "adopt": "required",
        "freeze": "required",
        "submit": "required",
    },
    "review_checkpoint": {
        "explain": "none",
        "explore": "none",
        "propose": "none",
        "execute_reversible": "none",
        "adopt": "optional",
        "freeze": "required",
        "submit": "required",
    },
    "none": {action: "none" for action in ACTION_LEVELS},
}
USER_INTENTS = {
    "understand",
    "explore",
    "select_topic",
    "literature",
    "model",
    "experiment",
    "draft",
    "revise",
    "audit",
    "disclose",
    "final_check",
    "release",
    "unknown",
}
INTENT_ACTION_MAP = {
    "understand": "explore",
    "explore": "explore",
    "select_topic": "propose",
    "literature": "explore",
    "model": "explore",
    "experiment": "execute_reversible",
    "draft": "execute_reversible",
    "revise": "execute_reversible",
    "audit": "explore",
    "disclose": "adopt",
    "final_check": "freeze",
    "release": "submit",
    "unknown": "explore",
}
INTENT_STAGE_MAP = {
    "understand": "problem_familiarization",
    "explore": "problem_intake",
    "select_topic": "topic_selection",
    "literature": "literature_evidence",
    "model": "model_architect",
    "experiment": "experiment_validator",
    "draft": "draft",
    "revise": "naturalizer",
    "audit": "paper_review",
    "disclose": "ai_disclosure",
    "final_check": "final_preflight",
    "release": "process_freezer",
}
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
        execution = record.get("execution_requires")
        if execution is None:
            execution = record.get("depends_on") or []
        if not isinstance(execution, list) or any(dep not in stages for dep in execution):
            raise ValueError(f"stage {stage} has an unknown execution requirement")
        if any(positions[dep] >= positions[stage] for dep in execution):
            raise ValueError(f"stage {stage} execution_requires is not topologically ordered")
        depends_on = record.get("depends_on")
        if depends_on is not None and list(depends_on) != list(execution):
            raise ValueError(f"stage {stage} depends_on must match execution_requires")
        for field in ("adoption_requires", "recommended_after"):
            values = record.get(field, [])
            if not isinstance(values, list) or any(dep not in stages for dep in values):
                raise ValueError(f"stage {stage} has an unknown {field} entry")
            if stage in values:
                raise ValueError(f"stage {stage} cannot list itself in {field}")
        gate_type = record.get("gate_type")
        if gate_type not in {"core_decision", "review_checkpoint", "none"}:
            raise ValueError(f"stage {stage} needs a gate_type")
        expected_gate = {
            "core_decision": "required",
            "review_checkpoint": "optional",
            "none": "not_applicable",
        }[gate_type]
        if record.get("human_gate") != expected_gate:
            raise ValueError(
                f"stage {stage} must use human_gate={expected_gate} for gate_type={gate_type}"
            )
        overlay = record.get("action_gates") or {}
        if not isinstance(overlay, dict) or any(
            key not in ACTION_LEVELS or value not in ACTION_GATE_VALUES
            for key, value in overlay.items()
        ):
            raise ValueError(f"stage {stage} has an invalid action_gates overlay")
    defaults = payload.get("default_action_gates")
    if not isinstance(defaults, dict):
        raise ValueError("stage registry needs default_action_gates")
    for gate_type in ("core_decision", "review_checkpoint", "none"):
        mapping = defaults.get(gate_type)
        if not isinstance(mapping, dict) or set(mapping) != ACTION_LEVELS:
            raise ValueError(f"default_action_gates.{gate_type} must cover every action")
        if any(value not in ACTION_GATE_VALUES for value in mapping.values()):
            raise ValueError(f"default_action_gates.{gate_type} has an invalid gate value")
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
            "execution_requires": list(record.get("execution_requires") or record.get("depends_on") or []),
            "adoption_requires": list(record.get("adoption_requires") or []),
            "depends_on": list(record.get("execution_requires") or record.get("depends_on") or []),
            "recommended_after": list(record.get("recommended_after") or []),
            "human_gate": record.get("human_gate"),
            "gate_type": record.get("gate_type"),
            "action_gates": resolve_action_gates(record, registry),
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


def stage_requirement_list(spec: Mapping[str, Any], field: str) -> List[str]:
    if field == "execution_requires":
        return list(spec.get("execution_requires") or spec.get("depends_on") or [])
    return [str(item) for item in (spec.get(field) or [])]


def resolve_action_gates(
    spec: Mapping[str, Any], registry: Mapping[str, Any]
) -> Dict[str, str]:
    gate_type = str(spec.get("gate_type") or "none")
    defaults = registry.get("default_action_gates") or FALLBACK_ACTION_GATES
    merged = dict(defaults.get(gate_type) or FALLBACK_ACTION_GATES.get(gate_type) or {})
    overlay = spec.get("action_gates") or {}
    if isinstance(overlay, Mapping):
        merged.update({str(key): str(value) for key, value in overlay.items()})
    return {action: merged.get(action, "none") for action in ACTION_LEVELS}


def action_gate_for(
    spec: Mapping[str, Any], registry: Mapping[str, Any], action: str
) -> str:
    return resolve_action_gates(spec, registry).get(action, "none")


def resolve_working_depth(state: Mapping[str, Any], profile: Mapping[str, Any]) -> str:
    requested_depth = state.get("working_depth")
    if requested_depth in WORKING_DEPTHS:
        return str(requested_depth)
    requested_mode = state.get("collaboration_mode")
    if requested_mode in WORKING_DEPTHS:
        return str(requested_mode)
    configured = profile.get("collaboration_policy", {}).get("default_mode")
    if configured in WORKING_DEPTHS:
        return str(configured)
    return "standard"


def resolve_collaboration_mode(
    state: Mapping[str, Any], profile: Mapping[str, Any]
) -> str:
    """Alias of working_depth for 0.2 compatibility; adaptive falls back to the profile default."""

    requested = state.get("collaboration_mode")
    if requested in WORKING_DEPTHS:
        if state.get("working_depth") in WORKING_DEPTHS:
            return str(state["working_depth"])
        return str(requested)
    return resolve_working_depth(state, profile)


def persist_artifact_mode(working_depth: str) -> str:
    if working_depth == "full":
        return "required"
    if working_depth == "light":
        return "optional"
    return "checkpoints"


def resolve_user_intent(
    state: Mapping[str, Any], registry: Mapping[str, Any]
) -> Dict[str, Any]:
    raw = state.get("user_intent")
    raw = raw if isinstance(raw, dict) else {}
    goal = str(raw.get("goal") or "unknown")
    if goal not in USER_INTENTS:
        goal = "unknown"
    requested_stage = raw.get("requested_stage")
    requested_stage = str(requested_stage) if requested_stage else None
    target_stage = requested_stage if requested_stage in registry["stages"] else None
    if target_stage is None:
        target_stage = INTENT_STAGE_MAP.get(goal)
    action = raw.get("action")
    if action not in ACTION_LEVELS:
        action = INTENT_ACTION_MAP.get(goal, "explore")
    return {
        "goal": goal,
        "action": action,
        "requested_stage": requested_stage,
        "target_stage": target_stage,
        "scope": raw.get("scope", "unknown"),
        "urgency": raw.get("urgency", "unknown"),
        "allow_provisional_output": raw.get("allow_provisional_output", True),
        "note": raw.get("note", ""),
        "explicit": bool(requested_stage) or goal != "unknown",
    }


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


def _cap_post_draft_lenses(
    lenses: Sequence[str], post_draft: Iterable[str], cap: Any
) -> List[str]:
    if cap == "all":
        return list(lenses)
    selected: List[str] = []
    post_draft_set = set(post_draft)
    selected_post = 0
    for lens in lenses:
        if lens in post_draft_set:
            if selected_post >= int(cap):
                continue
            selected_post += 1
        selected.append(lens)
    return selected


def select_lenses(
    profile: Mapping[str, Any],
    registry: Mapping[str, Any],
    state: Mapping[str, Any],
    *,
    collaboration_mode: str = "standard",
) -> Tuple[List[str], List[str], List[str]]:
    """Return (selected, skipped_conditional, not_in_profile) lens names."""
    known = set(registry["review_lenses"])
    default = [lens for lens in _as_list(profile.get("review_policy", {}).get("lenses")) if lens in known]
    conditional = [lens for lens in _as_list(profile.get("review_policy", {}).get("conditional_lenses")) if lens in known]
    explicit = [lens for lens in _as_list(state.get("selected_lenses")) if lens in known]
    post_draft = set(_post_draft_lenses(registry))
    cap = profile.get("review_policy", {}).get("max_post_draft_lenses", "all")
    if collaboration_mode == "full":
        cap = "all"
    elif collaboration_mode == "light" and cap == "all":
        cap = 2

    pool = list(dict.fromkeys(explicit or default))
    # Explicit selection may include conditional lenses; default selection does not.
    if explicit:
        pool = [lens for lens in pool if lens in set(default) | set(conditional) | set(explicit)]
    selected = (
        _cap_post_draft_lenses(pool, post_draft, cap)
        if explicit
        else apply_selection_rule(
            profile,
            pool,
            post_draft,
            cap,
            prefer_reader=collaboration_mode == "light",
        )
    )

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
    *,
    prefer_reader: bool = False,
) -> List[str]:
    rule = str(profile.get("review_policy", {}).get("selection_rule") or "")
    post_draft_set = set(post_draft)
    balanced_light = prefer_reader and cap != "all"
    if (
        rule != "choose_one_highest_risk_substantive_lens_and_one_reader_or_compliance_lens"
        and not balanced_light
    ):
        return _cap_post_draft_lenses(selected, post_draft_set, cap)
    kept: List[str] = []
    post_kept: List[str] = []
    substantive = next((lens for lens in selected if lens == "substantive"), None)
    reader_or_compliance = next(
        (lens for lens in selected if lens == "reader_experience"),
        None,
    ) or next(
        (lens for lens in selected if lens in {"ai_pattern", "anti_homogenization"}),
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
    working_depth = resolve_working_depth(state, profile)
    collaboration_mode = resolve_collaboration_mode(state, profile)
    selected, skipped_conditional, not_in_profile = select_lenses(
        profile, registry, state, collaboration_mode=working_depth
    )
    intent = resolve_user_intent(state, registry)
    selected_set = set(selected)
    skipped_set = set(skipped_conditional)
    absent_set = set(not_in_profile)
    stage_to_lens = _stage_to_lens(registry)
    review_gates = set(_as_list(profile.get("review_gates")))
    if not review_gates:
        # Backward-compatible fallback for pre-0.2 custom profiles.
        review_gates = {
            stage
            for stage in _as_list(profile.get("human_gates"))
            if stage in registry["stages"]
            and registry["stages"][stage].get("gate_type") == "review_checkpoint"
        }
    if working_depth == "full":
        review_gates = {
            stage
            for stage in registry["default_order"]
            if registry["stages"][stage].get("gate_type") == "review_checkpoint"
        }
    elif working_depth == "light":
        review_gates &= {"paper_review", "reader", "naturalizer"}
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
        current_action = intent.get("action") or "explore"
        action_gates = resolve_action_gates(spec, registry)
        action_gate = action_gates.get(current_action, "none")
        blocking = action_gate == "required"
        artifact_mode = profile.get("artifact_policy", {}).get("state")
        compact = artifact_mode not in {None, "separate_stage_artifacts"}
        if working_depth == "light":
            compact = True
        elif working_depth == "full":
            compact = False
        execution_requires = stage_requirement_list(spec, "execution_requires")
        stages[stage] = {
            "skill": spec["skill"],
            "execution_requires": execution_requires,
            "adoption_requires": stage_requirement_list(spec, "adoption_requires"),
            "depends_on": execution_requires,
            "recommended_after": stage_requirement_list(spec, "recommended_after"),
            "gate_type": gate_type,
            "human_gate": spec["human_gate"],
            "action_gates": action_gates,
            "action_gate": action_gate,
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
        "review_gates": sorted(review_gates),
        "working_depth": working_depth,
        "collaboration_mode": collaboration_mode,
        "persist_artifacts": persist_artifact_mode(working_depth),
        "intent": intent,
        "user_intent_priority": profile.get("collaboration_policy", {}).get(
            "user_intent_priority", True
        ),
        "allow_provisional_work": profile.get("collaboration_policy", {}).get(
            "allow_provisional_work", True
        ),
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
    collaboration_mode = state.get("collaboration_mode")
    if collaboration_mode is not None and collaboration_mode not in COLLABORATION_MODES:
        errors.append(f"unknown collaboration mode: {collaboration_mode}")
    working_depth = state.get("working_depth")
    if working_depth is not None and working_depth not in WORKING_DEPTHS:
        errors.append(f"unknown working depth: {working_depth}")
    user_intent = state.get("user_intent")
    if isinstance(user_intent, dict):
        requested_stage = user_intent.get("requested_stage")
        if requested_stage and requested_stage not in stages:
            errors.append(f"user_intent.requested_stage is not in the registry: {requested_stage}")
        action = user_intent.get("action")
        if action is not None and action not in ACTION_LEVELS:
            errors.append(f"unknown user_intent.action: {action}")
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
            canonical = stage_requirement_list(stages[stage], "execution_requires")
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
        review_gates = _as_list(profile.get("review_gates"))
        unknown_review_gates = [stage for stage in review_gates if stage not in stages]
        if unknown_review_gates:
            errors.append("run profile has unknown review gates: " + ", ".join(unknown_review_gates))
        invalid_review_gates = [
            stage
            for stage in review_gates
            if stage in stages and stages[stage].get("gate_type") != "review_checkpoint"
        ]
        if invalid_review_gates:
            errors.append("run profile review_gates must target review checkpoints: " + ", ".join(invalid_review_gates))
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def dependency_satisfied(state: Mapping[str, Any], policy: Mapping[str, Any], dependency: str) -> bool:
    """Execution-level satisfaction: passed/skipped, or a policy-skipped review lens."""

    status = stage_record(state, dependency).get("status", "not_started")
    if status in SATISFIED:
        return True
    execution = policy["stages"][dependency]["execution"]
    return execution in POLICY_SATISFIED and status in {"not_started", "ready", "skipped"}


def execution_satisfied(state: Mapping[str, Any], policy: Mapping[str, Any], dependency: str) -> bool:
    return dependency_satisfied(state, policy, dependency)


def adoption_satisfied(
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    dependency: str,
    *,
    registry: Optional[Mapping[str, Any]] = None,
) -> bool:
    """Adoption-level satisfaction: execution plus a human-confirmed decision for required gates."""

    if not execution_satisfied(state, policy, dependency):
        return False
    registry = registry or load_registry()
    spec = registry["stages"][dependency]
    gates = resolve_action_gates(spec, registry)
    if gates.get("adopt") != "required" and spec.get("gate_type") != "core_decision":
        return True
    record = stage_record(state, dependency)
    execution = policy["stages"][dependency]["execution"]
    if execution in POLICY_SATISFIED and record.get("status", "not_started") in {
        "not_started",
        "ready",
        "skipped",
    }:
        return True
    return _has_confirmed_marker(record.get("human_status")) and bool(_decision_ids(record))


def hard_prerequisite_closure(registry: Mapping[str, Any], stage: str) -> List[str]:
    """Return a target stage and its hard prerequisites in canonical order."""

    if stage not in registry["stages"]:
        return []
    closure = set()

    def visit(current: str) -> None:
        if current in closure:
            return
        closure.add(current)
        for dependency in stage_requirement_list(registry["stages"][current], "execution_requires"):
            visit(str(dependency))

    visit(stage)
    return [candidate for candidate in registry["default_order"] if candidate in closure]


def stage_input_available(
    state: Mapping[str, Any], stage: str, target_stage: Optional[str]
) -> bool:
    """Avoid advertising an empty-state writing stage without hiding explicit user work."""

    if stage != "draft":
        return True
    if target_stage == "draft":
        return True
    artifacts = state.get("artifacts") or []
    if any(
        isinstance(artifact, dict) and artifact.get("status") == "present"
        for artifact in artifacts
    ):
        return True
    return any(
        stage_record(state, prerequisite).get("status") in SATISFIED
        for prerequisite in ("problem_intake", "paper_architect", "experiment_validator")
    )


def recommended_frontier(
    result: Sequence[str],
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    registry: Mapping[str, Any],
    target_stage: Optional[str],
) -> List[str]:
    """Without an explicit user goal, follow recommended_after rather than advertising every executable stage."""

    filtered: List[str] = []
    for stage in result:
        spec = registry["stages"][stage]
        if stage == "draft" and stage_input_available(state, stage, target_stage):
            filtered.append(stage)
            continue
        recommended = stage_requirement_list(spec, "recommended_after")
        if all(dependency_satisfied(state, policy, dep) for dep in recommended):
            filtered.append(stage)
    return filtered


def ready_stages(
    state: Mapping[str, Any],
    *,
    policy: Optional[Mapping[str, Any]] = None,
    registry: Optional[Mapping[str, Any]] = None,
) -> List[str]:
    registry = registry or load_registry()
    policy = policy or build_effective_stage_policy(state, registry=registry)
    intent = policy.get("intent") or {}
    action = intent.get("action") or "explore"
    target_stage = intent.get("target_stage")
    explicit = bool(intent.get("explicit"))
    result = []
    for stage in registry["default_order"]:
        execution = policy["stages"][stage]["execution"]
        if execution in POLICY_SATISFIED | {"conditional"}:
            continue
        status = stage_record(state, stage).get("status", "not_started")
        if status not in {"not_started", "ready", "stale"}:
            continue
        if not stage_input_available(state, stage, target_stage):
            continue
        spec = registry["stages"][stage]
        execution_requires = stage_requirement_list(spec, "execution_requires")
        if not all(dependency_satisfied(state, policy, dep) for dep in execution_requires):
            continue
        if action in ADOPTION_ACTIONS:
            adoption_requires = stage_requirement_list(spec, "adoption_requires")
            if not all(
                adoption_satisfied(state, policy, dep, registry=registry)
                for dep in adoption_requires
            ):
                continue
        result.append(stage)
    if target_stage in result:
        return [target_stage] + [stage for stage in result if stage != target_stage]
    if target_stage and stage_record(state, target_stage).get("status", "not_started") in {
        "not_started",
        "ready",
        "stale",
    }:
        target_path = set(hard_prerequisite_closure(registry, target_stage))
        focused = [stage for stage in result if stage in target_path]
        if focused:
            return focused
    if not explicit:
        return recommended_frontier(result, state, policy, registry, target_stage)
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
        f"Working depth: {policy.get('working_depth', policy['collaboration_mode'])}",
        f"Collaboration mode: {policy['collaboration_mode']}",
        f"Persist artifacts: {policy.get('persist_artifacts', 'checkpoints')}",
        f"Profile policy: {policy['profile_path']}",
        f"Entry: {state.get('entry_status', 'unknown')}",
        f"Current stage: {state.get('current_stage', 'unknown')}",
        f"Snapshot: {state.get('last_snapshot_id', 'unknown')}",
        f"Selected lenses: {', '.join(policy['selected_lenses']) or '-'}",
        f"Skipped lenses: {', '.join(policy['skipped_lenses']) or '-'}",
        f"Artifact projection: {artifact_policy.get('state', 'unknown')}",
        f"User intent: {policy['intent']['goal']}",
        f"Intent action: {policy['intent'].get('action') or '-'}",
        f"Intent target: {policy['intent'].get('target_stage') or '-'}",
        "",
        "This is a routing proposal. It does not confirm mathematical correctness, human decisions, or submission readiness.",
        "User intent has priority over the recommended order; hard dependencies and human decision boundaries remain in force.",
        "Canonical dependencies are unchanged; execution_requires remain blocking for the requested task, while adoption_requires only block adopt/freeze/submit and recommended_after entries are advisory and do not block an explicitly requested task.",
        "",
        "## Stage status",
        "",
        "| stage | skill | status | execution | gate type | action gate | blocking | execution requires | adoption requires | recommended after |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for stage in registry["default_order"]:
        spec = registry["stages"][stage]
        status = stage_record(state, stage).get("status", "not_started")
        effective = policy["stages"][stage]
        execution_requires = ", ".join(stage_requirement_list(spec, "execution_requires")) or "-"
        adoption_requires = ", ".join(stage_requirement_list(spec, "adoption_requires")) or "-"
        recommended = ", ".join(stage_requirement_list(spec, "recommended_after")) or "-"
        lines.append(
            f"| {stage} | {spec['skill']} | {status} | {effective['execution']} | "
            f"{effective['gate_type']} | {effective.get('action_gate', '-')} | "
            f"{'yes' if effective['blocking'] else 'deferred'} | "
            f"{execution_requires} | {adoption_requires} | {recommended} |"
        )

    ready = ready_stages(state, policy=policy, registry=registry)
    lines.extend(["", "## Ready next", ""])
    if ready:
        for stage in ready:
            skill = registry["stages"][stage]["skill"]
            projection = policy["stages"][stage]["artifact_projection"]
            gate = (
                "required action gate for the current intent; propose and wait for a decision_id"
                if policy["stages"][stage]["blocking"]
                else "no required action gate for the current intent"
            )
            lines.append(
                f"- Run {stage} through {skill}; verify its inputs and write a {projection} artifact if useful; {gate}."
            )
    else:
        lines.append("- No stage is ready. Inspect human gates, blocked dependencies, stale snapshots, or incomplete state.")

    needs_human = [
        stage
        for stage in registry["default_order"]
        if stage_record(state, stage).get("status") == "needs_human"
    ]
    core_needs_human = [
        stage
        for stage in needs_human
        if registry["stages"][stage].get("gate_type") == "core_decision"
    ]
    review_needs_human = [stage for stage in needs_human if stage not in core_needs_human]
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
    lines.append("Core decision gates cannot be cancelled by a run profile. Review checkpoints are advisory unless the selected profile marks them for adoption review.")
    if core_needs_human:
        lines.extend(
            f"- {stage}: {stage_record(state, stage).get('reason', 'record the decision and scope')}"
            for stage in core_needs_human
        )
    else:
        lines.append("- No core decision is waiting in the current state; this does not mean final gates are complete.")
    if review_needs_human:
        lines.extend(
            f"- Review checkpoint {stage}: may remain pending while the user-requested work continues; check before final adoption."
            for stage in review_needs_human
        )
    lines.extend(["", "## Deferred review checkpoints", ""])
    if deferred:
        lines.extend(f"- {stage}: Agent may continue; human review is required before final adoption." for stage in deferred)
    else:
        lines.append("- None. No selected review checkpoint is currently blocking.")
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
    target_stage = policy.get("intent", {}).get("target_stage")
    safe_action = compose_safe_next_action(
        state,
        policy,
        ready=ready,
        core_needs_human=core_needs_human,
        review_needs_human=review_needs_human,
        blocked=blocked,
        target_stage=target_stage,
    )
    lines.extend(
        [
            "",
            "## Safe next action",
            "",
            safe_action + " Do not alter a core model, assumption, result, conclusion, or disclosure record without a human decision event.",
        ]
    )
    return "\n".join(lines) + "\n"


def compose_safe_next_action(
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    ready: Sequence[str],
    core_needs_human: Sequence[str],
    review_needs_human: Sequence[str],
    blocked: Sequence[str],
    target_stage: Optional[str],
) -> str:
    working_depth = str(policy.get("working_depth") or "standard")
    persist = str(policy.get("persist_artifacts") or "checkpoints")
    intent = policy.get("intent") or {}
    action = str(intent.get("action") or "explore")
    explicit = bool(intent.get("explicit"))
    local_turn = working_depth == "light" or (
        explicit and action in EXPLORATORY_ACTIONS and persist != "required"
    )
    finalish = working_depth == "full" or persist == "required" or state.get("mode") in {
        "final_check",
        "disclose",
    }
    if ready:
        if target_stage in ready:
            priority = f" Prioritize the requested target {target_stage}."
        elif target_stage:
            priority = " The requested target is not ready, so continue with its nearest hard prerequisite."
        else:
            priority = ""
        blocking_ready = [stage for stage in ready if policy["stages"][stage]["blocking"]]
        if local_turn:
            body = (
                "Continue the requested task directly. "
                "Do not open a process-freezer manifest or generate ledgers unless the user asked to persist state, this is a final delivery, or working_depth is full."
            )
        elif finalish:
            body = (
                "Continue the requested task. Read only the artifacts needed this turn. "
                "Update the process-freezer manifest because this is a full-depth or final-delivery pass."
            )
        else:
            body = (
                "Continue the requested task. Read input artifacts only if they are needed for this turn. "
                "Check the process-freezer manifest only for cross-session resume, full depth, or final delivery."
            )
        if blocking_ready and action in ADOPTION_ACTIONS:
            body += (
                f" Action `{action}` is a required human gate for {', '.join(blocking_ready)}; "
                "present the proposal and wait for a decision_id before marking adopted, frozen, or submitted."
            )
        return body + priority
    if core_needs_human:
        return "Resolve the listed human gates and record decision IDs before rerunning downstream stages."
    if review_needs_human:
        return "Review checkpoints are not a global stop; continue the user's requested work and carry these checks to final adoption."
    if blocked:
        return "Inspect the listed blocked or stale stages and their upstream evidence before rerunning anything."
    return "Inspect the incomplete state and continue the smallest user-requested task. Check a process-freezer manifest only for cross-session resume, full depth, or final delivery."
