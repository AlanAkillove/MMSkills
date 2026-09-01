#!/usr/bin/env python3
"""Check observable manuscript-quality risks without pretending to score prose.

This is a deterministic release-cleanliness check.  It catches process residue,
unfinished markers, broken TeX references and a few high-signal reading risks.
It does not estimate AI use, originality, quality, or competition outcome.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


PATTERNS: Sequence[Tuple[str, str, str, str]] = (
    (
        "draft-marker",
        r"草稿|待全文[^。\n]{0,20}定稿|尚未完成|draft\s+version|working\s+draft",
        "P1",
        "最终论文仍含草稿状态说明",
    ),
    (
        "placeholder",
        r"待填|待填写|\[填写[^\]]*\]|TODO|FIXME|TBD|placeholder",
        "P1",
        "最终论文仍含未完成占位内容",
    ),
    (
        "internal-id",
        r"(?<![A-Za-z0-9])(?:ASM|TAB|DATA|CHK|OVQ|R-AI|T)-\d+(?![A-Za-z0-9])",
        "P2",
        "正文疑似泄露内部账本、题面或审计编号",
    ),
    (
        "process-meta",
        r"本节已求解|假设账本|finding\s*ID|审计编号|关于表[一二三四五六七八九十\d]+的说明|当前拟合质量|最终数值以[^。\n]{0,30}确认|文中所有[^。\n]{0,30}初步估计",
        "P2",
        "正文含可能属于工作记录而非论文叙述的过程性话语",
    ),
)

DEFENSIVE_META_PATTERN = r"需要指出的是|值得注意的是|需要强调的是|需要说明的是|不能据此|这并不意味着|这不意味着"


def visible_tex(content: str) -> str:
    """Remove ordinary TeX comments so commented examples do not become findings."""

    lines = []
    for line in content.splitlines():
        lines.append(re.sub(r"(?<!\\)%.*$", "", line))
    return "\n".join(lines)


def line_numbers(text: str, matches: Iterable[re.Match[str]]) -> List[int]:
    positions = [match.start() for match in matches]
    return sorted({text.count("\n", 0, position) + 1 for position in positions})


def add_finding(
    findings: List[Dict[str, Any]],
    *,
    finding_id: str,
    category: str,
    severity: str,
    message: str,
    suggestion: str,
    lines: Optional[List[int]] = None,
) -> None:
    findings.append(
        {
            "finding_id": finding_id,
            "category": category,
            "severity": severity,
            "message": message,
            "suggestion": suggestion,
            "lines": lines or [],
        }
    )


NARRATIVE_SECTION = re.compile(
    r"(问题分析|总体分析|建模路线|结果解释|结论|讨论)"
)
SECTION_SPLIT = re.compile(r"\\(?:sub)*section\*?\{([^}]+)\}")


def narrative_list_risk(text: str) -> Optional[Dict[str, Any]]:
    """Flag lists that are doing narrative work, not a global item count.

    Assumptions, algorithm steps and parameter tables may reasonably use lists.
    Consecutive lists in analysis, route, result-explanation, discussion or
    conclusion sections are the high-signal reading risk.
    """

    parts = SECTION_SPLIT.split(text)
    hottest: Optional[Dict[str, Any]] = None
    for index in range(1, len(parts), 2):
        title = parts[index]
        body = parts[index + 1] if index + 1 < len(parts) else ""
        if not NARRATIVE_SECTION.search(title):
            continue
        environments = len(re.findall(r"\\begin\{(?:itemize|enumerate)\}", body))
        items = len(re.findall(r"\\item\b", body))
        if environments >= 2 and items >= 3:
            candidate = {
                "title": title,
                "environments": environments,
                "items": items,
            }
            if hottest is None or items > hottest["items"]:
                hottest = candidate
    return hottest


def extract_abstract(text: str) -> Optional[str]:
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S)
    return match.group(1).strip() if match else None


def style_metrics(text: str) -> Dict[str, Any]:
    abstract = extract_abstract(text)
    paragraphs = []
    if abstract is not None:
        paragraphs = [part.strip() for part in re.split(r"(?:\n\s*\n|\\par\b)", abstract) if part.strip()]
    return {
        "source_lines": len(text.splitlines()),
        "source_characters": len(text),
        "abstract_characters": len(abstract or ""),
        "abstract_paragraphs": len(paragraphs),
        "sections": len(re.findall(r"\\section\*?\{", text)),
        "subsections": len(re.findall(r"\\subsection\*?\{", text)),
        "itemize_environments": len(re.findall(r"\\begin\{itemize\}", text)),
        "enumerate_environments": len(re.findall(r"\\begin\{enumerate\}", text)),
        "list_items": len(re.findall(r"\\item\b", text)),
        "labels": len(re.findall(r"\\label\{[^}]+\}", text)),
        "references": len(re.findall(r"\\(?:eqref|ref|autoref)\{[^}]+\}", text)),
    }


def compare_metrics(reference: Optional[Path], current: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if reference is None:
        return None
    try:
        reference_text = visible_tex(reference.read_text(encoding="utf-8"))
    except OSError as exc:
        return {"error": str(exc)}
    reference_metrics = style_metrics(reference_text)
    comparable = (
        "abstract_paragraphs",
        "sections",
        "subsections",
        "itemize_environments",
        "enumerate_environments",
        "list_items",
    )
    return {
        "path": str(reference),
        "metrics": reference_metrics,
        "difference": {
            key: current.get(key, 0) - reference_metrics.get(key, 0) for key in comparable
        },
        "interpretation": "仅作风格参照，不是通过条件；列表数量和章节数量不能单独证明质量。",
    }


def check_manuscript(path: Path, reference: Optional[Path] = None) -> Dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    text = visible_tex(content)
    findings: List[Dict[str, Any]] = []
    for index, (category, pattern, severity, message) in enumerate(PATTERNS, start=1):
        matches = list(re.finditer(pattern, text, re.I if category == "process-meta" else 0))
        if matches:
            suggestion = {
                "draft-marker": "删除状态说明；若仍是草稿，将状态放在论文外部交接记录。",
                "placeholder": "补齐真实内容，或删除不适用的段落/宏；不要把占位符带入提交稿。",
                "internal-id": "将编号留在内部审计记录，正文改用自然的对象、变量或章节指代。",
                "process-meta": "保留真正影响结论范围的限制，将过程说明改写为论文叙述或移到内部记录。",
            }[category]
            add_finding(
                findings,
                finding_id=f"MQL-{index:03d}",
                category=category,
                severity=severity,
                message=message,
                suggestion=suggestion,
                lines=line_numbers(text, matches),
            )

    defensive_matches = list(re.finditer(DEFENSIVE_META_PATTERN, text))
    if len(defensive_matches) >= 3:
        add_finding(
            findings,
            finding_id="MQL-005",
            category="defensive-meta-cluster",
            severity="P2",
            message=f"检测到重复的防御性元话语（{len(defensive_matches)}处），需判断是否提供了新的范围、证据或限制",
            suggestion="保留有功能的范围/不确定性/局限说明；将没有新信息的自我免责句合并或删除，不要只做同义词轮换。",
            lines=line_numbers(text, defensive_matches),
        )

    abstract = extract_abstract(text)
    if abstract is None:
        add_finding(
            findings,
            finding_id="MQL-006",
            category="abstract-missing",
            severity="P1",
            message="未找到 abstract 环境",
            suggestion="在最终论文中补充摘要，并在主体结果稳定后回填。",
        )
    else:
        paragraphs = [part.strip() for part in re.split(r"(?:\n\s*\n|\\par\b)", abstract) if part.strip()]
        if len(paragraphs) <= 1 and len(abstract) >= 600:
            add_finding(
                findings,
                finding_id="MQL-007",
                category="dense-abstract",
                severity="P2",
                message="摘要为单个高密度段落，可能把多个问题、方法和限制挤在一起",
                suggestion="按实际信息功能分段，确保对象、任务、方法、关键结果和边界可快速定位；不强制固定段落数。",
                lines=[text.count("\n", 0, text.find(abstract)) + 1 if abstract else 1],
            )

    labels = set(re.findall(r"\\label\{([^}]+)\}", text))
    ref_matches = list(re.finditer(r"\\(?:eqref|ref|autoref)\{([^}]+)\}", text))
    missing_refs = sorted({match.group(1) for match in ref_matches if match.group(1) not in labels})
    if missing_refs:
        add_finding(
            findings,
            finding_id="MQL-008",
            category="broken-reference",
            severity="P1",
            message="存在找不到对应 label 的交叉引用：" + ", ".join(missing_refs),
            suggestion="补齐或删除失效引用，并重新编译检查编号。",
            lines=line_numbers(text, [match for match in ref_matches if match.group(1) in missing_refs]),
        )

    narrative_lists = narrative_list_risk(text)
    if narrative_lists:
        add_finding(
            findings,
            finding_id="MQL-009",
            category="list-density",
            severity="P2",
            message=(
                f"叙事性章节「{narrative_lists['title']}」连续使用列表"
                f"（environments={narrative_lists['environments']}, "
                f"items={narrative_lists['items']}），需检查是否用分点替代了论证"
            ),
            suggestion=(
                "假设、算法步骤、参数等真正并列的对象可以保留列表；"
                "问题分析、路线、结果解释、讨论和结论优先写成连续段落。"
                "此项按章节位置判断，不把全文 item 数写成固定上限。"
            ),
        )

    metrics = style_metrics(text)
    p1 = sum(1 for finding in findings if finding["severity"] == "P1")
    p2 = sum(1 for finding in findings if finding["severity"] == "P2")
    status = "blocked" if p1 else "needs_review" if p2 else "pass"
    return {
        "tool": "check_manuscript_quality",
        "tool_version": "0.2.1",
        "input": str(path),
        "status": status,
        "severity_counts": {"P1": p1, "P2": p2},
        "metrics": metrics,
        "findings": findings,
        "reference_comparison": compare_metrics(reference, metrics),
        "scope_note": "可观察的成文清洁与阅读风险检查；不计算 AI 率、原创度、相似度或获奖概率。",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="TeX or TeX-like manuscript source")
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    parser.add_argument("--reference", type=Path, help="optional local manuscript used only as a style reference")
    parser.add_argument(
        "--fail-on",
        choices=("p1", "any", "never"),
        default="p1",
        help="exit non-zero on P1 only (default), any finding, or never",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = check_manuscript(args.input, args.reference)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot inspect manuscript: {exc}", file=sys.stderr)
        return 2
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: cannot write report: {exc}", file=sys.stderr)
            return 2
    print(f"STATUS: {report['status']}")
    print(f"FINDINGS: {len(report['findings'])}")
    print(json.dumps(report["metrics"], ensure_ascii=False, sort_keys=True))
    if args.fail_on == "never":
        return 0
    if args.fail_on == "any" and report["findings"]:
        return 1
    if args.fail_on == "p1" and report["status"] == "blocked":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
