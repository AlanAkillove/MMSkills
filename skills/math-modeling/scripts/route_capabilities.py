#!/usr/bin/env python3
"""L1.5 capability retrieval: query → task facets → candidates → min cover.

This is high-recall discovery, not a workflow engine. It does not load SKILL.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set


try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


CAP_DIR = Path(__file__).resolve().parents[1] / "references" / "capabilities"
ROLE_FILES = {
    "modeler": CAP_DIR / "modeler.yaml",
    "computationalist": CAP_DIR / "computationalist.yaml",
    "writer": CAP_DIR / "writer.yaml",
}
CRITICAL_PATH = CAP_DIR / "critical.yaml"
SHARED_PATH = CAP_DIR / "shared.yaml"
INVALIDATE = re.compile(
    r"重新建模|物理模型|换题|改做编程|跑代码|机理研究|重新研究",
    re.I,
)


def _load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load capability indexes")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be an object")
    return payload


def load_indexes() -> Dict[str, Dict[str, Any]]:
    return {role: _load_yaml(path) for role, path in ROLE_FILES.items()}


def load_critical() -> Dict[str, Any]:
    return _load_yaml(CRITICAL_PATH)


def load_shared() -> Dict[str, Any]:
    if not SHARED_PATH.is_file():
        return {}
    return _load_yaml(SHARED_PATH)


def extract_facets(query: str, index: Dict[str, Any]) -> List[str]:
    text = query.strip()
    found: List[str] = []
    cues = index.get("facet_cues") or {}
    for facet, pattern in cues.items():
        if not pattern:
            continue
        if re.search(str(pattern), text, re.I):
            found.append(str(facet))
    return found


def extract_all_facets(
    query: str, indexes: Optional[Dict[str, Dict[str, Any]]] = None
) -> Dict[str, List[str]]:
    indexes = indexes or load_indexes()
    return {role: extract_facets(query, index) for role, index in indexes.items()}


def imply_role(facets_by_role: Dict[str, List[str]]) -> Optional[str]:
    scored = sorted(
        ((role, facets) for role, facets in facets_by_role.items() if facets),
        key=lambda item: len(item[1]),
        reverse=True,
    )
    if not scored:
        return None
    role, facets = scored[0]
    exclusive = {
        "writer": {"review", "format", "abstract", "naturalize", "preflight"},
        "modeler": {"understand", "intake", "model", "literature", "topic"},
        "computationalist": {"experiment", "figure", "data_change"},
    }
    if len(facets) >= 2:
        return role
    if facets and set(facets) & exclusive.get(role, set()):
        return role
    return None


def coverage_of(index: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
    raw = index.get("coverage") or {}
    parsed: Dict[str, Dict[str, int]] = {}
    for skill, weights in raw.items():
        parsed[str(skill)] = {str(facet): int(value) for facet, value in (weights or {}).items()}
    return parsed


def min_cover(
    facets: Sequence[str],
    index: Dict[str, Any],
    *,
    exclude: Optional[Iterable[str]] = None,
) -> List[str]:
    uncovered: Set[str] = set(facets)
    selected: List[str] = []
    blocked = set(exclude or [])
    matrix = coverage_of(index)
    costs = {str(k): int(v) for k, v in (index.get("cost") or {}).items()}
    while uncovered:
        best: Optional[str] = None
        best_score: Optional[tuple[int, int, int]] = None
        for skill, weights in matrix.items():
            if skill in selected or skill in blocked:
                continue
            gain = sum(weights.get(facet, 0) for facet in uncovered)
            if gain <= 0:
                continue
            primary = sum(1 for facet in uncovered if weights.get(facet, 0) >= 2)
            score = (gain, primary, -costs.get(skill, 2))
            if best_score is None or score > best_score:
                best = skill
                best_score = score
        if best is None:
            break
        selected.append(best)
        for facet, weight in matrix[best].items():
            if weight >= 1:
                uncovered.discard(facet)
    return selected


def critical_hits(query: str, facets: Sequence[str], critical: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    critical = critical or load_critical()
    text = query.strip()
    consideration: List[str] = []
    promote: List[str] = []
    matched: List[str] = []
    for name, spec in (critical.get("items") or {}).items():
        cues = spec.get("cues")
        if not cues or not re.search(str(cues), text, re.I):
            continue
        matched.append(str(name))
        required = [str(item) for item in (spec.get("require_consideration") or [])]
        consideration.extend(required)
        promote_when = set(str(item) for item in (spec.get("promote_when_any_facet") or []))
        if promote_when and (set(facets) & promote_when):
            promote.extend(required)
    # preserve order, drop dups
    def _uniq(items: List[str]) -> List[str]:
        seen: Set[str] = set()
        ordered: List[str] = []
        for item in items:
            if item not in seen:
                seen.add(item)
                ordered.append(item)
        return ordered

    return {
        "matched": matched,
        "mandatory_consideration": _uniq(consideration),
        "promote": _uniq(promote),
    }


def working_set_status(
    query: str,
    *,
    role: Optional[str],
    facets: Sequence[str],
    working_set: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not working_set:
        return {"hit": False, "reason": "absent"}
    active = working_set.get("active_working_set") or working_set
    if INVALIDATE.search(query):
        return {"hit": False, "reason": "invalidated"}
    cached_role = active.get("role")
    if role and cached_role and role not in {"unknown", "inherit"} and role != cached_role:
        return {"hit": False, "reason": "role_shift"}
    recent = set(active.get("recent_capabilities") or [])
    novel = [facet for facet in facets if facet not in recent]
    if novel:
        return {"hit": False, "reason": "new_facets", "novel_facets": novel}
    if not facets:
        return {"hit": True, "reason": "hit"}
    return {"hit": False, "reason": "same_role_new_query"}


def retrieve_capabilities(
    query: str,
    *,
    role: Optional[str] = None,
    intent: Optional[str] = None,
    working_set: Optional[Dict[str, Any]] = None,
    indexes: Optional[Dict[str, Dict[str, Any]]] = None,
    critical: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    indexes = indexes or load_indexes()
    critical = critical or load_critical()
    shared_index = load_shared()
    by_role = extract_all_facets(query, indexes)
    implied = imply_role(by_role)
    resolved_role = role if role and role not in {"unknown", "inherit", "cross_cutting"} else implied
    facets = list(by_role.get(resolved_role or "", []) or [])
    shared_facets = extract_facets(query, shared_index) if shared_index else []
    cache = working_set_status(query, role=resolved_role, facets=facets, working_set=working_set)
    index = indexes.get(resolved_role or "", {})
    diagnosis = bool(set(facets) & set(index.get("diagnosis_facets") or []))
    exclude = list(index.get("exclude_when_diagnosing") or []) if diagnosis else []
    if intent == "draft_full":
        exclude.append("modeling-paper-writer")
    selected = min_cover(facets, index, exclude=exclude) if facets and index else []
    shared_selected = min_cover(shared_facets, shared_index) if shared_facets and shared_index else []
    crit = critical_hits(query, facets, critical)
    if diagnosis:
        for skill in crit.get("promote") or []:
            if skill not in selected:
                selected.append(skill)

    def _uniq(items: List[str]) -> List[str]:
        seen: Set[str] = set()
        ordered: List[str] = []
        for item in items:
            if item not in seen:
                seen.add(item)
                ordered.append(item)
        return ordered

    candidates = list(selected)
    for skill, weights in coverage_of(index).items():
        if skill in candidates or skill in exclude:
            continue
        if any(facet in weights for facet in facets):
            candidates.append(skill)
    for skill in crit.get("mandatory_consideration") or []:
        if skill not in candidates:
            candidates.append(skill)
    for skill in shared_selected:
        if skill not in candidates:
            candidates.append(skill)
    facet_count = len(facets)
    return {
        "role": resolved_role,
        "implied_role": implied,
        "task_facets": facets,
        "shared_facets": shared_facets,
        "facets_by_role": by_role,
        "candidates": _uniq(candidates),
        "specialists": selected,
        "shared_specialists": shared_selected,
        "mandatory_consideration": crit["mandatory_consideration"],
        "critical_matched": crit["matched"],
        "working_set": cache,
        "diagnosis": diagnosis,
        "expandable": facet_count >= 2,
        "precision_locked": facet_count <= 1,
    }


def should_expand(intent: str, retrieval: Dict[str, Any], current_specialists: Sequence[str]) -> bool:
    """Fan-out when the request itself has multiple facets, not because of intent type."""
    facets = retrieval.get("task_facets") or []
    selected = retrieval.get("specialists") or []
    if retrieval.get("working_set", {}).get("hit") and not facets:
        return False
    if len(facets) >= 2:
        return True
    if intent in {"review", "composite_review", "preflight"} and selected:
        return set(selected) != set(current_specialists) and len(selected) >= len(current_specialists)
    return False


def merge_specialists(base: Sequence[str], extra: Sequence[str]) -> List[str]:
    seen: Set[str] = set()
    ordered: List[str] = []
    for item in list(base) + list(extra):
        if item and item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--role", choices=["modeler", "computationalist", "writer"])
    parser.add_argument("--intent")
    parser.add_argument("--working-set", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    working_set = None
    if args.working_set:
        working_set = _load_yaml(args.working_set)
    payload = retrieve_capabilities(
        args.query,
        role=args.role,
        intent=args.intent,
        working_set=working_set,
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"ROLE: {payload['role'] or '-'}")
    print(f"FACETS: {', '.join(payload['task_facets']) or '-'}")
    print(f"CANDIDATES: {', '.join(payload['candidates']) or '-'}")
    print(f"MIN_COVER: {', '.join(payload['specialists']) or '-'}")
    print(f"MANDATORY_CONSIDERATION: {', '.join(payload['mandatory_consideration']) or '-'}")
    print(f"WORKING_SET: {payload['working_set'].get('reason')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
