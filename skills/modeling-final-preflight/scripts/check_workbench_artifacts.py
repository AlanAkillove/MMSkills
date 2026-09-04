#!/usr/bin/env python3
"""Run deterministic workbench checks that preflight can invoke without LLM judgment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[3]
RESULTS = ROOT / "skills" / "math-modeling" / "scripts" / "results"
FIGURES = ROOT / "skills" / "math-modeling" / "scripts" / "figures"
TERM = ROOT / "skills" / "modeling-terminology-auditor" / "scripts"
EVIDENCE = ROOT / "skills" / "math-modeling" / "scripts" / "evidence"
TEX = ROOT / "skills" / "modeling-tex-paper-production" / "scripts"
for path in (RESULTS, FIGURES, TERM, EVIDENCE, TEX):
    sys.path.insert(0, str(path))

from check_figure_placement import check_manifest  # noqa: E402
from check_pdf_visual import inspect_pdf  # noqa: E402
from check_result_freshness import check_freshness  # noqa: E402
from check_terminology_drift import scan  # noqa: E402
from citations import compare_records  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--snapshot-source", type=Path)
    parser.add_argument("--terminology-table", type=Path)
    parser.add_argument("--manuscript", type=Path)
    parser.add_argument("--figure-manifest", type=Path)
    parser.add_argument("--claimed-citation", type=Path)
    parser.add_argument("--fetched-citation", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    report: dict[str, Any] = {"errors": []}
    if args.snapshot:
        report["errors"].extend(check_freshness(args.snapshot, args.snapshot_source))
    if args.terminology_table and args.manuscript:
        drifts = scan(
            args.terminology_table.read_text(encoding="utf-8"),
            args.manuscript.read_text(encoding="utf-8"),
        )
        report["terminology_drift"] = drifts
        report["errors"].extend(f"terminology {item['kind']}: {item['term']}" for item in drifts)
    if args.figure_manifest:
        payload = yaml.safe_load(args.figure_manifest.read_text(encoding="utf-8"))
        figure_errors = check_manifest(payload)
        report["figure_errors"] = figure_errors
        report["errors"].extend(figure_errors)
    if args.claimed_citation and args.fetched_citation:
        citation_errors = compare_records(
            json.loads(args.claimed_citation.read_text(encoding="utf-8")),
            json.loads(args.fetched_citation.read_text(encoding="utf-8")),
        )
        report["citation_errors"] = citation_errors
        report["errors"].extend(citation_errors)
    if args.pdf:
        pdf_report = inspect_pdf(args.pdf)
        report["pdf"] = pdf_report
        report["errors"].extend(
            f"pdf {item['id']}: {item['message']}"
            for item in pdf_report.get("findings", [])
            if item.get("severity") in {"P0", "P1"}
        )
    if args.json_out:
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["errors"]:
        for item in report["errors"]:
            print(f"ERROR: {item}")
        return 1
    print("OK: workbench artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
