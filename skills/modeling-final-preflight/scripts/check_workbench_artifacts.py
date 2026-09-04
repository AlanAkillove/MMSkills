#!/usr/bin/env python3
"""Run deterministic workbench checks that preflight can invoke without LLM judgment.

Zero requested checks is unassessed, not OK. Pass contest paper size when checking PDFs.
Terminology drift here is a mechanical alias/wrapper scan only.
"""

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
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--terminology-table", type=Path)
    parser.add_argument("--manuscript", type=Path)
    parser.add_argument("--figure-manifest", type=Path)
    parser.add_argument("--claimed-citation", type=Path)
    parser.add_argument("--fetched-citation", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--paper", choices=["a4", "letter"])
    parser.add_argument("--no-identity", action="store_true")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    report: dict[str, Any] = {
        "errors": [],
        "warnings": [],
        "checks_run": [],
        "unassessed": [],
    }
    repo_root = args.repo_root or Path.cwd()

    if args.snapshot:
        report["checks_run"].append("result_freshness")
        report["errors"].extend(
            check_freshness(args.snapshot, args.snapshot_source, repo_root)
        )
    if args.terminology_table and args.manuscript:
        report["checks_run"].append("terminology_mechanical_drift")
        drifts = scan(
            args.terminology_table.read_text(encoding="utf-8"),
            args.manuscript.read_text(encoding="utf-8"),
        )
        report["terminology_drift"] = drifts
        report["errors"].extend(f"terminology {item['kind']}: {item['term']}" for item in drifts)
    elif args.terminology_table or args.manuscript:
        report["unassessed"].append("terminology_mechanical_drift_needs_table_and_manuscript")
    if args.figure_manifest:
        report["checks_run"].append("figure_placement")
        payload = yaml.safe_load(args.figure_manifest.read_text(encoding="utf-8"))
        figure_errors = check_manifest(payload)
        report["figure_errors"] = figure_errors
        report["errors"].extend(figure_errors)
    if args.claimed_citation and args.fetched_citation:
        report["checks_run"].append("citation_compare")
        citation_errors = compare_records(
            json.loads(args.claimed_citation.read_text(encoding="utf-8")),
            json.loads(args.fetched_citation.read_text(encoding="utf-8")),
        )
        report["citation_errors"] = citation_errors
        report["errors"].extend(citation_errors)
    elif args.claimed_citation or args.fetched_citation:
        report["unassessed"].append("citation_compare_needs_claimed_and_fetched")
    if args.pdf:
        report["checks_run"].append("pdf_visual")
        if not args.paper:
            report["unassessed"].append("pdf_paper_size")
        pdf_report = inspect_pdf(
            args.pdf,
            paper=args.paper,
            scan_identity=not args.no_identity,
        )
        report["pdf"] = pdf_report
        report["errors"].extend(
            f"pdf {item['id']}: {item['message']}"
            for item in pdf_report.get("findings", [])
            if item.get("severity") in {"P0", "P1"}
        )
        report["warnings"].extend(
            f"pdf {item['id']}: {item['message']}"
            for item in pdf_report.get("findings", [])
            if item.get("status") == "unassessed" or item.get("severity") == "P2"
        )

    if args.json_out:
        args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not report["checks_run"]:
        report["unassessed"].append("no_checks_requested")
        print("UNASSESSED: no workbench checks were requested")
        print("checks_run: []")
        print(f"unassessed: {', '.join(report['unassessed'])}")
        return 2

    if report["errors"]:
        for item in report["errors"]:
            print(f"ERROR: {item}")
        print(f"checks_run: {', '.join(report['checks_run'])}")
        if report["unassessed"]:
            print(f"unassessed: {', '.join(report['unassessed'])}")
        return 1
    print("OK: workbench artifacts")
    print(f"checks_run: {', '.join(report['checks_run'])}")
    if report["unassessed"]:
        print(f"unassessed: {', '.join(report['unassessed'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
