#!/usr/bin/env python3
"""High-confidence role hint for the current turn. This is not a workflow engine
and not a keyword classifier that guesses a role when context is missing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


ROOT = Path(__file__).resolve().parents[3]
ROUTING_PATH = Path(__file__).resolve().parents[1] / "references" / "specialist-routing.yaml"

from route_capabilities import (  # noqa: E402
    merge_specialists,
    retrieve_capabilities,
    should_expand,
)

# (intent, pattern, default_confidence)
INTENT_PATTERNS: List[Tuple[str, re.Pattern[str], str]] = [
    ("resume", re.compile(r"恢复会话|跨会话|handoff|process-freezer|续接上次", re.I), "high"),
    ("full_audit", re.compile(r"全流程审计|完整审查|full audit", re.I), "high"),
    ("submission_plan", re.compile(r"提交计划|安排提交|submission plan", re.I), "high"),
    ("diagnose_state", re.compile(r"项目状态诊断|stage registry|pipeline plan", re.I), "high"),
    ("disclose", re.compile(r"AI\s*披露|使用详情\.pdf|disclosure", re.I), "high"),
    ("preflight", re.compile(r"提交前|终检|preflight", re.I), "high"),
    (
        "composite_review",
        re.compile(
            r"(写作质量|论文结构|语言表达|术语规范|格式规范).{0,80}(审阅|审查|审稿)"
            r"|(审阅|审查|审稿).{0,80}(写作质量|论文结构|语言表达|术语规范|格式规范|多个方面)"
            r"|多个方面进行审阅",
            re.I,
        ),
        "high",
    ),
    ("review", re.compile(r"最终审稿|成稿审阅|审阅论文|预审论文|投稿前自审", re.I), "high"),
    ("formal_intake", re.compile(r"问题地图|正式题意|固化题意|整理成正式问题", re.I), "high"),
    ("terminology_audit", re.compile(r"术语漂移|术语审查|terminology drift", re.I), "high"),
    ("terminology_establish", re.compile(r"术语表|统一叫|canonical term|terminology_table", re.I), "high"),
    (
        "model_from_literature",
        re.compile(
            r"(根据|结合|基于).{0,30}(这些|这几篇|已读|上述)?(论文|文献).{0,30}"
            r"(推模型|建模|设计模型|比较模型|继续.{0,12}模型)",
            re.I,
        ),
        "high",
    ),
    ("model", re.compile(r"比较.*模型|候选模型|模型设计|采用这个模型|继续.*模型|推模型", re.I), "high"),
    ("revise", re.compile(r"重写摘要|改摘要|续写|自然化|精修\s*\d|5\.3|章节", re.I), "high"),
    ("draft", re.compile(r"写论文|正文|摘要|draft", re.I), "medium"),
    ("literature", re.compile(r"文献|相关工作|论文检索|相关论文|这几篇论文|DOI|orientation", re.I), "medium"),
    ("figure", re.compile(r"画图|绘图|figure|plot", re.I), "medium"),
    ("figure_inspect", re.compile(r"检查图|修改图", re.I), "low"),
    ("experiment", re.compile(r"实验|跑代码|求解|python|matlab", re.I), "medium"),
    ("numeric_ambiguous", re.compile(r"数值", re.I), "low"),
    (
        "understand",
        re.compile(r"让我理解|帮我理解|理解主要内容|弄懂|熟悉题目|阅读赛题|机理|题意|familiar", re.I),
        "medium",
    ),
    ("continue_local", re.compile(r"继续问题|接着(写|做|算)|continue (question|q)\s*\d+", re.I), "low"),
]

# Intents that cross roles. Do not guess modeler/computationalist/writer.
CONTEXT_REQUIRED_INTENTS = {"continue_local", "figure_inspect", "numeric_ambiguous"}


def load_routing(path: Path = ROUTING_PATH) -> Dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("specialist-routing.yaml must be an object")
    return payload


def classify_intent(query: str) -> Tuple[str, str, str]:
    """Return (intent, matched_rule, confidence). Empty/unmatched is continue_local."""
    text = query.strip()
    if not text:
        return "continue_local", "empty_query", "low"
    for intent, pattern, confidence in INTENT_PATTERNS:
        if pattern.search(text):
            return intent, intent, confidence
    return "continue_local", "unmatched", "low"


def _as_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def route_query(
    query: str,
    *,
    current_role: Optional[str] = None,
    routing: Optional[Dict[str, Any]] = None,
    working_set: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    routing = routing or load_routing()
    intent, matched_rule, confidence = classify_intent(query)
    spec = (routing.get("intents") or {}).get(intent) or {}
    requires_context = bool(spec.get("requires_context")) or intent in CONTEXT_REQUIRED_INTENTS
    declared_role = spec.get("role") or "inherit"
    if declared_role == "inherit" or (requires_context and not current_role):
        if current_role:
            role = current_role
            if requires_context:
                confidence = "medium"
            requires_context = False
        else:
            role = "unknown"
            confidence = "low"
            requires_context = True
            declared_role = "inherit"
    else:
        role = declared_role
    specialists = _as_list(spec.get("specialists"))
    if role == "unknown":
        specialists = []
    orchestrator_intents = set(_as_list(routing.get("orchestrator_intents")))
    never_preload = _as_list(routing.get("never_preload"))
    load_orchestrator = intent in orchestrator_intents
    loaded = ["math-modeling"]
    if role != "unknown":
        loaded.append(f"role:{role}")
    loaded.extend(specialists)
    if load_orchestrator and "modeling-pipeline-orchestrator" not in specialists:
        loaded.append("modeling-pipeline-orchestrator")
    review_isolation = spec.get("review_isolation")
    retrieval = retrieve_capabilities(
        query,
        role=None if role in {"unknown", "cross_cutting"} else role,
        intent=intent,
        working_set=working_set,
    )
    if (
        role == "unknown"
        and intent == "continue_local"
        and retrieval.get("implied_role")
        and retrieval.get("specialists")
        and not retrieval.get("working_set", {}).get("hit")
    ):
        role = retrieval["implied_role"]
        specialists = list(retrieval.get("specialists") or [])
        requires_context = False
        confidence = "medium"
        loaded = ["math-modeling", f"role:{role}"]
        loaded.extend(specialists)
    elif should_expand(intent, retrieval, specialists):
        specialists = merge_specialists(specialists, retrieval.get("specialists") or [])
        loaded = ["math-modeling"]
        if role != "unknown":
            loaded.append(f"role:{role}")
        loaded.extend(specialists)
        if load_orchestrator and "modeling-pipeline-orchestrator" not in specialists:
            loaded.append("modeling-pipeline-orchestrator")
    if not review_isolation and "modeling-paper-reviewer" in specialists:
        review_isolation = "required_subagent"
    return {
        "query": query,
        "intent": intent,
        "role": role,
        "specialists": specialists,
        "loaded": loaded,
        "load_orchestrator": load_orchestrator,
        "load_stage_registry": load_orchestrator,
        "persist_artifacts": bool(spec.get("persist_artifacts", False)),
        "review_isolation": review_isolation,
        "never_preload": never_preload,
        "confidence": confidence,
        "matched_rule": matched_rule,
        "requires_context": requires_context,
        "task_facets": retrieval.get("task_facets") or [],
        "capability_candidates": retrieval.get("candidates") or [],
        "mandatory_consideration": retrieval.get("mandatory_consideration") or [],
        "working_set": retrieval.get("working_set") or {"hit": False, "reason": "absent"},
        "note": (
            "High-confidence hint only. unknown means this script cannot judge; "
            "use the explicit intent, then recent conversation and current artifact, "
            "then current_role; ask the user only if those still fail. "
            "Do not default to modeler. Do not open the stage registry unless "
            "load_stage_registry is true. Ordinary single tasks load 0-2 specialists; "
            "composite tasks use capability coverage with no fixed specialist cap. "
            "L1.5 recalls candidates; full SKILL.md is precision. "
            "Final review requires an independent subagent."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Current user utterance")
    parser.add_argument("--current-role", choices=["modeler", "computationalist", "writer"])
    parser.add_argument("--working-set", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    working_set = None
    if args.working_set:
        working_set = yaml.safe_load(args.working_set.read_text(encoding="utf-8"))
    plan = route_query(args.query, current_role=args.current_role, working_set=working_set)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    print(f"INTENT: {plan['intent']}")
    print(f"ROLE: {plan['role']}")
    print(f"CONFIDENCE: {plan['confidence']}")
    print(f"MATCHED_RULE: {plan['matched_rule']}")
    print(f"REQUIRES_CONTEXT: {plan['requires_context']}")
    print(f"FACETS: {', '.join(plan.get('task_facets') or []) or '-'}")
    print(f"SPECIALISTS: {', '.join(plan['specialists']) or '-'}")
    print(f"MANDATORY_CONSIDERATION: {', '.join(plan.get('mandatory_consideration') or []) or '-'}")
    print(f"REVIEW_ISOLATION: {plan.get('review_isolation') or '-'}")
    print(f"PERSIST_ARTIFACTS: {plan['persist_artifacts']}")
    print(f"LOAD_ORCHESTRATOR: {plan['load_orchestrator']}")
    print(f"LOAD_STAGE_REGISTRY: {plan['load_stage_registry']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
