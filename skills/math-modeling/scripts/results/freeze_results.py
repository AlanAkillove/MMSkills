#!/usr/bin/env python3
"""Record a mechanical results snapshot. Status is snapshot until a human freeze
decision_id is supplied; this script must not bypass the action gate.
"""

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


def project_relative(path: Path, repo_root: Path, *, allow_external: bool = False) -> str:
    resolved = path.resolve()
    root = repo_root.resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        if allow_external:
            return resolved.as_posix()
        raise ValueError(
            f"source is outside repo root ({root.as_posix()}); "
            "pass --allow-external-source to record an absolute path"
        ) from exc


def claims_from_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(payload.get("claims"), list):
        return [item for item in payload["claims"] if isinstance(item, dict)]
    if payload.get("claim_id"):
        return [payload]
    return []


def load_snapshot(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema": "results_snapshot", "claims": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("snapshot must be a JSON object")
    return {"schema": "results_snapshot", "claims": claims_from_payload(payload)}


def upsert_claim(snapshot: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    claims = snapshot.setdefault("claims", [])
    claim_id = claim.get("claim_id")
    for index, existing in enumerate(claims):
        if existing.get("claim_id") == claim_id:
            claims[index] = claim
            return snapshot
    claims.append(claim)
    return snapshot


def freeze_claim(
    source: Path,
    *,
    locator: str,
    claim_id: str,
    unit: str,
    scope: str,
    repo_root: Path,
    status: str,
    human_status: str,
    decision_id: str | None,
    allow_external: bool = False,
) -> dict[str, Any]:
    payload = json.loads(source.read_text(encoding="utf-8"))
    value = lookup(payload, locator)
    recorded_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    claim: dict[str, Any] = {
        "claim_id": claim_id,
        "value": value,
        "unit": unit,
        "source_file": project_relative(source, repo_root, allow_external=allow_external),
        "source_locator": locator,
        "source_hash": sha256_file(source),
        "recorded_at": recorded_at,
        "scope": scope,
        "status": status,
        "human_status": human_status,
        "decision_id": decision_id,
    }
    if status == "frozen":
        claim["frozen_at"] = recorded_at
    return claim


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--locator", required=True)
    parser.add_argument("--claim-id", required=True)
    parser.add_argument("--unit", default="")
    parser.add_argument("--scope", default="unknown")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--status", choices=["snapshot", "frozen"], default="snapshot")
    parser.add_argument("--decision-id", default=None)
    parser.add_argument(
        "--human-status",
        choices=["unreviewed", "confirmed"],
        default=None,
    )
    parser.add_argument(
        "--allow-external-source",
        action="store_true",
        help="Allow recording an absolute path when source is outside --repo-root",
    )
    args = parser.parse_args()
    if args.status == "frozen" and not args.decision_id:
        parser.error("--status frozen requires --decision-id from a human freeze decision")
    repo_root = (args.repo_root or Path.cwd()).resolve()
    human_status = args.human_status or ("confirmed" if args.status == "frozen" else "unreviewed")
    try:
        claim = freeze_claim(
            args.source,
            locator=args.locator,
            claim_id=args.claim_id,
            unit=args.unit,
            scope=args.scope,
            repo_root=repo_root,
            status=args.status,
            human_status=human_status,
            decision_id=args.decision_id,
            allow_external=args.allow_external_source,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2
    snapshot = load_snapshot(args.output)
    upsert_claim(snapshot, claim)
    args.output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE: {args.output} ({claim['status']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
