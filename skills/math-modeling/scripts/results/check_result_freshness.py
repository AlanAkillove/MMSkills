#!/usr/bin/env python3
"""Fail if a frozen result's source file hash no longer matches."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from freeze_results import sha256_file


def check_freshness(snapshot_path: Path, source: Path | None = None) -> list[str]:
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    source_path = source or Path(snapshot["source_file"])
    errors: list[str] = []
    if not source_path.is_file():
        return [f"source missing: {source_path}"]
    current = sha256_file(source_path)
    expected = snapshot.get("source_hash")
    if current != expected:
        errors.append(
            f"stale snapshot for {snapshot.get('claim_id')}: source hash changed "
            f"({expected} -> {current})"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    errors = check_freshness(args.snapshot, args.source)
    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    print("OK: snapshot is fresh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
