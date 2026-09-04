"""PDF visual QA must catch blank pages, wrong paper size, and metadata leaks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "modeling-tex-paper-production" / "scripts" / "check_pdf_visual.py"
sys.path.insert(0, str(SCRIPT.parent))
from check_pdf_visual import inspect_pdf  # noqa: E402


def write_simple_pdf(
    path: Path,
    *,
    width: float,
    height: float,
    texts: list[str],
    author: str = "",
) -> None:
    """Write a tiny PDF with Helvetica text. No reportlab required."""

    def escape(text: str) -> str:
        return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

    objects = ["placeholder"]
    objects.append("<< /Type /Catalog /Pages 2 0 R >>")
    kids: list[str] = []
    page_objs: list[tuple[str, str]] = []
    next_id = 4
    for text in texts:
        page_id = next_id
        content_id = next_id + 1
        next_id += 2
        kids.append(f"{page_id} 0 R")
        stream = f"BT /F1 12 Tf 72 720 Td ({escape(text)}) Tj ET" if text else ""
        encoded = stream.encode("latin-1", "replace")
        page_objs.append(
            (
                "<< /Type /Page /Parent 2 0 R "
                f"/MediaBox [0 0 {width:.2f} {height:.2f}] "
                "/Resources << /Font << /F1 3 0 R >> >> "
                f"/Contents {content_id} 0 R >>",
                f"<< /Length {len(encoded)} >>\nstream\n{stream}\nendstream",
            )
        )
    objects.append(f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(texts)} >>")
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    for page_dict, content in page_objs:
        objects.append(page_dict)
        objects.append(content)
    info_id = len(objects)
    objects.append(f"<< /Author ({escape(author)}) /Producer (MMSkills PDF QA fixture) >>")

    body = b"%PDF-1.4\n"
    offsets = [0]
    for index, obj in enumerate(objects[1:], start=1):
        offsets.append(len(body))
        body += f"{index} 0 obj\n{obj}\nendobj\n".encode("latin-1", "replace")
    xref_pos = len(body)
    xref = f"xref\n0 {len(objects)}\n0000000000 65535 f \n"
    xref += "".join(f"{offset:010d} 00000 n \n" for offset in offsets[1:])
    trailer = (
        f"trailer\n<< /Size {len(objects)} /Root 1 0 R /Info {info_id} 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n"
    )
    path.write_bytes(body + xref.encode("ascii") + trailer.encode("ascii"))


def test_a4_text_page_passes(tmp_path: Path):
    pdf = tmp_path / "ok.pdf"
    write_simple_pdf(pdf, width=595.27, height=841.89, texts=["abstract page"])
    report = inspect_pdf(pdf, paper="a4", scan_identity=True)
    assert report["pages"] == 1, report
    assert not [item for item in report["findings"] if item["severity"] in {"P0", "P1"}], report["findings"]


def test_blank_page_wrong_size_and_path_metadata(tmp_path: Path):
    pdf = tmp_path / "bad.pdf"
    write_simple_pdf(
        pdf,
        width=612.0,
        height=792.0,
        texts=["body", ""],
        author=r"C:\Users\contestant",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(SCRIPT),
            str(pdf),
            "--paper",
            "a4",
            "--json-out",
            str(tmp_path / "qa.json"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads((tmp_path / "qa.json").read_text(encoding="utf-8"))
    ids = {item["id"] for item in payload["findings"]}
    assert any(item.startswith("pdf-blank-") for item in ids), ids
    assert any(item.startswith("pdf-page-size-") for item in ids), ids
    assert "pdf-meta-path" in ids, ids


def test_letter_paper_is_ok_when_profile_asks_for_letter(tmp_path: Path):
    pdf = tmp_path / "letter.pdf"
    write_simple_pdf(pdf, width=612.0, height=792.0, texts=["MCM page"])
    report = inspect_pdf(pdf, paper="letter", scan_identity=True)
    assert not [item for item in report["findings"] if item["severity"] in {"P0", "P1"}], report["findings"]
    unassessed = inspect_pdf(pdf, paper=None, scan_identity=False)
    assert any(item["id"] == "pdf-paper-unassessed" for item in unassessed["findings"])
    assert not [item for item in unassessed["findings"] if item["severity"] in {"P0", "P1"}]


def test_edu_cn_bibliography_url_is_not_identity_leak(tmp_path: Path):
    pdf = tmp_path / "refs.pdf"
    write_simple_pdf(
        pdf,
        width=595.27,
        height=841.89,
        texts=["https://www.tsinghua.edu.cn/paper.pdf"],
    )
    report = inspect_pdf(pdf, paper="a4", scan_identity=True)
    ids = {item["id"] for item in report["findings"]}
    assert not any(item.startswith("pdf-identity-") for item in ids), report["findings"]
