#!/usr/bin/env python3
"""Create a SHA-256 project-state manifest without modifying source artifacts."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


STATES = {"working", "reviewable", "frozen", "blocked", "superseded", "released"}
PURPOSES = {"context_checkpoint", "human_gate", "revision_baseline", "release_candidate"}
DEFAULT_EXCLUDED_PARTS = {
    ".git",
    ".hg",
    ".svn",
    ".pytest_cache",
    "__pycache__",
    ".venv",
    "node_modules",
    "tmp",
}
DEFAULT_EXCLUDED_NAMES = {".env", ".env.local", "id_rsa", "credentials.json"}
DEFAULT_EXCLUDED_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def normalize_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_excluded(rel: str, path: Path, patterns: Iterable[str]) -> bool:
    parts = set(Path(rel).parts)
    if parts & DEFAULT_EXCLUDED_PARTS:
        return True
    name = path.name.lower()
    if name in DEFAULT_EXCLUDED_NAMES or path.suffix.lower() in DEFAULT_EXCLUDED_SUFFIXES:
        return True
    if any(part.lower() in {"raw", "secrets", "credentials"} for part in Path(rel).parts):
        return True
    return any(fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(name, pattern) for pattern in patterns)


def collect_files(root: Path, output: Path, excludes: List[str], includes: List[str]) -> List[Dict[str, Any]]:
    output_resolved = output.resolve()
    entries: List[Dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = normalize_relative(path, root)
        if path.resolve() == output_resolved or is_excluded(rel, path, excludes):
            continue
        if includes and not any(fnmatch.fnmatch(rel, pattern) for pattern in includes):
            continue
        try:
            size, digest = sha256_file(path)
            status = "present"
        except OSError:
            size, digest, status = 0, "", "unreadable"
        sensitivity = "private" if any(token in rel.lower() for token in ("private", "personal", "internal")) else "normal"
        entries.append(
            {
                "path": rel,
                "kind": "file",
                "bytes": size,
                "sha256": digest,
                "status": status,
                "sensitivity": sensitivity,
                "source_or_generator": "local_file",
                "last_checked_at": now_iso(),
            }
        )
    return entries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--snapshot-id")
    parser.add_argument("--parent-snapshot-id", default=None)
    parser.add_argument("--state", default="working", choices=sorted(STATES))
    parser.add_argument("--purpose", default="context_checkpoint", choices=sorted(PURPOSES))
    parser.add_argument("--profile-id", default="unknown")
    parser.add_argument("--profile-hash", default="unknown")
    parser.add_argument("--decision-id", action="append", default=[])
    parser.add_argument("--confirmed-by", default=None)
    parser.add_argument("--confirmed-date", default=None)
    parser.add_argument("--confirmation-scope", default=None)
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--include", action="append", default=[])
    parser.add_argument("--note", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2
    if args.state in {"frozen", "released"} and (not args.confirmed_by or not args.decision_id):
        print("ERROR: frozen/released snapshots require --confirmed-by and --decision-id", file=sys.stderr)
        return 2
    snapshot_id = args.snapshot_id or datetime.now(timezone.utc).strftime("SNAP-%Y%m%dT%H%M%S%fZ")
    manifest = {
        "schema_version": "0.1",
        "snapshot_id": snapshot_id,
        "parent_snapshot_id": args.parent_snapshot_id,
        "project_root": str(root),
        "state": args.state,
        "purpose": args.purpose,
        "created_at": now_iso(),
        "rules_profile": {
            "profile_id": args.profile_id,
            "content_hash": args.profile_hash,
            "status": "unknown" if args.profile_id == "unknown" else "unverified",
        },
        "files": collect_files(root, output, args.exclude, args.include),
        "artifact_status": [],
        "decision_ids": args.decision_id,
        "claim_ids": [],
        "open_issue_ids": [],
        "notes": args.note,
        "human_confirmation": {
            "status": "confirmed" if args.confirmed_by and args.decision_id else "pending",
            "person_or_role": args.confirmed_by or "unknown",
            "date": args.confirmed_date or "unknown",
            "decision_id": args.decision_id[0] if args.decision_id else "unknown",
            "scope": args.confirmation_scope or "unknown",
        },
    }
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot write manifest: {exc}", file=sys.stderr)
        return 2
    print(f"WROTE: {output}")
    print(f"FILES: {len(manifest['files'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
