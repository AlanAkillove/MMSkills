"""Deterministic package checks for modeling-ai-pattern-reviewer."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-ai-pattern-reviewer"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-ai-pattern-reviewer"


def test_entrypoint_has_observation_boundary():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-ai-pattern-reviewer" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "observed_signal",
        "alternative_explanation",
        "不判断作者身份",
        "不输出原创度百分比",
        "不直接改写原文",
        "human-confirmed",
    ):
        assert phrase in content


def test_references_define_five_layers_and_protocol():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for name in ("signal-taxonomy.md", "pattern-audit-protocol.md", "research-basis.md"):
        assert name in content
        assert (SKILL_DIR / "references" / name).is_file()
    assert (SKILL_DIR / "references" / "negative-signal-registry.md").is_file()
    assert (SKILL_DIR / "references" / "academic-signal-registry.md").is_file()
    assert (SKILL_DIR / "scripts" / "scan_language_signals.py").is_file()
    assert "negative-signal-registry.md" in content
    assert "防御性声明处理协议" in content
    assert (ROOT / "references" / "defensive-statement-protocol.md").is_file()
    taxonomy = (SKILL_DIR / "references" / "signal-taxonomy.md").read_text(encoding="utf-8")
    protocol = (SKILL_DIR / "references" / "pattern-audit-protocol.md").read_text(encoding="utf-8")
    for phrase in ("结构", "句法/篇章", "词汇/术语", "论证/证据", "图表/交付"):
        assert phrase in taxonomy
    for phrase in ("原文锚点", "替代解释", "竞赛保密", "相似"):
        assert phrase in protocol


def test_fixture_set_covers_false_positive_and_unauthorized_cases():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "positive-discipline-not-template.md",
        "positive-topic-specific.md",
        "negative-generic-contribution.md",
        "negative-uniform-paragraphs.md",
        "negative-high-register-packaging.md",
        "negative-claim-evidence-detach.md",
        "negative-defensive-statement-cluster.md",
        "positive-required-boundary.md",
        "negative-unauthorized-similarity.md",
        "negative-false-positive-language.md",
        "positive-reframe-packaging.md",
        "positive-empty-colon.md",
        "positive-iso-sentences.md",
        "expected-behavior.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in ("合理规范", "题目/证据锚点", "防御性声明", "不说", "未授权", "假阳性"):
        assert phrase in expected


if __name__ == "__main__":
    for test in (
        test_entrypoint_has_observation_boundary,
        test_references_define_five_layers_and_protocol,
        test_fixture_set_covers_false_positive_and_unauthorized_cases,
    ):
        test()
    print("modeling-ai-pattern-reviewer contract: OK")
