#!/usr/bin/env python3
"""Fail if a results snapshot's source file hash no longer matches."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from freeze_results import claims_from_payload, sha256_file


def resolve_source(
    raw: str,
    *,
    snapshot_path: Path,
    repo_root: Path | None,
    override: Path | None,
) -> Path:
    if override is not None:
        return override
    path = Path(raw)
    if path.is_file():
        return path
    candidates: list[Path] = []
    if repo_root is not None:
        candidates.append(repo_root / raw)
    candidates.append(snapshot_path.parent / raw)
    candidates.append(Path.cwd() / raw)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return path


def check_freshness(
    snapshot_path: Path,
    source: Path | None = None,
    repo_root: Path | None = None,
) -> list[str]:
    payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
    claims = claims_from_payload(payload)
    if not claims:
        return ["snapshot has no claims"]
    errors: list[str] = []
    for claim in claims:
        source_path = resolve_source(
            str(claim.get("source_file") or ""),
            snapshot_path=snapshot_path,
            repo_root=repo_root,
            override=source,
        )
        if not source_path.is_file():
            errors.append(f"source missing: {source_path}")
            continue
        current = sha256_file(source_path)
        expected = claim.get("source_hash")
        if current != expected:
            errors.append(
                f"stale snapshot for {claim.get('claim_id')}: source hash changed "
                f"({expected} -> {current})"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()
    errors = check_freshness(args.snapshot, args.source, args.repo_root or Path.cwd())
    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    print("OK: snapshot is fresh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
