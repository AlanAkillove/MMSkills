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

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


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
    r"(问题分析|总体分析|建模路线|结果解释|结论|讨论|模型评价|可靠性)"
)
SECTION_SPLIT = re.compile(r"\\(?:sub)*section\*?\{([^}]+)\}")
BOXED_COMMANDS = re.compile(r"\\(?:boxed|fbox|framebox|colorbox)\b|\\box\{")
ENGLISH_ABSTRACT = re.compile(
    r"\\textbf\{\s*Abstract\s*\}|\\section\*?\{\s*Abstract\s*\}",
    re.I,
)
CITE_KEY = re.compile(r"\\cite[t]?\{([^}]+)\}")
BIBITEM_KEY = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")
TWENTY_PAGE_LIMIT = re.compile(r"(正文|[Mm]ain text).{0,24}(?:<=|≤|不超过|不多于)\s*20\s*页")
EVALUATION_TRIPLE = re.compile(r"优点.{0,12}局限.{0,12}改进")
PROBLEM_RESTATEMENT_SECTION = re.compile(r"\\(?:sub)*section\*?\{\s*[^}]*问题重述")


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


def load_yaml_profile(path: Optional[Path]) -> Optional[Dict[str, Any]]:
    if path is None:
        return None
    if yaml is None:
        raise RuntimeError("PyYAML is required to load writing/rules profiles")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def citation_keys(text: str) -> tuple[set[str], set[str]]:
    cited: set[str] = set()
    for match in CITE_KEY.finditer(text):
        cited.update(part.strip() for part in match.group(1).split(",") if part.strip())
    bibitems = {match.group(1).strip() for match in BIBITEM_KEY.finditer(text)}
    return cited, bibitems


def apply_writing_profile(
    text: str,
    findings: List[Dict[str, Any]],
    writing_profile: Dict[str, Any],
    *,
    rules_profile: Optional[Dict[str, Any]] = None,
    pdf_pages: Optional[int] = None,
    raw_content: Optional[str] = None,
    preferred_pages: Optional[List[int]] = None,
) -> None:
    prose = writing_profile.get("prose") or {}
    if prose.get("unordered_lists") == "forbidden":
        itemize = list(re.finditer(r"\\begin\{itemize\}", text))
        if itemize:
            add_finding(
                findings,
                finding_id="MQL-010",
                category="unordered-list-forbidden",
                severity="P1",
                message=f"当前写作 profile 禁止无序 itemize（{len(itemize)} 处）",
                suggestion="把分点改成连续段落。算法步骤和正式假设可用 enumerate。不要写问题重述专章。",
                lines=line_numbers(text, itemize),
            )
    sections_cfg = writing_profile.get("sections") or {}
    if sections_cfg.get("problem_restatement") == "forbidden":
        restated = list(PROBLEM_RESTATEMENT_SECTION.finditer(text))
        if restated:
            add_finding(
                findings,
                finding_id="MQL-017",
                category="problem-restatement-section",
                severity="P1",
                message="当前写作 profile 禁止单独的“问题重述”章节",
                suggestion="不要整章复述题面。必要对象、任务和条件并入问题分析或各问建模。",
                lines=line_numbers(text, restated),
            )
    if prose.get("default_model_evaluation_triple") == "forbidden" and EVALUATION_TRIPLE.search(text):
        add_finding(
            findings,
            finding_id="MQL-011",
            category="evaluation-triple",
            severity="P2",
            message="检测到“优点—局限—改进方向”式模型评价骨架",
            suggestion="写成讨论段，说明主要误差来源和验证边界，不要用三组 bullet 收束。",
        )
    equations = writing_profile.get("equations") or {}
    if equations.get("boxed_emphasis") == "forbidden":
        boxed = list(BOXED_COMMANDS.finditer(text))
        if boxed:
            add_finding(
                findings,
                finding_id="MQL-012",
                category="boxed-equation",
                severity="P1",
                message="禁止用 boxed/fbox/framebox/colorbox 对公式做视觉框强调",
                suggestion="给公式编号，在正文写“由式（n）可得”，不要画框。",
                lines=line_numbers(text, boxed),
            )
    abstract_cfg = writing_profile.get("abstract") or {}
    if abstract_cfg.get("english_abstract") is False:
        english = list(ENGLISH_ABSTRACT.finditer(text))
        if english:
            add_finding(
                findings,
                finding_id="MQL-013",
                category="english-abstract-forbidden",
                severity="P1",
                message="当前写作 profile 不生成英文摘要",
                suggestion="删除 Abstract；官方“无需翻译成英文”不是要求补英文摘要。",
                lines=line_numbers(text, english),
            )
    refs_cfg = writing_profile.get("references") or {}
    if refs_cfg.get("orphan_entries") == "forbidden":
        cited, bibitems = citation_keys(text)
        orphans = sorted(bibitems - cited)
        if bibitems and not cited:
            add_finding(
                findings,
                finding_id="MQL-014",
                category="orphan-bibliography",
                severity="P1",
                message=f"参考文献 {len(bibitems)} 条，正文 \\cite 为 0",
                suggestion="在首次使用参数、模型或材料常数处给出文内引用；孤立 bibitem 不能作为文献证据。",
            )
        elif orphans:
            add_finding(
                findings,
                finding_id="MQL-014",
                category="orphan-bibliography",
                severity="P1",
                message="存在正文未引用的参考文献：" + ", ".join(orphans),
                suggestion="删除孤立条目，或在首次使用处 \\cite。",
            )
    body = writing_profile.get("body_length") or {}
    preferred = preferred_pages if preferred_pages else (body.get("preferred_pages") or [])
    official_limit = None
    if rules_profile:
        official_limit = (
            ((rules_profile.get("submission") or {}).get("paper") or {}).get("main_text_page_limit")
        )
    try:
        official_limit = int(official_limit) if official_limit is not None else None
    except (TypeError, ValueError):
        official_limit = None
    page_limit_haystack = raw_content if raw_content is not None else text
    if official_limit == 30 and TWENTY_PAGE_LIMIT.search(page_limit_haystack):
        add_finding(
            findings,
            finding_id="MQL-015",
            category="wrong-rules-year-page-limit",
            severity="P1",
            message="稿件仍按正文不超过 20 页描述，与当前 rules profile 的 30 页上限冲突",
            suggestion="赛题年份不是提交规则年份。加载 cumcm-2026，不要搜索或套用 2025 页数。",
        )
    if (
        pdf_pages is not None
        and isinstance(preferred, list)
        and len(preferred) >= 1
        and pdf_pages < int(preferred[0])
    ):
        add_finding(
            findings,
            finding_id="MQL-016",
            category="coverage-short",
            severity="P2",
            message=(
                f"PDF 约 {pdf_pages} 页，低于当前写作目标 {preferred[0]}–{preferred[-1]} 页"
            ),
            suggestion=(
                "触发论证覆盖审查：参数来源、算法细节、验证和不确定度是否缺失。"
                "不得用空话、重复或多余图表注水。官方上限仍以 rules profile 为准。"
            ),
        )


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


