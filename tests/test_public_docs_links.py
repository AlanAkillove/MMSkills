"""Public docs should only point at files that still exist."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_ROOTS = (
    ROOT / "README.md",
    ROOT / "docs" / "architecture.md",
    ROOT / "docs" / "skill-catalog.md",
    ROOT / "docs" / "agent-skill-installation.md",
    ROOT / "docs" / "quality-model.md",
    ROOT / "docs" / "tex.md",
)
RELATIVE_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _local_targets(markdown: str, source: Path) -> list[Path]:
    targets: list[Path] = []
    for raw in RELATIVE_LINK.findall(markdown):
        href = raw.strip().split()[0]
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = href.split("#", 1)[0]
        if not path:
            continue
        targets.append((source.parent / path).resolve())
    return targets


def test_public_doc_relative_links_exist():
    missing: list[str] = []
    for doc in DOC_ROOTS:
        text = doc.read_text(encoding="utf-8")
        for target in _local_targets(text, doc):
            if not target.exists():
                missing.append(f"{doc.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
    assert missing == []


def test_readme_does_not_advertise_process_docs():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in (
        "implementation-roadmap",
        "docs/research/",
        "docs/adr/",
        "block-design",
        "roles-and-gates",
    ):
        assert phrase not in readme
