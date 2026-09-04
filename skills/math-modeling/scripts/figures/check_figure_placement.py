#!/usr/bin/env python3
"""Refuse diagnostic figures in the manuscript set; optionally inspect PNG geometry."""

from __future__ import annotations

import argparse
import json
import struct
import zlib
from pathlib import Path
from typing import Any

import yaml

ALLOWED_PLACEMENT = {"diagnostic", "comparison", "paper", "appendix"}
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def inspect_png(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIG):
        raise ValueError(f"not a PNG: {path}")
    width = height = None
    dpi = None
    offset = 8
    while offset + 8 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        tag = data[offset + 4 : offset + 8]
        chunk = data[offset + 8 : offset + 8 + length]
        if tag == b"IHDR" and len(chunk) >= 8:
            width, height = struct.unpack(">II", chunk[:8])
        elif tag == b"pHYs" and len(chunk) >= 9:
            xppm, _yppm, unit = struct.unpack(">IIB", chunk[:9])
            if unit == 1:
                dpi = round(xppm * 0.0254, 2)
        elif tag == b"IEND":
            break
        offset += 12 + length
    return {"path": str(path).replace("\\", "/"), "width": width, "height": height, "dpi": dpi}


def write_png(path: Path, width: int, height: int) -> None:
    """Tiny RGB PNG helper for tests and fixtures."""

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + (b"\x00\x00\x00" * width) for _ in range(height))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(PNG_SIG + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def _as_figures(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("figures"), list):
        return [item for item in payload["figures"] if isinstance(item, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("figure_design"), dict):
        return [payload["figure_design"]]
    if isinstance(payload, dict):
        return [payload]
    raise ValueError("figure manifest must be a mapping")


def check_manifest(payload: Any) -> list[str]:
    errors: list[str] = []
    for figure in _as_figures(payload):
        figure_id = figure.get("figure_id") or "unknown"
        placement = figure.get("placement")
        if placement not in ALLOWED_PLACEMENT:
            errors.append(f"{figure_id}: placement must be diagnostic|comparison|paper|appendix")
            continue
        used = bool(figure.get("used_in_manuscript"))
        location = str(figure.get("paper_location") or "")
        in_body = used or location.lower() in {"body", "main", "正文"}
        if placement == "diagnostic" and in_body:
            errors.append(f"{figure_id}: diagnostic figure must not enter the manuscript body")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--image", type=Path, action="append")
    parser.add_argument("--min-width", type=int)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    payload = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    errors = check_manifest(payload)
    images = []
    for image in args.image or []:
        info = inspect_png(image)
        images.append(info)
        if args.min_width and (info["width"] or 0) < args.min_width:
            errors.append(f"{image.name}: width {info['width']} < {args.min_width}")
    if args.json_out:
        args.json_out.write_text(
            json.dumps({"errors": errors, "images": images}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    print("OK: figure placement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