def check_manuscript(
    path: Path,
    reference: Optional[Path] = None,
    *,
    writing_profile: Optional[Path] = None,
    rules_profile: Optional[Path] = None,
    pdf_pages: Optional[int] = None,
    preferred_pages: Optional[List[int]] = None,
) -> Dict[str, Any]:
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

    writing_payload = load_yaml_profile(writing_profile)
    rules_payload = load_yaml_profile(rules_profile)
    if writing_payload:
        apply_writing_profile(
            text,
            findings,
            writing_payload,
            rules_profile=rules_payload,
            pdf_pages=pdf_pages,
            raw_content=content,
            preferred_pages=preferred_pages,
        )

    metrics = style_metrics(text)
    cited, bibitems = citation_keys(text)
    metrics["cite_keys"] = len(cited)
    metrics["bibitems"] = len(bibitems)
    p1 = sum(1 for finding in findings if finding["severity"] == "P1")
    p2 = sum(1 for finding in findings if finding["severity"] == "P2")
    status = "blocked" if p1 else "needs_review" if p2 else "pass"
    return {
        "tool": "check_manuscript_quality",
        "tool_version": "0.3.2",
        "input": str(path),
        "status": status,
        "severity_counts": {"P1": p1, "P2": p2},
        "metrics": metrics,
        "findings": findings,
        "reference_comparison": compare_metrics(reference, metrics),
        "writing_profile": str(writing_profile) if writing_profile else None,
        "rules_profile": str(rules_profile) if rules_profile else None,
        "scope_note": "可观察的成文清洁、写作 profile 机械项与阅读风险检查；不计算 AI 率、原创度、相似度或获奖概率。",
    }


def parse_preferred_pages(value: Optional[str]) -> Optional[List[int]]:
    if not value:
        return None
    parts = [part.strip() for part in value.replace("-", ",").split(",") if part.strip()]
    return [int(part) for part in parts]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="TeX or TeX-like manuscript source")
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    parser.add_argument("--reference", type=Path, help="optional local manuscript used only as a style reference")
    parser.add_argument("--writing-profile", type=Path, help="manuscript writing profile YAML")
    parser.add_argument("--rules-profile", type=Path, help="official contest rules profile YAML")
    parser.add_argument("--pdf-pages", type=int, help="observed PDF page count for coverage audit")
    parser.add_argument(
        "--preferred-pages",
        help="optional project overlay like 26,28; public writing profiles should leave this empty",
    )
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
        report = check_manuscript(
            args.input,
            args.reference,
            writing_profile=args.writing_profile,
            rules_profile=args.rules_profile,
            pdf_pages=args.pdf_pages,
            preferred_pages=parse_preferred_pages(args.preferred_pages),
        )
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
