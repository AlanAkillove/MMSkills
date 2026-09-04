#!/usr/bin/env python3
"""Freeze a scalar result with source file hash. Exploration runs should not call this."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def lookup(payload: Any, locator: str) -> Any:
    if locator.startswith("$."):
        current = payload
        for part in locator[2:].split("."):
            if not isinstance(current, dict) or part not in current:
                raise KeyError(locator)
            current = current[part]
        return current
    raise ValueError("locator must look like $.path.to.field")


def freeze(
    source: Path,
    *,
    locator: str,
    claim_id: str,
    unit: str,
    scope: str,
) -> dict[str, Any]:
    payload = json.loads(source.read_text(encoding="utf-8"))
    value = lookup(payload, locator)
    return {
        "claim_id": claim_id,
        "value": value,
        "unit": unit,
        "source_file": str(source).replace("\\", "/"),
        "source_locator": locator,
        "source_hash": sha256_file(source),
        "frozen_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": scope,
        "status": "frozen",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--locator", required=True)
    parser.add_argument("--claim-id", required=True)
    parser.add_argument("--unit", default="")
    parser.add_argument("--scope", default="unknown")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    snapshot = freeze(
        args.source,
        locator=args.locator,
        claim_id=args.claim_id,
        unit=args.unit,
        scope=args.scope,
    )
    args.output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
