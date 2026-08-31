"""Deterministic package checks for modeling-data-audit."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-data-audit"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-data-audit"


def test_entrypoint_declares_data_provenance_and_no_silent_cleaning():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-data-audit" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "SHA-256 hash",
        "不覆盖或静默修改原始数据",
        "provenance",
        "semantics",
        "split_leakage",
        "unknown/unverified",
        "human_status",
    ):
        assert phrase in content


def test_references_define_manifest_quality_and_leakage():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "data-contract.md",
        "quality-and-missingness.md",
        "split-and-leakage.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "data-contract.md").read_text(
        encoding="utf-8"
    )
    quality = (SKILL_DIR / "references" / "quality-and-missingness.md").read_text(
        encoding="utf-8"
    )
    leakage = (SKILL_DIR / "references" / "split-and-leakage.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "data_manifest",
        "sha256",
        "data_dictionary_entry",
        "leakage_status",
        "transform_decision",
    ):
        assert phrase in contract
    for phrase in ("缺失值", "异常与重复", "单位与口径", "影响检查"):
        assert phrase in quality
    for phrase in ("预测、解释、估计、优化还是描述", "后信息", "实体", "cleared"):
        assert phrase in leakage


def test_fixture_set_covers_quality_leakage_and_version_conflict():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-traceable-data.md",
        "negative-overwrite-raw.md",
        "negative-unit-drift.md",
        "negative-silent-outlier-delete.md",
        "negative-time-leakage.md",
        "negative-entity-leakage.md",
        "negative-unknown-source.md",
        "negative-paper-code-mismatch.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "原始数据",
        "单位漂移",
        "异常删除",
        "时间泄漏",
        "实体泄漏",
        "授权/版本/口径未知",
        "论文代码图表不一致",
        "unknown/unverified",
    ):
        assert phrase in expected
    leakage = (FIXTURE_DIR / "negative-time-leakage.md").read_text(encoding="utf-8")
    assert "整个月" in leakage and "按日期切分" in leakage


if __name__ == "__main__":
    for test in (
        test_entrypoint_declares_data_provenance_and_no_silent_cleaning,
        test_references_define_manifest_quality_and_leakage,
        test_fixture_set_covers_quality_leakage_and_version_conflict,
    ):
        test()
    print("modeling-data-audit contract: OK")
