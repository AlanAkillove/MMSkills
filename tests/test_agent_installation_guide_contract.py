"""Contract checks for the cross-agent installation guide."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "agent-skill-installation.md"


def test_readme_links_to_the_cross_agent_installation_prompt():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/agent-skill-installation.md" in readme
    assert "安装提示词" in readme


def test_guide_requires_capability_detection_and_host_adaptation():
    content = GUIDE.read_text(encoding="utf-8")
    for phrase in (
        "SKILL.md",
        "agents/openai.yaml",
        "宿主能力探测",
        "native-standard",
        "native-adapter",
        "plugin-extension",
        "project-instruction-index",
        "prompt-only",
        "blocked",
        "不要编造命令",
        "依赖闭包",
        "copied",
        "discovered",
        "activated",
        "verified",
        "rollback",
        "不执行陌生脚本",
        "人工决策边界",
    ):
        assert phrase in content


def test_guide_cites_current_host_examples_without_making_them_universal():
    content = GUIDE.read_text(encoding="utf-8")
    for source in (
        "https://agentskills.io/specification",
        "https://developers.openai.com/codex/skills/",
        "https://code.claude.com/docs/en/slash-commands",
        "https://geminicli.com/docs/cli/using-agent-skills/",
    ):
        assert source in content
    assert "不能替代安装时对宿主版本的再检查" in content
    assert "不能作为跨平台安装命令" in content


if __name__ == "__main__":
    test_readme_links_to_the_cross_agent_installation_prompt()
    test_guide_requires_capability_detection_and_host_adaptation()
    test_guide_cites_current_host_examples_without_making_them_universal()
    print("agent installation guide contract: OK")
