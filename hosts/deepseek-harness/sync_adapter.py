#!/usr/bin/env python3
"""Mirror MMSkills into a DeepSeek Harness scan root without rewriting source skills."""

from __future__ import annotations

import argparse
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SHARED_DIRS = ("references", "schemas", "templates", "profiles", "docs")
ROOT_FILES = ("AGENTS.md",)
IGNORE_NAMES = {".git", "__pycache__", ".pyc", ".DS_Store"}


def _ignore(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORE_NAMES or name.endswith(".pyc")}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def sync(repo: Path, target: Path) -> dict:
    target.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    src_skills = repo / "skills"
    dest_skills = target / "skills"
    if dest_skills.exists():
        shutil.rmtree(dest_skills)
    shutil.copytree(src_skills, dest_skills, ignore=_ignore)
    copied.append("skills")
    for name in SHARED_DIRS:
        src = repo / name
        if not src.is_dir():
            continue
        dest = target / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest, ignore=_ignore)
        copied.append(name)
    for name in ROOT_FILES:
        src = repo / name
        if src.is_file():
            shutil.copy2(src, target / name)
            copied.append(name)
    skill_names = sorted(path.name for path in dest_skills.iterdir() if path.is_dir())
    entry = dest_skills / "math-modeling" / "SKILL.md"
    manifest = {
        "source": "MathModelingSkills",
        "installation_mode": "native-adapter",
        "host": "deepseek-harness",
        "required_for_release": False,
        "adapter_root": str(target).replace("\\", "/"),
        "copied": copied,
        "default_entry": "math-modeling",
        "skills": skill_names,
        "source_skill_hash": sha256_file(repo / "skills" / "math-modeling" / "SKILL.md") if entry.is_file() else "",
        "adapter_skill_hash": sha256_file(entry) if entry.is_file() else "",
        "synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notes": [
            "Do not rewrite SKILL.md for DSH.",
            "Run python scripts from the upstream repository root.",
            "copied is not discovered/activated/verified.",
        ],
    }
    (target / "source-manifest.yaml").write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO)
    parser.add_argument("--target", type=Path, default=REPO / ".agents")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        skills = sorted(path.name for path in (args.repo / "skills").iterdir() if path.is_dir())
        print("DRY-RUN default_entry=math-modeling")
        print("DRY-RUN skills=" + ",".join(skills))
        print(f"DRY-RUN target={args.target}")
        return 0
    manifest = sync(args.repo, args.target)
    if manifest.get("source_skill_hash") != manifest.get("adapter_skill_hash"):
        print("ERROR: adapter rewrote math-modeling SKILL.md")
        return 1
    print(f"WROTE: {args.target / 'source-manifest.yaml'}")
    print(f"ENTRY: {manifest['default_entry']}")
    print(f"SKILLS: {len(manifest['skills'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
