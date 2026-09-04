#!/usr/bin/env python3
"""Flag manuscript tokens that contradict an established terminology table.

This is a mechanical drift scanner, not a decision to invent or replace canonical terms.
OK does not mean the manuscript has no invented terminology, high-commitment words, or concept-level drift.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WRAP_PATTERNS = (
    r"多尺度协同",
    r"动态耦合效应",
    r"综合调控指数",
    r"synergistic effect",
    r"multi-scale flow imbalance",
)


def _cells(line: str) -> list[str]:
    parts = [part.strip() for part in line.strip().strip("|").split("|")]
    return parts


def parse_concept_rows(table_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_concepts = False
    header: list[str] = []
    for line in table_text.splitlines():
        if line.startswith("## Concepts"):
            in_concepts = True
            header = []
            continue
        if in_concepts and line.startswith("## "):
            break
        if not in_concepts or not line.startswith("|"):
            continue
        cells = _cells(line)
        if set("".join(cells)) <= set("-: "):
            continue
        if not header:
            header = cells
            continue
        record = {header[i]: cells[i] if i < len(cells) else "" for i in range(len(header))}
        rows.append(record)
    return rows


def scan(table_text: str, manuscript: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for row in parse_concept_rows(table_text):
        forbidden = [
            item.strip()
            for item in re.split(r"[;；,/]", row.get("ambiguous_or_deprecated") or "")
            if item.strip()
        ]
        for alias in forbidden:
            if alias and alias in manuscript:
                findings.append(
                    {
                        "kind": "deprecated-or-ambiguous-alias",
                        "term": alias,
                        "canonical": row.get("en_canonical") or row.get("zh_canonical") or "",
                    }
                )
    for pattern in WRAP_PATTERNS:
        if re.search(pattern, manuscript, flags=re.I):
            if not any(pattern.lower() in (row.get("en_canonical") or "").lower() or pattern in (row.get("zh_canonical") or "") for row in parse_concept_rows(table_text)):
                findings.append({"kind": "unregistered-wrapper", "term": pattern})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", type=Path, required=True)
    parser.add_argument("--manuscript", type=Path, required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    findings = scan(args.table.read_text(encoding="utf-8"), args.manuscript.read_text(encoding="utf-8"))
    if args.json_out:
        args.json_out.write_text(json.dumps(findings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if findings:
        for item in findings:
            print(f"DRIFT: {item['kind']}: {item['term']}")
        return 1
    print("OK: no mechanical terminology drift")
    print("NOTE: this is an alias/wrapper scan only; it is not a semantic invented-term audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
