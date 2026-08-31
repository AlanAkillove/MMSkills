#!/usr/bin/env python3
"""Merge cross-review JSONL findings without silently discarding conflicts."""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]
FINDING_SCHEMA_PATH = ROOT / "schemas" / "finding.schema.json"
SEVERITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
CLOSED_STATUS = {"resolved", "rejected", "superseded"}
OPEN_STATUS = {"open", "needs_human", "confirmed", "unknown"}
TERMINAL_HUMAN = {"human-confirmed", "rejected"}


def load_finding_validator() -> Draft202012Validator:
    schema = json.loads(FINDING_SCHEMA_PATH.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def read_jsonl(path: Path, validator: Draft202012Validator) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number}: finding must be an object")
        schema_errors = list(validator.iter_errors(record))
        if schema_errors:
            raise ValueError(f"{path}:{line_number}: schema {schema_errors[0].message}")
        dedup = record["deduplication"]
        if not isinstance(dedup, dict) or not dedup.get("canonical_issue_key"):
            raise ValueError(f"{path}:{line_number}: missing canonical_issue_key")
        record["_source_path"] = path.as_posix()
        records.append(record)
    return records


def anchor_ids(record: Dict[str, Any]) -> List[str]:
    ids: List[str] = []
    for anchor in record.get("evidence_anchors") or []:
        if isinstance(anchor, dict):
            ids.append(str(anchor.get("anchor_id") or anchor.get("locator") or "unknown"))
        else:
            ids.append(str(anchor))
    return ids


