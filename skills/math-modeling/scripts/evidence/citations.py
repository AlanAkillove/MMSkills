#!/usr/bin/env python3
"""Local citation helpers: normalize DOI, deduplicate, compare claimed vs fetched metadata.

Search is discovery only. This script never fetches the web; it only checks records
the caller already obtained from a publication page or PDF.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DOI_PREFIXES = (
    "https://doi.org/",
    "http://doi.org/",
    "https://dx.doi.org/",
    "http://dx.doi.org/",
    "doi:",
)


def normalize_doi(value: str) -> str:
    text = (value or "").strip()
    lowered = text.lower()
    for prefix in DOI_PREFIXES:
        if lowered.startswith(prefix):
            text = text[len(prefix) :]
            break
    return text.strip().rstrip(".").lower()


def _norm_title(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def compare_records(claimed: dict[str, Any], fetched: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    claimed_doi = normalize_doi(str(claimed.get("doi") or ""))
    fetched_doi = normalize_doi(str(fetched.get("doi") or ""))
    if not claimed_doi or not fetched_doi:
        errors.append("DOI missing; keep as unverified candidate")
    elif claimed_doi != fetched_doi:
        errors.append(f"DOI mismatch: {claimed_doi} != {fetched_doi}")
    claimed_title = _norm_title(claimed.get("title"))
    fetched_title = _norm_title(fetched.get("title"))
    if claimed_title and fetched_title and claimed_title != fetched_title:
        errors.append("title mismatch")
    claimed_year = str(claimed.get("year") or "").strip()
    fetched_year = str(fetched.get("year") or "").strip()
    if claimed_year and fetched_year and claimed_year != fetched_year:
        errors.append("year mismatch")
    return errors


def deduplicate(records: list[dict[str, Any]]) -> list[list[str]]:
    groups: dict[str, list[str]] = {}
    for index, record in enumerate(records):
        key = normalize_doi(str(record.get("doi") or "")) or f"noid:{index}"
        label = str(record.get("id") or record.get("title") or index)
        groups.setdefault(key, []).append(label)
    return [labels for key, labels in groups.items() if len(labels) > 1 and not key.startswith("noid:")]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    doi_cmd = sub.add_parser("normalize-doi")
    doi_cmd.add_argument("value")
    compare_cmd = sub.add_parser("compare")
    compare_cmd.add_argument("--claimed", type=Path, required=True)
    compare_cmd.add_argument("--fetched", type=Path, required=True)
    dup_cmd = sub.add_parser("dedupe")
    dup_cmd.add_argument("--records", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "normalize-doi":
        print(normalize_doi(args.value))
        return 0
    if args.command == "compare":
        claimed = json.loads(args.claimed.read_text(encoding="utf-8"))
        fetched = json.loads(args.fetched.read_text(encoding="utf-8"))
        errors = compare_records(claimed, fetched)
        if errors:
            for item in errors:
                print(f"ERROR: {item}")
            return 1
        print("OK: citation fields match")
        return 0
    records = json.loads(args.records.read_text(encoding="utf-8"))
    duplicates = deduplicate(records)
    if duplicates:
        print(json.dumps(duplicates, ensure_ascii=False))
        return 1
    print("OK: no DOI duplicates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
