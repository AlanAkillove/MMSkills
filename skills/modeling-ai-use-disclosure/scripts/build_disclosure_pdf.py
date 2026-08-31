#!/usr/bin/env python3
"""Build a Chinese AI-use disclosure PDF from a safe structured JSON input.

The script deliberately accepts structured JSON rather than raw chat exports. The
skill is responsible for collection, redaction, reconciliation, and human
confirmation before this presentation step.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List


def text_value(value: Any, default: str = "unknown") -> str:
    if value is None:
        return default
    if isinstance(value, list):
        if not value:
            return default
        return ", ".join(text_value(item, "") for item in value if item is not None)
    if isinstance(value, dict):
        return "; ".join(
            f"{key}: {text_value(item, '')}" for key, item in value.items()
        ) or default
    result = str(value).strip()
    return result or default


def paragraph_text(value: Any, default: str = "unknown") -> str:
    """Escape content before putting it into a ReportLab Paragraph."""

    raw = text_value(value, default)
    raw = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", raw)
    return escape(raw).replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br/>")


def require_mapping(data: Any, label: str) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError(f"{label} must be an object")
    return data


def load_input(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON input {path}: {exc}") from exc
    return require_mapping(data, "input")


def import_reportlab():
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import (
            KeepTogether,
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError as exc:  # pragma: no cover - depends on runtime bundle
        raise RuntimeError(
            "ReportLab is required. Use the bundled workspace Python runtime."
        ) from exc
    return {
        "colors": colors,
        "TA_CENTER": TA_CENTER,
        "TA_LEFT": TA_LEFT,
        "A4": A4,
        "ParagraphStyle": ParagraphStyle,
        "getSampleStyleSheet": getSampleStyleSheet,
        "mm": mm,
        "pdfmetrics": pdfmetrics,
        "UnicodeCIDFont": UnicodeCIDFont,
        "TTFont": TTFont,
        "KeepTogether": KeepTogether,
        "PageBreak": PageBreak,
        "Paragraph": Paragraph,
        "SimpleDocTemplate": SimpleDocTemplate,
        "Spacer": Spacer,
        "Table": Table,
        "TableStyle": TableStyle,
    }


def make_styles(rl: Dict[str, Any]) -> Dict[str, Any]:
    ParagraphStyle = rl["ParagraphStyle"]
    get_sample = rl["getSampleStyleSheet"]
    TA_CENTER = rl["TA_CENTER"]
    TA_LEFT = rl["TA_LEFT"]
    font_name = rl["font_name"]
    styles = get_sample()
    common = {
        "fontName": font_name,
    }
    return {
        "title": ParagraphStyle(
            "DisclosureTitle", parent=styles["Title"], fontName=font_name,
            fontSize=18, leading=24, alignment=TA_CENTER, spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "DisclosureSubtitle", parent=styles["Normal"], **common,
            fontSize=9, leading=13, alignment=TA_CENTER, textColor=rl["colors"].dimgrey,
        ),
        "banner": ParagraphStyle(
            "DisclosureBanner", parent=styles["Normal"], **common,
            fontSize=11, leading=16, alignment=TA_CENTER,
            textColor=rl["colors"].darkred, borderColor=rl["colors"].darkred,
            borderWidth=0.7, borderPadding=5, spaceAfter=10,
        ),
        "h1": ParagraphStyle(
            "DisclosureH1", parent=styles["Heading1"], **common,
            fontSize=13, leading=18, spaceBefore=8, spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "DisclosureH2", parent=styles["Heading2"], **common,
            fontSize=10.5, leading=15, spaceBefore=5, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "DisclosureBody", parent=styles["BodyText"], **common,
            fontSize=9.2, leading=14,
        ),
        "small": ParagraphStyle(
            "DisclosureSmall", parent=styles["BodyText"], **common,
            fontSize=7.4, leading=10,
        ),
        "cell": ParagraphStyle(
            "DisclosureCell", parent=styles["BodyText"], **common,
            fontSize=7.6, leading=10,
        ),
        "cell_header": ParagraphStyle(
            "DisclosureCellHeader", parent=styles["BodyText"], **common,
            fontSize=7.6, leading=10, textColor=rl["colors"].white,
        ),
        "center": ParagraphStyle(
            "DisclosureCenter", parent=styles["BodyText"], **common,
            fontSize=8, leading=11, alignment=TA_CENTER,
        ),
        "footer": ParagraphStyle(
            "DisclosureFooter", parent=styles["BodyText"], **common,
            fontSize=7, leading=9, alignment=TA_CENTER, textColor=rl["colors"].grey,
        ),
    }


def p(rl: Dict[str, Any], styles: Dict[str, Any], value: Any, style: str = "body"):
    return rl["Paragraph"](paragraph_text(value), styles[style])


def label_value_table(rl: Dict[str, Any], styles: Dict[str, Any], rows: Iterable):
    data = []
    for label, value in rows:
        data.append([p(rl, styles, label, "cell_header"), p(rl, styles, value, "cell")])
    table = rl["Table"](data, colWidths=[35 * rl["mm"], 135 * rl["mm"]], hAlign="LEFT")
    table.setStyle(
        rl["TableStyle"](
            [
                ("BACKGROUND", (0, 0), (0, -1), rl["colors"].HexColor("#40566f")),
                ("BACKGROUND", (1, 0), (1, -1), rl["colors"].HexColor("#f6f8fa")),
                ("GRID", (0, 0), (-1, -1), 0.35, rl["colors"].HexColor("#b9c1ca")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def section_heading(rl: Dict[str, Any], styles: Dict[str, Any], title: str):
    return [rl["Paragraph"](paragraph_text(title), styles["h1"])]


def build_story(data: Dict[str, Any], rl: Dict[str, Any], styles: Dict[str, Any], final: bool):
    story: List[Any] = []
    status = text_value(data.get("status"), "draft")
    status_label = "最终版 / 已人工确认" if final else "草稿 / 待人工确认"
    competition = data.get("competition", {})
    if isinstance(competition, dict):
        competition_label = " ".join(
            part for part in [text_value(competition.get("name"), ""), text_value(competition.get("year"), "")] if part
        ) or "unknown"
    else:
        competition_label = text_value(competition)

    story.append(rl["Paragraph"](paragraph_text(data.get("title"), "AI 工具使用详情"), styles["title"]))
    story.append(rl["Paragraph"](paragraph_text(status_label), styles["banner"]))
    story.append(
        rl["Paragraph"](
            paragraph_text(
                f"赛事：{competition_label}　Profile：{text_value(data.get('profile_id'))}　记录状态：{status}"
            ),
            styles["subtitle"],
        )
    )
    story.append(rl["Spacer"](1, 5))

    story += section_heading(rl, styles, "一、记录范围与规则")
    profile_source = data.get("profile_source", "unknown")
    story.append(
        label_value_table(
            rl,
            styles,
            [
                ("赛事与年份", competition_label),
                ("记录范围", data.get("scope", "unknown")),
                ("记录完整性", data.get("record_completeness", "unknown")),
                ("规则来源", profile_source),
                ("采集/整理时间", data.get("prepared_at", "unknown")),
            ],
        )
    )
    story.append(rl["Spacer"](1, 7))
    story.append(
        rl["Paragraph"](
            paragraph_text(
                "本文件仅整理授权范围内可见的 AI 使用记录。未知、冲突和未完成历史不会被推断或静默删除；最终提交前须由作者确认。"
            ),
            styles["body"],
        )
    )

    story += section_heading(rl, styles, "二、使用工具")
    tools = data.get("tools", [])
    if not isinstance(tools, list) or not tools:
        story.append(rl["Paragraph"](paragraph_text("未建立工具清单：unknown"), styles["body"]))
    else:
        tool_rows = [[
            p(rl, styles, "工具", "cell_header"),
            p(rl, styles, "开发者", "cell_header"),
            p(rl, styles, "版本/模型", "cell_header"),
            p(rl, styles, "身份状态", "cell_header"),
        ]]
        for tool in tools:
            tool = tool if isinstance(tool, dict) else {"name": tool}
            tool_rows.append([
                p(rl, styles, tool.get("name")),
                p(rl, styles, tool.get("developer")),
                p(rl, styles, tool.get("version_or_model")),
                p(rl, styles, tool.get("identity_status")),
            ])
        table = rl["Table"](tool_rows, colWidths=[42 * rl["mm"], 40 * rl["mm"], 48 * rl["mm"], 40 * rl["mm"]], repeatRows=1)
        table.setStyle(
            rl["TableStyle"](
                [
                    ("BACKGROUND", (0, 0), (-1, 0), rl["colors"].HexColor("#40566f")),
                    ("GRID", (0, 0), (-1, -1), 0.35, rl["colors"].HexColor("#b9c1ca")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl["colors"].white, rl["colors"].HexColor("#f6f8fa")]),
                ]
            )
        )
        story.append(table)

    story += section_heading(rl, styles, "三、使用阶段、用途与人工控制")
    story.append(
        rl["Paragraph"](
            paragraph_text(data.get("human_control", "unknown")), styles["body"]
        )
    )
    events = data.get("events", [])
    if not isinstance(events, list):
        events = []
    if not events:
        story.append(rl["Paragraph"](paragraph_text("没有可展示的事件记录：unknown"), styles["body"]))
    else:
        for index, event in enumerate(events, start=1):
            event = event if isinstance(event, dict) else {"output_summary": event}
            event_id = text_value(event.get("event_id"), f"event-{index}")
            story.append(
                rl["Paragraph"](
                    paragraph_text(f"事件 {event_id}　{event.get('event_family', 'unknown')}"),
                    styles["h2"],
                )
            )
            story.append(
                label_value_table(
                    rl,
                    styles,
                    [
                        ("阶段", event.get("stage")),
                        ("目的", event.get("purpose")),
                        ("输入范围", event.get("input_scope", event.get("provided"))),
                        ("输出摘要", event.get("output_summary", event.get("output"))),
                        ("采用状态", event.get("adoption")),
                        ("人工修改", event.get("human_modification", event.get("modification"))),
                        ("人工核验", event.get("human_verification", event.get("verification"))),
                        ("实质风险", event.get("substantive_risk")),
                        ("证据与记录状态", f"{text_value(event.get('evidence_level'))} / {text_value(event.get('record_status'))}"),
                        ("来源定位", event.get("source_locator", event.get("source_ids"))),
                        ("最终产物关联", event.get("artifact_refs")),
                        ("规则映射", event.get("rule_refs", event.get("rule_status"))),
                    ],
                )
            )
            story.append(rl["Spacer"](1, 5))

    story += section_heading(rl, styles, "四、代表性交互说明")
    examples = data.get("examples", [])
    if not isinstance(examples, list) or not examples:
        story.append(rl["Paragraph"](paragraph_text("未提供代表性事件：unknown"), styles["body"]))
    else:
        for example in examples:
            example = example if isinstance(example, dict) else {"output_summary": example}
            story.append(
                label_value_table(
                    rl,
                    styles,
                    [
                        ("事件", example.get("event_id")),
                        ("提示/过程完整度", example.get("prompt_status", example.get("prompt_method"))),
                        ("输出摘要", example.get("output_summary")),
                        ("后续处理", example.get("follow_up")),
                    ],
                )
            )
            story.append(rl["Spacer"](1, 5))

    story += section_heading(rl, styles, "五、未知项、冲突与隐私处理")
    unknowns = data.get("unknowns", [])
    conflicts = data.get("conflicts", [])
    privacy = data.get("privacy_note", "已按最小化原则移除密钥、私人信息和未授权隐藏内容；脱敏影响核验的项目已标明。")
    story.append(
        label_value_table(
            rl,
            styles,
            [
                ("未知项", unknowns),
                ("冲突项", conflicts),
                ("隐私说明", privacy),
            ],
        )
    )

    story += section_heading(rl, styles, "六、作者确认")
    confirmation = data.get("confirmation", {})
    confirmation = confirmation if isinstance(confirmation, dict) else {}
    story.append(
        label_value_table(
            rl,
            styles,
            [
                ("确认状态", confirmation.get("status", "pending")),
                ("确认人", confirmation.get("person")),
                ("确认日期", confirmation.get("date")),
                ("决定 ID", confirmation.get("decision_id")),
                ("确认范围", confirmation.get("scope", "unknown")),
            ],
        )
    )
    story.append(rl["Spacer"](1, 8))
    story.append(
        rl["Paragraph"](
            paragraph_text(
                "声明：本文件中的事件、采用关系、人工修改和核验状态须由作者根据真实记录确认。AI 工具不替代参赛团队对问题理解、建模决策、数据处理、实验结果和论文内容的责任。"
            ),
            styles["small"],
        )
    )
    return story


def register_cjk_font(rl: Dict[str, Any]) -> str:
    """Prefer an installed TrueType CJK font so Latin text is not over-spaced.

    The CID fallback keeps the script usable on systems without a bundled CJK
    font. A local font is embedded by ReportLab; no font is downloaded.
    """

    candidates = [
        Path(r"C:\Windows\Fonts\Deng.ttf"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
    ]
    for candidate in candidates:
        if not candidate.exists():
            continue
        try:
            kwargs = {"subfontIndex": 0} if candidate.suffix.lower() == ".ttc" else {}
            rl["pdfmetrics"].registerFont(
                rl["TTFont"]("MathDisclosureCJK", str(candidate), **kwargs)
            )
            return "MathDisclosureCJK"
        except Exception:
            continue
    rl["pdfmetrics"].registerFont(rl["UnicodeCIDFont"]("STSong-Light"))
    return "STSong-Light"


def build_pdf(data: Dict[str, Any], output: Path, final: bool) -> None:
    rl = import_reportlab()
    rl["font_name"] = register_cjk_font(rl)
    styles = make_styles(rl)
    output.parent.mkdir(parents=True, exist_ok=True)

    doc = rl["SimpleDocTemplate"](
        str(output),
        pagesize=rl["A4"],
        rightMargin=20 * rl["mm"],
        leftMargin=20 * rl["mm"],
        topMargin=18 * rl["mm"],
        bottomMargin=17 * rl["mm"],
        title="AI 工具使用详情",
        author="",
        subject="Math modeling AI-use disclosure",
    )

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(rl["font_name"], 7)
        canvas.setFillColor(rl["colors"].grey)
        canvas.drawCentredString(105 * rl["mm"], 9 * rl["mm"], f"AI 工具使用详情　第 {document.page} 页")
        canvas.restoreState()

    doc.build(build_story(data, rl, styles, final), onFirstPage=footer, onLaterPages=footer)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="structured JSON input")
    parser.add_argument("--output", required=True, type=Path, help="output PDF path")
    parser.add_argument(
        "--final",
        action="store_true",
        help="build final status; requires human-confirmed input",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = load_input(args.input)
        status = text_value(data.get("status"), "draft")
        confirmation = data.get("confirmation", {})
        if args.final:
            if status != "human-confirmed":
                raise ValueError("--final requires status=human-confirmed")
            if not isinstance(confirmation, dict) or confirmation.get("status") != "confirmed":
                raise ValueError("--final requires confirmation.status=confirmed")
            for key in ("person", "date", "decision_id"):
                if not text_value(confirmation.get(key), ""):
                    raise ValueError(f"--final requires confirmation.{key}")
        build_pdf(data, args.output, args.final)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"WROTE: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
