"""Check the repository's generic TeX template contract.

This is a deterministic structure check, not a LaTeX compiler and not a
competition-compliance decision. It intentionally rejects project-specific
paths and content from the reusable template.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PATTERNS = {
    r"\\documentclass": "document class",
    r"\\begin\{document\}": "document start",
    r"\\end\{document\}": "document end",
    r"\\begin\{abstract\}": "abstract environment",
    r"\\appendix": "appendix entry",
    r"\\bibliographystyle": "bibliography style",
    r"\\bibliography\{references\}": "references database",
    r"\\mmIncludeContents": "contents switch",
    r"\\mmIncludeAIStatement": "AI statement switch",
    r"\\mmIncludeCodeAppendix": "code appendix switch",
    r"\\mmShowHeader": "header switch",
    r"\\mmIncludeBibliography": "bibliography switch",
    r"\\mmIncludeAppendix": "appendix switch",
}


def check_template(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"cannot read {path}: {exc}"], []

    for pattern, label in REQUIRED_PATTERNS.items():
        if not re.search(pattern, content):
            errors.append(f"missing {label}: {pattern}")

    if re.search(r"(?:[A-Za-z]:[\\/]|/Users/|/home/|/mnt/)", content):
        errors.append("absolute local path found")
    if re.search(r"(?:\.\.[\\/]){2,}", content):
        errors.append("deep project-relative path found")
    if re.search(r"问题重述|总体分析与建模路线|子问题一：模型建立与求解|复现与支撑材料|支撑材料清单", content):
        errors.append("default template must not ship a fixed paper outline; keep layout only")
    if "TODO" in content or "FIXME" in content:
        warnings.append("unfinished marker found; replace before using as a paper")
    if re.search(r"\[填写[^\]]*\]", content):
        warnings.append("unfilled template placeholders remain (expected for a starter template)")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="TeX file to inspect")
    args = parser.parse_args()

    errors, warnings = check_template(args.path)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {args.path} matches the generic TeX template contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
