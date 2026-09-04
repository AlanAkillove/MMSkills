#!/usr/bin/env python3
"""Deterministic PDF page QA. This is not a layout beauty score or compliance certificate.

Always runs with pypdf: page count, paper size, blank pages, text extractability,
metadata/path leaks. Optional pymupdf raster is recorded as unassessed when missing.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader

A4 = (595.27, 841.89)
LETTER = (612.0, 792.0)
PAPERS = {"a4": A4, "letter": LETTER}
PATH_RE = re.compile(r"(?:[A-Za-z]:[\\/](?:Users|home)|/Users/|/home/)")
IDENTITY_RE = re.compile(r"(?:队号|指导老师|指导教师|\.edu\.cn)")


def _page_size(page: Any) -> tuple[float, float]:
    box = page.mediabox
    return float(box.width), float(box.height)


def _size_ok(width: float, height: float, expected: tuple[float, float], tol: float = 3.0) -> bool:
    ew, eh = expected
    portrait = abs(width - ew) <= tol and abs(height - eh) <= tol
    landscape = abs(width - eh) <= tol and abs(height - ew) <= tol
    return portrait or landscape


def inspect_pdf(
    path: Path,
    *,
    paper: str = "a4",
    min_pages: int | None = None,
    max_pages: int | None = None,
    scan_identity: bool = True,
) -> dict[str, Any]:
    reader = PdfReader(str(path))
    findings: list[dict[str, Any]] = []
    expected = PAPERS[paper]
    pages: list[dict[str, Any]] = []
    metadata = reader.metadata
    meta_text = " ".join(
        str(getattr(metadata, key, "") or "")
        for key in ("author", "creator", "producer", "subject", "title")
    ) if metadata else ""
    if PATH_RE.search(meta_text):
        findings.append({"id": "pdf-meta-path", "severity": "P1", "message": "PDF metadata contains a local filesystem path"})
    if scan_identity and IDENTITY_RE.search(meta_text):
        findings.append({"id": "pdf-meta-identity", "severity": "P1", "message": "PDF metadata may contain identity or affiliation text"})

    if not reader.pages:
        findings.append({"id": "pdf-empty", "severity": "P0", "message": "PDF has no pages"})

    for index, page in enumerate(reader.pages, start=1):
        width, height = _page_size(page)
        text = page.extract_text() or ""
        try:
            images = list(getattr(page, "images", []) or [])
        except Exception:
            images = []
        rotation = int(getattr(page, "rotation", 0) or 0)
        record = {
            "page": index,
            "width": round(width, 2),
            "height": round(height, 2),
            "rotation": rotation,
            "chars": len(text.strip()),
            "images": len(images),
            "extraction": "ok" if text.strip() else ("unreliable" if images else "empty"),
        }
        pages.append(record)
        if not _size_ok(width, height, expected):
            findings.append(
                {
                    "id": f"pdf-page-size-{index}",
                    "severity": "P1",
                    "message": f"page {index} size {width:.1f}x{height:.1f} is not {paper}",
                }
            )
        if record["extraction"] == "empty":
            findings.append(
                {
                    "id": f"pdf-blank-{index}",
                    "severity": "P1",
                    "message": f"page {index} has no extractable text or images",
                }
            )
        elif record["extraction"] == "unreliable":
            findings.append(
                {
                    "id": f"pdf-extract-{index}",
                    "severity": "P2",
                    "message": f"page {index} has images but no extractable text; use raster review",
                    "status": "unassessed-without-raster",
                }
            )
        if PATH_RE.search(text):
            findings.append(
                {
                    "id": f"pdf-path-{index}",
                    "severity": "P1",
                    "message": f"page {index} text contains a local filesystem path",
                }
            )
        if scan_identity and IDENTITY_RE.search(text):
            findings.append(
                {
                    "id": f"pdf-identity-{index}",
                    "severity": "P1",
                    "message": f"page {index} may leak contest identity text",
                }
            )

    if min_pages is not None and len(reader.pages) < min_pages:
        findings.append({"id": "pdf-page-count-low", "severity": "P1", "message": f"page count {len(reader.pages)} < {min_pages}"})
    if max_pages is not None and len(reader.pages) > max_pages:
        findings.append({"id": "pdf-page-count-high", "severity": "P1", "message": f"page count {len(reader.pages)} > {max_pages}"})

    raster = _optional_raster(path)
    report = {
        "file": str(path).replace("\\", "/"),
        "pages": len(reader.pages),
        "paper": paper,
        "page_records": pages,
        "raster": raster,
        "findings": findings,
    }
    return report


def _optional_raster(path: Path) -> dict[str, Any]:
    try:
        import fitz  # type: ignore
    except ImportError:
        return {"status": "unassessed", "reason": "pymupdf not installed"}
    document = fitz.open(str(path))
    blanks: list[int] = []
    for index, page in enumerate(document, start=1):
        pixmap = page.get_pixmap(dpi=72, alpha=False)
        samples = pixmap.samples
        if not samples:
            continue
        mean = sum(samples) / len(samples)
        if mean > 250:
            blanks.append(index)
    document.close()
    return {"status": "checked", "near_blank_pages": blanks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--paper", choices=sorted(PAPERS), default="a4")
    parser.add_argument("--min-pages", type=int)
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--no-identity", action="store_true")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    report = inspect_pdf(
        args.pdf,
        paper=args.paper,
        min_pages=args.min_pages,
        max_pages=args.max_pages,
        scan_identity=not args.no_identity,
    )
    if args.json_out:
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    blocking = [item for item in report["findings"] if item.get("severity") in {"P0", "P1"}]
    if blocking:
        for item in blocking:
            print(f"ERROR: {item['id']}: {item['message']}")
        return 1
    print(f"OK: {report['pages']} page PDF; raster={report['raster']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
