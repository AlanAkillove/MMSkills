"""Deterministic contract checks for modeling-paper-writer."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-paper-writer"


def test_writer_is_intent_first_and_not_a_template_filler():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-paper-writer" in content
    for phrase in (
        "优先推进该范围",
        "不是必须的固定顺序",
        "以段落为主要表达单位",
        "摘要通常在主体结果稳定后写",
        "成文清洁",
        "不编造证据",
        "writing_notes",
    ):
        assert phrase in content


def test_writer_has_human_boundary_and_soft_missing_artifact_behavior():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "仍由人类确认",
        "不替团队决定核心内容",
        "内部 finding/decision/assumption ID",
        "可选的流程文档",
        "可以继续写作",
    ):
        assert phrase in content
    assert (SKILL_DIR / "agents" / "openai.yaml").exists()


if __name__ == "__main__":
    test_writer_is_intent_first_and_not_a_template_filler()
    test_writer_has_human_boundary_and_soft_missing_artifact_behavior()
    print("modeling-paper-writer contract: OK")
