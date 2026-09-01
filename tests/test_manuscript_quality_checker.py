"""Regression tests for the deterministic manuscript cleanliness checker."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "skills" / "modeling-final-preflight" / "scripts" / "check_manuscript_quality.py"
REFERENCE = ROOT / "templates" / "tex" / "main.tex"


def run_checker(path: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(path), *extra],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_checker_blocks_process_residue_and_reports_reading_risks(tmp_path: Path):
    manuscript = tmp_path / "bad.tex"
    report = tmp_path / "report.json"
    manuscript.write_text(
        r"""\begin{document}
\begin{abstract}
（草稿，待全文完成后定稿。）需要指出的是，本文围绕某对象展开。值得注意的是，结果仅供说明。不能据此外推。"""
        + "具体结果。" * 220
        + r"""
\end{abstract}
\section{结果}
本节已求解，使用 ASM-01 和表\ref{tab:missing}。
\begin{itemize}
\item 第一项
\end{itemize}
\begin{itemize}
\item 第二项
\end{itemize}
\begin{itemize}
\item 第三项
\end{itemize}
\end{document}
""",
        encoding="utf-8",
    )
    result = run_checker(manuscript, "--output", str(report), "--reference", str(REFERENCE))
    assert result.returncode == 1
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["status"] == "blocked"
    categories = {item["category"] for item in payload["findings"]}
    assert {"draft-marker", "internal-id", "broken-reference", "list-density"} <= categories
    assert "defensive-meta-cluster" in categories
    assert "abstract_paragraphs" in payload["reference_comparison"]["metrics"]


def test_checker_accepts_clean_small_manuscript(tmp_path: Path):
    manuscript = tmp_path / "clean.tex"
    manuscript.write_text(
        r"""\begin{document}
\begin{abstract}
第一段交代对象、任务和方法。

第二段给出结果、适用范围和必要限制。
\end{abstract}
\section{问题分析}
本文根据题面中的变量关系建立模型，并用实验结果检验参数影响。
\label{sec:analysis}
详见第\ref{sec:analysis}节。
\end{document}
""",
        encoding="utf-8",
    )
    result = run_checker(manuscript)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "STATUS: pass" in result.stdout


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        test_checker_blocks_process_residue_and_reports_reading_risks(Path(directory))
        test_checker_accepts_clean_small_manuscript(Path(directory))
    print("manuscript quality checker tests: OK")
