#!/usr/bin/env python3
"""Resolve quality requirements for an artifact state transition.

This is an execution constraint, not a workflow engine and not a Skill.
Missing review evidence still allows discussion; it does not allow marking
adopted / frozen / paper / assembled / finalized.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


POLICY_PATH = Path(__file__).resolve().parents[1] / "references" / "capabilities" / "quality-policy.yaml"

PASS_STATUSES = {"pass", "passed", "complete", "done", "ok"}
INDEPENDENT_ISOLATION = {"fresh_subagent", "independent_subagent"}
TARGET_ALIASES = {
    "adopt": "adopted",
    "adopted": "adopted",
    "accept": "accepted",
    "accepted": "accepted",
    "freeze": "frozen",
    "freeze_claim_bearing": "frozen",
    "frozen": "frozen",
    "promote": "paper",
    "promote_from_diagnostic": "paper",
    "paper": "paper",
    "assembly": "accepted-for-assembly",
    "accepted-for-assembly": "accepted-for-assembly",
    "reviewed": "reviewed",
    "final": "finalized",
    "finalized": "finalized",
    "compliance_claim": "claimed_compliant",
    "claimed_compliant": "claimed_compliant",
}
GATED_TARGETS = {
    "model_candidate": {"adopted", "reviewed", "finalized"},
    "high_impact_assumption": {"accepted", "reviewed", "finalized"},
    "result": {"frozen", "reviewed", "finalized"},
    "paper_figure": {"paper", "reviewed", "finalized"},
    "manuscript_section": {"accepted-for-assembly", "reviewed"},
    "abstract_or_conclusion": {"accepted-for-assembly", "reviewed"},
    "final_manuscript": {"finalized", "reviewed"},
    "rules_format": {"claimed_compliant"},
}
HUMAN_TARGETS = {"adopted", "accepted", "frozen", "finalized", "claimed_compliant"}


def _load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load quality-policy.yaml")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be an object")
    return payload


def load_policy(path: Path = POLICY_PATH) -> Dict[str, Any]:
    return _load_yaml(path)


def _uniq(items: Iterable[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def canonicalize_target(target_state: str) -> str:
    key = (target_state or "").strip()
    return TARGET_ALIASES.get(key, key)


def _requirement_block(kind: str, spec: Dict[str, Any], *, risk: str) -> Dict[str, Any]:
    raw = spec.get(kind)
    if kind == "review" and not raw:
        raw = spec.get("visual_review")
    intensity = spec.get("intensity")
    if kind == "review" and isinstance(raw, dict) and "required" not in raw:
        if intensity in {"Q2", "Q3"}:
            raw = {**raw, "required": True}
    if kind == "audit" and not raw:
        return {"required": False}
    if raw in (None, False):
        return {"required": False}
    if raw == "only_if_rule_ambiguous":
        return {"required": False, "when": "rule_ambiguous"}
    if not isinstance(raw, dict):
        if raw == "high_risk":
            return {
                "required": risk == "high",
                "recommended": True,
                "mode": "independent_subagent",
            }
        required = bool(raw)
        return {"required": required, "mode": "independent_subagent" if required else None}
    required = bool(raw.get("required"))
    recommended = bool(raw.get("recommended"))
    if kind == "challenge":
        if spec.get("challenge") == "high_risk" or raw.get("mode") and risk == "high":
            required = required or risk == "high"
            recommended = True
        if isinstance(spec.get("challenge"), dict):
            required = bool(spec["challenge"].get("required", required))
    return {
        "required": required,
        "recommended": recommended,
        "mode": raw.get("mode"),
        "owner": raw.get("owner"),
        "question": raw.get("question"),
        "scoped": raw.get("scoped"),
        "full": raw.get("full"),
    }


def _audit_for_figure(spec: Dict[str, Any], figure_kind: Optional[str]) -> Dict[str, Any]:
    audits = spec.get("evidence_audit") or {}
    kind = figure_kind or "quantitative"
    chosen = audits.get(kind) or audits.get("quantitative") or ["visual_brief", "data_unit_audit"]
    return {
        "required": True,
        "mode": "tool",
        "owner": (spec.get("audit") or {}).get("owner"),
        "checks": list(chosen),
        "figure_kind": kind,
    }


def _evidence_section(evidence: Optional[Dict[str, Any]], name: str) -> Dict[str, Any]:
    if not evidence:
        return {}
    block = evidence.get(name) or {}
    return block if isinstance(block, dict) else {}


def _status_ok(block: Dict[str, Any]) -> bool:
    return str(block.get("status") or "").lower() in PASS_STATUSES


def _hash_ok(block: Dict[str, Any], artifact_hash: Optional[str]) -> bool:
    recorded = block.get("artifact_hash")
    if not artifact_hash:
        return bool(recorded)
    return recorded == artifact_hash


def _open_findings(block: Dict[str, Any]) -> bool:
    open_items = block.get("findings_open")
    if open_items in (None, False, 0, []):
        return False
    if isinstance(open_items, list):
        return any(
            str(item.get("severity") if isinstance(item, dict) else item).upper() in {"P0", "P1"}
            for item in open_items
        )
    return bool(open_items)


def evaluate_evidence(
    *,
    kind: str,
    required: bool,
    block: Dict[str, Any],
    artifact_hash: Optional[str],
) -> Tuple[str, Optional[str]]:
    if not required:
        return "not_required", None
    if not block:
        return "missing", f"missing_{kind}"
    if not _status_ok(block):
        return "incomplete", f"{kind}_incomplete"
    if not _hash_ok(block, artifact_hash):
        return "stale", f"{kind}_stale_hash"
    if kind in {"review", "challenge"}:
        isolation = str(block.get("isolation") or "")
        if isolation in {"unavailable", "non_isolated", "same_context"}:
            return "not_independent", f"{kind}_isolation_unavailable"
        if isolation not in INDEPENDENT_ISOLATION:
            return "not_independent", f"{kind}_not_independent"
        if _open_findings(block):
            return "blocked", f"{kind}_open_findings"
    return "ok", None


def _review_unit(policy: Dict[str, Any], artifact_type: str, bundle: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    units = policy.get("review_units") or {}
    if bundle:
        return {
            "kind": bundle.get("kind") or "question_bundle",
            "one_subagent": True,
            "members": list(bundle.get("members") or []),
            "lens": bundle.get("lens") or (units.get("question_bundle") or {}).get("lens"),
        }
    mapping = {
        "manuscript_section": "question_bundle",
        "result": "question_bundle",
        "paper_figure": "question_bundle",
        "abstract_or_conclusion": "manuscript_bundle",
        "final_manuscript": "manuscript_bundle",
        "model_candidate": "model_bundle",
        "high_impact_assumption": "assumption_bundle",
    }
    name = mapping.get(artifact_type)
    spec = units.get(name) or {}
    return {
        "kind": name or "artifact",
        "one_subagent": bool(spec.get("one_review", True)),
        "member_types": list(spec.get("member_types") or [artifact_type]),
        "lens": spec.get("lens"),
    }


def resolve_quality_requirements(
    artifact_type: str,
    current_state: str,
    target_state: str,
    *,
    risk: str = "standard",
    figure_kind: Optional[str] = None,
    quality_evidence: Optional[Dict[str, Any]] = None,
    artifact_hash: Optional[str] = None,
    bundle: Optional[Dict[str, Any]] = None,
    policy: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    policy = policy or load_policy()
    target = canonicalize_target(target_state)
    current = (current_state or "candidate").strip() or "candidate"
    spec = (policy.get("artifact_types") or {}).get(artifact_type) or {}
    gated = target in GATED_TARGETS.get(artifact_type, set())
    audit = (
        _audit_for_figure(spec, figure_kind)
        if artifact_type == "paper_figure"
        else _requirement_block("audit", spec, risk=risk)
    )
    if artifact_type == "paper_figure":
        audit["required"] = True
    review = _requirement_block("review", spec, risk=risk)
    challenge = _requirement_block("challenge", spec, risk=risk)
    if spec.get("challenge") == "high_risk" and risk == "high":
        challenge["required"] = True
        challenge["recommended"] = True
    human_required = gated and target in HUMAN_TARGETS
    if artifact_type == "paper_figure":
        human_required = False

    gaps: List[str] = []
    audit_state, audit_gap = evaluate_evidence(
        kind="audit",
        required=bool(audit.get("required")) and gated,
        block=_evidence_section(quality_evidence, "audit"),
        artifact_hash=artifact_hash,
    )
    review_state, review_gap = evaluate_evidence(
        kind="review",
        required=bool(review.get("required")) and gated,
        block=_evidence_section(quality_evidence, "review"),
        artifact_hash=artifact_hash,
    )
    challenge_state, challenge_gap = evaluate_evidence(
        kind="challenge",
        required=bool(challenge.get("required")) and gated,
        block=_evidence_section(quality_evidence, "challenge"),
        artifact_hash=artifact_hash,
    )
    for gap in (audit_gap, review_gap, challenge_gap):
        if gap:
            gaps.append(gap)
    human_block = _evidence_section(quality_evidence, "human_decision")
    if human_required:
        if str(human_block.get("status") or "").lower() not in {"confirmed", "approved", "signed"}:
            gaps.append("human_decision_pending")

    allowed = (not gated) or not gaps
    return {
        "artifact_type": artifact_type,
        "current_state": current,
        "target_state": target,
        "gated": gated,
        "allowed": allowed,
        "allow_discussion": True,
        "block_reason": None if allowed else (gaps[0] if gaps else "quality_evidence_missing"),
        "gaps": gaps,
        "risk": risk,
        "requirements": {
            "audit": {**audit, "evidence_status": audit_state},
            "review": {**review, "evidence_status": review_state},
            "challenge": {**challenge, "evidence_status": challenge_state},
            "human_decision": {
                "required": human_required,
                "evidence_status": "ok" if human_required and "human_decision_pending" not in gaps else (
                    "not_required" if not human_required else "missing"
                ),
            },
        },
        "review_unit": _review_unit(policy, artifact_type, bundle),
        "note": (
            "Discussion is allowed without quality evidence. "
            "Do not mark the target state until required audit/review/challenge "
            "cover this artifact_hash. One review_unit uses one Subagent."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-type", required=True)
    parser.add_argument("--current-state", default="candidate")
    parser.add_argument("--target-state", required=True)
    parser.add_argument("--risk", default="standard", choices=["standard", "high"])
    parser.add_argument("--figure-kind", choices=["quantitative", "conceptual"])
    parser.add_argument("--artifact-hash")
    parser.add_argument("--evidence", type=Path, help="quality_evidence YAML/JSON")
    parser.add_argument("--bundle", type=Path, help="optional review bundle JSON/YAML")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    evidence = None
    bundle = None
    if args.evidence:
        text = args.evidence.read_text(encoding="utf-8")
        evidence = json.loads(text) if args.evidence.suffix == ".json" else _load_yaml(args.evidence)
    if args.bundle:
        text = args.bundle.read_text(encoding="utf-8")
        bundle = json.loads(text) if args.bundle.suffix == ".json" else _load_yaml(args.bundle)
    payload = resolve_quality_requirements(
        args.artifact_type,
        args.current_state,
        args.target_state,
        risk=args.risk,
        figure_kind=args.figure_kind,
        quality_evidence=evidence,
        artifact_hash=args.artifact_hash,
        bundle=bundle,
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"TRANSITION: {payload['current_state']} -> {payload['target_state']}")
        print(f"ALLOWED: {payload['allowed']}")
        print(f"BLOCK: {payload['block_reason'] or '-'}")
        print(f"GAPS: {', '.join(payload['gaps']) or '-'}")
        print(f"REVIEW_UNIT: {payload['review_unit'].get('kind')}")
    return 0 if payload["allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
