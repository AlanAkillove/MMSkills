"""End-to-end manuscript regression against desensitized real-failure signals.

This is not a prose scorer and does not compare similarity with any mature paper.
It checks that known process-residue patterns remain visible to the cleanliness
linter, and that the human rubric still names the reading dimensions that regex
cannot judge.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "paper-regression"
CHECKER = ROOT / "skills" / "modeling-final-preflight" / "scripts" / "check_manuscript_quality.py"


def test_rubric_names_reading_dimensions_without_prescribing_a_template():
    rubric = (FIXTURES / "rubric.md").read_text(encoding="utf-8")
    for phrase in (
        "摘要",
        "段落组织",
        "列表使用",
        "题目特异性",
        "过程痕迹",
        "术语自然度",
        "论证连续性",
        "不是相似度",
        "不把任何一篇成熟论文规定为必须五段摘要",
    ):
        assert phrase in rubric
    readme = (FIXTURES / "README.md").read_text(encoding="utf-8")
    assert "26A" not in readme or "不是" in readme
    protocol = (FIXTURES / "replay-protocol.md").read_text(encoding="utf-8")
    for phrase in (
        "不是",
        "端到端写作测试",
        "继续问题三",
        "比较几个模型",
        "第一次真实 Agent",
        "不要计算与任何成熟论文的相似度",
    ):
        assert phrase in protocol, phrase


def test_desensitized_failure_excerpt_still_surfaces_process_residue(tmp_path: Path):
    report = tmp_path / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            str(FIXTURES / "excerpt-process-residue.tex"),
            "--output",
            str(report),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(report.read_text(encoding="utf-8"))
    categories = {item["category"] for item in payload["findings"]}
    assert {"draft-marker", "internal-id", "process-meta", "list-density"} <= categories
    assert payload["scope_note"].startswith("可观察的成文清洁")
