#!/usr/bin/env python3
"""Validate structured AI-use disclosure input and, optionally, its PDF text."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_TOP_LEVEL = (
    "profile_id",
    "status",
    "record_completeness",
    "scope",
    "tools",
    "events",
    "human_control",
    "confirmation",
)
REQUIRED_EVENT = (
    "event_id",
    "event_family",
    "stage",
    "purpose",
    "adoption",
    "human_modification",
    "human_verification",
    "evidence_level",
    "record_status",
)
PLACEHOLDER_RE = re.compile(r"(?:TODO|TBD|replace[-_ ]?me|\{\{|\}\}|<insert|待填写)", re.I)
SECRET_RE = re.compile(r"(?:sk-[A-Za-z0-9]{12,}|AKIA[0-9A-Z]{16}|-----BEGIN .* PRIVATE KEY-----)")


def read_json(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return data


def is_unknown(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in {"", "unknown", "未确认"})


def flatten(value: Any) -> List[str]:
    if isinstance(value, dict):
        result: List[str] = []
        for key, item in value.items():
            result.append(str(key))
            result.extend(flatten(item))
        return result
    if isinstance(value, list):
        result: List[str] = []
        for item in value:
            result.extend(flatten(item))
        return result
    return [str(value)]


def validate(data: Dict[str, Any], final: bool) -> List[str]:
    errors: List[str] = []
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"missing top-level field: {key}")

    status = data.get("status")
    allowed_status = {"draft", "human-confirmed", "final"}
    if status not in allowed_status:
        errors.append(f"invalid status: {status!r}")
    if data.get("record_completeness") not in {"complete", "partial", "unknown"}:
        errors.append("record_completeness must be complete, partial, or unknown")
    if not isinstance(data.get("tools"), list):
        errors.append("tools must be a list")
    if not isinstance(data.get("events"), list):
        errors.append("events must be a list")

    confirmation = data.get("confirmation")
    if not isinstance(confirmation, dict):
        errors.append("confirmation must be an object")
        confirmation = {}
    if confirmation.get("status") not in {"pending", "confirmed", "rejected", "not_available"}:
        errors.append("confirmation.status is invalid")

    event_ids = set()
    for index, event in enumerate(data.get("events", []), start=1):
        if not isinstance(event, dict):
            errors.append(f"event {index} must be an object")
            continue
        for key in REQUIRED_EVENT:
            if key not in event:
                errors.append(f"event {index} missing field: {key}")
        event_id = event.get("event_id")
        if event_id in event_ids:
            errors.append(f"duplicate event_id: {event_id}")
        event_ids.add(event_id)
        if event.get("evidence_level") not in {"E3", "E2", "E1", "E0"}:
            errors.append(f"event {index} has invalid evidence_level")
        if event.get("record_status") not in {"confirmed", "proposed", "partial_history", "conflict", "unknown", "privacy_blocked"}:
            errors.append(f"event {index} has invalid record_status")
        if event.get("adoption") not in {
            "not_adopted", "partially_adopted", "adopted_after_edit", "adopted_as_is", "unclear", "not_applicable"
        }:
            errors.append(f"event {index} has invalid adoption")
        if final:
            for key in ("stage", "purpose", "human_modification", "human_verification", "evidence_level", "record_status"):
                if is_unknown(event.get(key)):
                    errors.append(f"final event {event.get('event_id', index)} has unknown {key}")
            if event.get("record_status") != "confirmed":
                errors.append(f"final event {event.get('event_id', index)} is not confirmed")
            if not event.get("source_ids") and is_unknown(event.get("source_locator")):
                errors.append(f"final event {event.get('event_id', index)} has no source locator")

    all_text = "\n".join(flatten(data))
    if PLACEHOLDER_RE.search(all_text):
        errors.append("placeholder text detected")
    if SECRET_RE.search(all_text):
        errors.append("possible secret or private key detected")

    if final:
        tools = data.get("tools", [])
        if data.get("events") and not tools:
            errors.append("final disclosure has events but no tool record")
        for tool_index, tool in enumerate(tools, start=1):
            if not isinstance(tool, dict):
                errors.append(f"final tool {tool_index} must be an object")
                continue
            for key in data.get("required_tool_fields", ["name", "version_or_model"]):
                if is_unknown(tool.get(key)):
                    errors.append(f"final tool {tool_index} has unknown {key}")
        if status not in {"human-confirmed", "final"}:
            errors.append("final validation requires status=human-confirmed or final")
        if confirmation.get("status") != "confirmed":
            errors.append("final validation requires confirmation.status=confirmed")
        for key in ("person", "date", "decision_id"):
            if is_unknown(confirmation.get(key)):
                errors.append(f"final confirmation missing {key}")
        if data.get("record_completeness") != "complete":
            errors.append("final validation requires record_completeness=complete")
        if data.get("render_status") not in {"passed", "checked"}:
            errors.append("final validation requires render_status=passed or checked")
        for item in data.get("unknowns", []) or []:
            if isinstance(item, dict) and item.get("blocking") is True:
                errors.append("blocking unknown remains")
    return errors


def validate_pdf(pdf_path: Path, final: bool) -> List[str]:
    errors: List[str] = []
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - depends on runtime bundle
        return [f"pypdf is required for PDF validation: {exc}"]
    try:
        reader = PdfReader(str(pdf_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:  # pragma: no cover - parser implementation detail
        return [f"cannot read PDF: {exc}"]
    if "AI" not in text and "AI 工具使用详情" not in text:
        errors.append("PDF title/status text not found")
    if final:
        if "最终版" not in text or "已人工确认" not in text:
            errors.append("final PDF confirmation banner not found")
    else:
        if "草稿" not in text or "待人工确认" not in text:
            errors.append("draft PDF status banner not found")
    if PLACEHOLDER_RE.search(text):
        errors.append("placeholder text detected in PDF")
    if SECRET_RE.search(text):
        errors.append("possible secret or private key detected in PDF")
    if not reader.pages:
        errors.append("PDF has no pages")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--final", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = read_json(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 2
    errors = validate(data, args.final)
    if args.pdf:
        errors.extend(validate_pdf(args.pdf, args.final))
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
