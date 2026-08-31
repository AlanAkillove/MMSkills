#!/usr/bin/env python3
"""Validate a state manifest, relative paths, file hashes, and sign-off gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


STATES = {"working", "reviewable", "frozen", "blocked", "superseded", "released"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return size, digest.hexdigest()


def unknown(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in {"", "unknown", "pending"})


def validate(manifest: Dict[str, Any], root: Path, final: bool) -> List[str]:
    errors: List[str] = []
    for key in ("schema_version", "snapshot_id", "state", "purpose", "files", "human_confirmation"):
        if key not in manifest:
            errors.append(f"missing field: {key}")
    state = manifest.get("state")
    if state not in STATES:
        errors.append(f"invalid state: {state!r}")
    if not isinstance(manifest.get("files"), list):
        errors.append("files must be a list")
        files = []
    else:
        files = manifest["files"]
    seen = set()
    for index, entry in enumerate(files, start=1):
        if not isinstance(entry, dict):
            errors.append(f"file {index} must be an object")
            continue
        rel = entry.get("path")
        if not isinstance(rel, str) or not rel:
            errors.append(f"file {index} has no relative path")
            continue
        path_obj = Path(rel)
        if path_obj.is_absolute() or ".." in path_obj.parts or "\\" in rel:
            errors.append(f"file {index} has unsafe/non-POSIX path: {rel!r}")
            continue
        if rel in seen:
            errors.append(f"duplicate file path: {rel}")
        seen.add(rel)
        if not SHA256_RE.fullmatch(str(entry.get("sha256", ""))):
            errors.append(f"file {rel} has invalid sha256")
            continue
        actual = root / Path(*path_obj.parts)
        if not actual.is_file():
            errors.append(f"file missing: {rel}")
            continue
        try:
            size, digest = sha256_file(actual)
        except OSError as exc:
            errors.append(f"file unreadable: {rel}: {exc}")
            continue
        if size != entry.get("bytes"):
            errors.append(f"byte count changed: {rel}")
        if digest != entry.get("sha256"):
            errors.append(f"sha256 changed: {rel}")

    confirmation = manifest.get("human_confirmation")
    if not isinstance(confirmation, dict):
        errors.append("human_confirmation must be an object")
        confirmation = {}
    if state in {"frozen", "released"} or final:
        if confirmation.get("status") != "confirmed":
            errors.append("frozen/released validation requires confirmed human_confirmation")
        for key in ("person_or_role", "date", "decision_id", "scope"):
            if unknown(confirmation.get(key)):
                errors.append(f"confirmation missing {key}")
        if not manifest.get("decision_ids"):
            errors.append("frozen/released validation requires decision_ids")
    if final and state != "released":
        errors.append("final validation requires state=released")
    if state == "released" and not manifest.get("artifact_status"):
        errors.append("released validation requires artifact_status")
    if state == "released" and not manifest.get("rules_profile", {}).get("profile_id"):
        errors.append("released validation requires rules_profile")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--final", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read manifest: {exc}")
        return 2
    errors = validate(manifest, args.root.resolve(), args.final)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
