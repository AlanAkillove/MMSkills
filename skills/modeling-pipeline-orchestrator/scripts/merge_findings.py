#!/usr/bin/env python3
"""Merge cross-review JSONL findings without silently discarding conflicts."""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


REQUIRED = {
    "finding_id",
    "source_skill",
    "finding_type",
    "severity",
    "status",
    "observation",
    "evidence_anchors",
    "impact",
    "acceptance_test",
    "deduplication",
    "human_status",
}


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
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
        missing = sorted(REQUIRED - set(record))
        if missing:
            raise ValueError(f"{path}:{line_number}: missing finding fields: {', '.join(missing)}")
        dedup = record["deduplication"]
        if not isinstance(dedup, dict) or not dedup.get("canonical_issue_key"):
            raise ValueError(f"{path}:{line_number}: missing canonical_issue_key")
        record["_source_path"] = path.as_posix()
        records.append(record)
    return records


def anchor_key(record: Dict[str, Any]) -> Tuple[str, Tuple[str, ...]]:
    dedup = record["deduplication"]
    issue_key = str(dedup["canonical_issue_key"])
    anchors = record.get("evidence_anchors", [])
    anchor_ids = []
    for anchor in anchors:
        if isinstance(anchor, dict):
            anchor_ids.append(str(anchor.get("anchor_id") or anchor.get("locator") or "unknown"))
        else:
            anchor_ids.append(str(anchor))
    return issue_key, tuple(sorted(anchor_ids))


def merge_records(records: Iterable[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    groups: "OrderedDict[Tuple[str, Tuple[str, ...]], List[Dict[str, Any]]]" = OrderedDict()
    for record in records:
        groups.setdefault(anchor_key(record), []).append(record)

    merged: List[Dict[str, Any]] = []
    report_groups: List[Dict[str, Any]] = []
    for group_key, group in groups.items():
        first = dict(group[0])
        source_ids = [str(item["finding_id"]) for item in group]
        source_skills = sorted({str(item["source_skill"]) for item in group})
        severities = sorted({str(item["severity"]) for item in group})
        statuses = sorted({str(item["status"]) for item in group})
        relations = sorted({str(item["deduplication"].get("relation", "unknown")) for item in group})
        conflict = len(severities) > 1 or "conflict" in relations
        dedup = dict(first["deduplication"])
        dedup.update(
            {
                "canonical_finding_id": str(first["finding_id"]),
                "relation": "conflict" if conflict else ("supplement" if len(group) > 1 else "new"),
                "source_record_ids": source_ids,
            }
        )
        first["deduplication"] = dedup
        first["related_finding_ids"] = sorted(
            set(first.get("related_finding_ids", [])) | set(source_ids[1:])
        )
        first["source_skills"] = source_skills
        first["source_record_count"] = len(group)
        if conflict:
            first["status"] = "needs_human"
            first["human_status"] = "needs-human-confirmation"
            first["notes"] = (str(first.get("notes", "")).rstrip() + " 严重性/关系存在跨审查冲突，需人工确认。").strip()
        first.pop("_source_path", None)
        merged.append(first)
        report_groups.append(
            {
                "canonical_issue_key": group_key[0],
                "anchor_ids": list(group_key[1]),
                "source_record_ids": source_ids,
                "source_skills": source_skills,
                "severities": severities,
                "statuses": statuses,
                "relations": relations,
                "action": "human_review_required" if conflict else ("supplement_merged" if len(group) > 1 else "kept"),
                "source_paths": sorted({str(item["_source_path"]) for item in group}),
            }
        )
    return merged, {"group_count": len(groups), "input_record_count": sum(len(group) for group in groups.values()), "groups": report_groups}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", action="append", required=True, type=Path, help="finding JSONL; repeat for each report")
    parser.add_argument("--output", required=True, type=Path, help="canonical finding register JSONL")
    parser.add_argument("--report", required=True, type=Path, help="merge report JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        records = [record for path in args.input for record in read_jsonl(path)]
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
