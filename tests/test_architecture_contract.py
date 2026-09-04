"""0.3 default architecture must not present the legacy stage pipeline as the main path."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "architecture.md"


def test_legacy_stage_graph_is_appendix_only():
    text = DOC.read_text(encoding="utf-8")
    assert "附录 A" in text
    assert "Legacy / full-orchestration" in text
    appendix = text.index("附录 A")
    assert text.index("RULES_PROFILE") > appendix
    assert "unknown" in text
    assert "语义证据" in text
    main = text[:appendix]
    assert "RULES_PROFILE" not in main
    assert "project_state/" not in main
    assert "历史字段 `depends_on`" in text[appendix:]
