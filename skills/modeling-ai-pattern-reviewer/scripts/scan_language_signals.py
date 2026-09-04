#!/usr/bin/env python3
"""Locate mechanical language-signal *candidates*. This is not an AI detector.

Output status is always "candidate". Never emit AI_probability, AI_score, or error
just because a pattern matched. Semantic judgment stays with the reviewer.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


MATH_SPAN = re.compile(r"(\$.*?\$|\\\[.*?\\\]|\\\(.*?\\\))", re.S)
ISO_LINE = re.compile(
    r"对问题[一二三四五六七八九十0-9]+[，,]\s*(本文|我们)(建立|构建|提出)"
)
EMPTY_COLON = re.compile(
    r"(核心是|原因如下|值得注意的是|本文主要工作如下|主要工作如下|具体如下)[：:]"
)
DEFINITION_COLON = re.compile(r"(定义|记为|设|令).{0,12}[：:]")
REFRAME = re.compile(r"这不仅是.{0,30}，更是")
PERSONIFY = re.compile(
    r"(如同|宛如|像)一?个?(智慧|永不疲倦|聪明).{0,16}(决策者|导师|审查员|管家)"
)
ZERO_ANAPHORA = re.compile(
    r"(?:^|\n\n)[ \t]*(值得注意的是|需要指出的是|不难发现)[，,]"
)
DASHES = re.compile(r"—|──|--")


def _plain(text: str) -> str:
    return MATH_SPAN.sub(" ", text)


def _sentences(text: str) -> list[tuple[int, str]]:
    parts: list[tuple[int, str]] = []
    start = 0
    for match in re.finditer(r"[^。！？\n]+[。！？]?", text):
        chunk = match.group().strip()
        if chunk:
            parts.append((match.start(), chunk))
        start = match.end()
    if start < len(text) and text[start:].strip():
        parts.append((start, text[start:].strip()))
    return parts


def _hit(signal_id: str, start: int, matched: str, reason: str) -> dict[str, Any]:
    snippet = re.sub(r"\s+", " ", matched).strip()
    if len(snippet) > 160:
        snippet = snippet[:157] + "..."
    return {
        "signal_id": signal_id,
        "status": "candidate",
        "location": f"offset:{start}",
        "matched_text": snippet,
        "mechanical_reason": reason,
    }


def scan_text(text: str) -> list[dict[str, Any]]:
    body = _plain(text)
    findings: list[dict[str, Any]] = []

    sentences = _sentences(body)
    run: list[tuple[int, str]] = []
    for offset, sent in sentences:
        if ISO_LINE.search(sent):
            run.append((offset, sent))
            continue
        if len(run) >= 3:
            findings.append(
                _hit(
                    "SYN-ISO-SENT",
                    run[0][0],
                    " ".join(item[1] for item in run),
                    "three-or-more consecutive isomorphic question-frames",
                )
            )
        run = []
    if len(run) >= 3:
        findings.append(
            _hit(
                "SYN-ISO-SENT",
                run[0][0],
                " ".join(item[1] for item in run),
                "three-or-more consecutive isomorphic question-frames",
            )
        )

    for match in EMPTY_COLON.finditer(body):
        window = body[max(0, match.start() - 12) : match.end()]
        if DEFINITION_COLON.search(window):
            continue
        findings.append(
            _hit("SYN-EMPTY-COLON", match.start(), match.group(), "empty lead-in before a colon")
        )

    for match in REFRAME.finditer(body):
        findings.append(
            _hit("SYN-REFRAME", match.start(), match.group(), "not-A-but-B packaging frame")
        )

    for match in PERSONIFY.finditer(body):
        findings.append(
            _hit("LEX-PERSONIFY", match.start(), match.group(), "idealized occupational metaphor")
        )

    for match in ZERO_ANAPHORA.finditer(body):
        if not body[: match.start()].strip():
            continue
        findings.append(
            _hit(
                "SYN-ZERO-ANAPHORA",
                match.start(),
                match.group().strip(),
                "paragraph-initial comment without anaphor",
            )
        )

    for paragraph in re.split(r"\n\s*\n", body):
        count = len(DASHES.findall(paragraph))
        if count >= 3:
            start = body.find(paragraph)
            findings.append(
                _hit(
                    "PUNC-DASH",
                    max(0, start),
                    paragraph[:80],
                    f"{count} dashes in one paragraph",
                )
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manuscript", type=Path, required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    findings = scan_text(args.manuscript.read_text(encoding="utf-8"))
    if args.json_out:
        args.json_out.write_text(json.dumps(findings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not findings:
        print("CANDIDATES: none")
        return 0
    for item in findings:
        print(f"CANDIDATE: {item['signal_id']}: {item['matched_text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
