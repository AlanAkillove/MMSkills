#!/usr/bin/env python3
"""Route a user turn to one role and a small specialist set. This is not a workflow engine."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


ROOT = Path(__file__).resolve().parents[3]
ROUTING_PATH = Path(__file__).resolve().parents[1] / "references" / "specialist-routing.yaml"

INTENT_PATTERNS: List[tuple[str, re.Pattern[str]]] = [
    ("resume", re.compile(r"恢复会话|跨会话|handoff|process-freezer|续接上次", re.I)),
    ("full_audit", re.compile(r"全流程审计|完整审查|full audit", re.I)),
    ("submission_plan", re.compile(r"提交计划|安排提交|submission plan", re.I)),
    ("diagnose_state", re.compile(r"项目状态诊断|stage registry|pipeline plan", re.I)),
    ("disclose", re.compile(r"AI\s*披露|使用详情\.pdf|disclosure", re.I)),
    ("preflight", re.compile(r"提交前|终检|preflight", re.I)),
    ("terminology_audit", re.compile(r"术语漂移|术语审查|terminology drift", re.I)),
    ("terminology_establish", re.compile(r"术语表|统一叫|canonical term|terminology_table", re.I)),
    ("literature", re.compile(r"文献|相关工作|论文检索|DOI|orientation", re.I)),
    ("figure", re.compile(r"画图|绘图|检查图|figure|plot", re.I)),
    ("experiment", re.compile(r"实验|跑代码|数值|求解|python|matlab", re.I)),
    ("model", re.compile(r"比较.*模型|候选模型|模型设计|采用这个模型", re.I)),
    ("understand", re.compile(r"理解|弄懂|歧管|机理|题意|familiar", re.I)),
    ("revise", re.compile(r"重写摘要|改摘要|续写|自然化|5\.3|章节", re.I)),
    ("draft", re.compile(r"写论文|正文|摘要|draft", re.I)),
    ("continue_local", re.compile(r"继续问题|接着(写|做|算)|continue (question|q)\s*\d+", re.I)),
]


def load_routing(path: Path = ROUTING_PATH) -> Dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("specialist-routing.yaml must be an object")
    return payload


def classify_intent(query: str) -> str:
    text = query.strip()
    if not text:
        return "continue_local"
    for intent, pattern in INTENT_PATTERNS:
        if pattern.search(text):
            return intent
    return "continue_local"


def _as_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def route_query(
    query: str,
    *,
    current_role: Optional[str] = None,
    routing: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    routing = routing or load_routing()
    intent = classify_intent(query)
    spec = (routing.get("intents") or {}).get(intent) or {}
    role = spec.get("role") or "inherit"
    if role == "inherit":
        role = current_role or "modeler"
    specialists = _as_list(spec.get("specialists"))
    orchestrator_intents = set(_as_list(routing.get("orchestrator_intents")))
    never_preload = _as_list(routing.get("never_preload"))
    load_orchestrator = intent in orchestrator_intents
    loaded = ["math-modeling", f"role:{role}", *specialists]
    if load_orchestrator and "modeling-pipeline-orchestrator" not in specialists:
        loaded.append("modeling-pipeline-orchestrator")
    return {
        "query": query,
        "intent": intent,
        "role": role,
        "specialists": specialists,
        "loaded": loaded,
        "load_orchestrator": load_orchestrator,
        "load_stage_registry": load_orchestrator,
        "persist_artifacts": bool(spec.get("persist_artifacts", False)),
        "never_preload": never_preload,
        "note": "Load only these capabilities this turn. Do not open the stage registry unless load_stage_registry is true.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Current user utterance")
    parser.add_argument("--current-role", choices=["modeler", "computationalist", "writer"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    plan = route_query(args.query, current_role=args.current_role)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    print(f"INTENT: {plan['intent']}")
    print(f"ROLE: {plan['role']}")
    print(f"SPECIALISTS: {', '.join(plan['specialists']) or '-'}")
    print(f"LOAD_ORCHESTRATOR: {plan['load_orchestrator']}")
    print(f"LOAD_STAGE_REGISTRY: {plan['load_stage_registry']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