def union_anchors(records: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    for record in records:
        for anchor in record.get("evidence_anchors") or []:
            if not isinstance(anchor, dict):
                key = str(anchor)
                merged.setdefault(key, {"anchor_id": key, "locator": key, "evidence_status": "unknown"})
                continue
            key = str(anchor.get("anchor_id") or anchor.get("locator") or f"anon-{len(merged)}")
            existing = merged.get(key)
            if existing is None:
                merged[key] = dict(anchor)
                continue
            if existing.get("evidence_status") != anchor.get("evidence_status"):
                existing["evidence_status"] = "conflict"
            if not existing.get("excerpt") and anchor.get("excerpt"):
                existing["excerpt"] = anchor["excerpt"]
            if not existing.get("locator") and anchor.get("locator"):
                existing["locator"] = anchor["locator"]
    return list(merged.values())


def union_ids(records: Sequence[Dict[str, Any]], field: str) -> List[str]:
    values: "OrderedDict[str, None]" = OrderedDict()
    for record in records:
        for item in record.get(field) or []:
            values[str(item)] = None
    return list(values)


def classify_group(group: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    severities = sorted({str(item["severity"]) for item in group})
    statuses = sorted({str(item["status"]) for item in group})
    human_statuses = sorted({str(item["human_status"]) for item in group})
    acceptance_tests = [str(item["acceptance_test"]) for item in group]
    relations = sorted({str(item["deduplication"].get("relation", "unknown")) for item in group})
    skills = sorted({str(item["source_skill"]) for item in group})
    anchor_sets = {tuple(sorted(anchor_ids(item))) for item in group}

    status_conflict = bool(set(statuses) & CLOSED_STATUS) and bool(set(statuses) & OPEN_STATUS)
    human_conflict = len(set(human_statuses)) > 1 and bool(set(human_statuses) & TERMINAL_HUMAN)
    explicit_conflict = "conflict" in relations
    severity_conflict = len(severities) > 1
    conflict = status_conflict or human_conflict or explicit_conflict

    if conflict:
        relation = "conflict"
        action = "human_review_required"
    elif severity_conflict:
        first_rank = SEVERITY_RANK.get(str(group[0]["severity"]), 99)
        worst_rank = min(SEVERITY_RANK.get(item, 99) for item in severities)
        relation = "upgrade" if worst_rank < first_rank else "downgrade"
        action = "human_review_required"
    elif len(group) == 1:
        relation = "new"
        action = "kept"
    elif len(anchor_sets) > 1 or len(skills) > 1:
        relation = "supplement"
        action = "supplement_merged"
    else:
        relation = "duplicate"
        action = "duplicate_collapsed"

    return {
        "relation": relation,
        "action": action,
        "conflict": conflict or severity_conflict,
        "severities": severities,
        "statuses": statuses,
        "human_statuses": human_statuses,
        "acceptance_tests": list(dict.fromkeys(acceptance_tests)),
        "relations": relations,
        "source_skills": skills,
        "status_conflict": status_conflict,
        "human_status_conflict": human_conflict,
        "severity_conflict": severity_conflict,
        "acceptance_test_conflict": len(set(acceptance_tests)) > 1,
    }


def most_severe(severities: Sequence[str]) -> str:
    return sorted(severities, key=lambda item: SEVERITY_RANK.get(item, 99))[0]


def merge_group(issue_key: str, group: Sequence[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    classification = classify_group(group)
    first = dict(group[0])
    source_ids = [str(item["finding_id"]) for item in group]
    anchors = union_anchors(group)
    observations = [str(item["observation"]) for item in group]
    notes = [str(item.get("notes", "")).strip() for item in group if str(item.get("notes", "")).strip()]
    if classification["acceptance_test_conflict"]:
        notes.append("验收标准不一致，已保留全部 acceptance_test，不能静默覆盖。")
    if classification["status_conflict"]:
        notes.append("status 在 resolved/open 之间冲突，不能采用首条记录的关闭状态。")
    if classification["human_status_conflict"]:
        notes.append("human_status 冲突，需人工确认。")
    if classification["severity_conflict"]:
        notes.append("severity 不一致，canonical 取更严重级别并等待人工确认。")

    dedup = dict(first["deduplication"])
    dedup.update(
        {
            "canonical_issue_key": issue_key,
            "canonical_finding_id": str(first["finding_id"]),
            "relation": classification["relation"],
            "source_record_ids": source_ids,
        }
    )
    first["deduplication"] = dedup
    first["evidence_anchors"] = anchors
    first["related_finding_ids"] = sorted(set(union_ids(group, "related_finding_ids") + source_ids[1:]))
    first["related_claim_ids"] = union_ids(group, "related_claim_ids")
    first["related_term_ids"] = union_ids(group, "related_term_ids")
    first["related_figure_ids"] = union_ids(group, "related_figure_ids")
    first["source_skills"] = classification["source_skills"]
    first["source_record_count"] = len(group)
    first["source_observations"] = observations
    first["acceptance_tests"] = classification["acceptance_tests"]
    if classification["acceptance_tests"]:
        first["acceptance_test"] = classification["acceptance_tests"][0]
    if classification["severity_conflict"]:
        first["severity"] = most_severe(classification["severities"])
    if classification["conflict"]:
        first["status"] = "needs_human"
        first["human_status"] = "needs-human-confirmation"
    first["notes"] = " ".join(dict.fromkeys(notes)).strip()
    first.pop("_source_path", None)
    report = {
        "canonical_issue_key": issue_key,
        "anchor_ids": [str(anchor.get("anchor_id")) for anchor in anchors],
        "source_record_ids": source_ids,
        "source_skills": classification["source_skills"],
        "severities": classification["severities"],
        "statuses": classification["statuses"],
        "human_statuses": classification["human_statuses"],
        "relations": classification["relations"],
        "acceptance_tests": classification["acceptance_tests"],
        "action": classification["action"],
        "source_paths": sorted({str(item["_source_path"]) for item in group}),
    }
    return first, report


def merge_records(records: Iterable[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    groups: "OrderedDict[str, List[Dict[str, Any]]]" = OrderedDict()
    for record in records:
        issue_key = str(record["deduplication"]["canonical_issue_key"])
        groups.setdefault(issue_key, []).append(record)

    merged: List[Dict[str, Any]] = []
    report_groups: List[Dict[str, Any]] = []
    for issue_key, group in groups.items():
        record, report = merge_group(issue_key, group)
        merged.append(record)
        report_groups.append(report)
    return merged, {
        "group_count": len(groups),
        "input_record_count": sum(len(group) for group in groups.values()),
        "grouping_key": "canonical_issue_key",
        "groups": report_groups,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", required=True, type=Path, help="finding JSONL; repeat for each report")
    parser.add_argument("--output", required=True, type=Path, help="canonical finding register JSONL")
    parser.add_argument("--report", required=True, type=Path, help="merge report JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        validator = load_finding_validator()
        records = [record for path in args.input for record in read_jsonl(path, validator)]
        merged, report = merge_records(records)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="\n") as handle:
            for record in merged:
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"WROTE: {args.output}")
    print(f"GROUPS: {report['group_count']}")
    print(f"INPUT_FINDINGS: {report['input_record_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
