"""Deterministic package checks for modeling-anti-homogenization-auditor."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-anti-homogenization-auditor"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-anti-homogenization-auditor"


def test_entrypoint_distinguishes_homogenization_from_ai_or_originality_claims():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-anti-homogenization-auditor" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "成稿后核对题目特征",
        "不输出原创度",
        "不能推断 AI 来源",
        "problem_anchor",
        "model_path",
        "evidence_story",
        "强行创新",
        "unknown",
    ):
        assert phrase in content


def test_references_define_coverage_and_authorization_contract():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "audit-contract.md",
        "coverage-matrix.md",
        "similarity-safeguards.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "audit-contract.md").read_text(
        encoding="utf-8"
    )
    matrix = (SKILL_DIR / "references" / "coverage-matrix.md").read_text(
        encoding="utf-8"
    )
    safeguards = (SKILL_DIR / "references" / "similarity-safeguards.md").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "source_manifest_hash",
        "anchor_id",
        "present",
        "partial",
        "conflict",
        "evidence_ids",
        "human_status",
    ):
        assert phrase in contract
    for phrase in ("六列回查", "题目层", "建模层", "证据层", "修复动作分类"):
        assert phrase in matrix
    for phrase in ("默认不进行", "明确给出", "不能证明抄袭", "竞赛进行期间"):
        assert phrase in safeguards


def test_fixture_set_covers_valid_structure_and_unauthorized_comparison():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-topic-specific.md",
        "positive-standard-structure.md",
        "negative-anchor-background-only.md",
        "negative-model-menu.md",
        "negative-generic-contribution.md",
        "negative-forced-novelty.md",
        "negative-deleted-limitations.md",
        "negative-unauthorized-comparison.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "present",
        "不输出原创度",
        "合理规范",
        "基线和取舍",
        "强行创新",
        "普适最优",
        "未授权比较",
        "unknown",
    ):
        assert phrase in expected
    positive = (FIXTURE_DIR / "positive-topic-specific.md").read_text(
        encoding="utf-8"
    )
    assert "潮汐窗口" in positive and "容量敏感性" in positive


if __name__ == "__main__":
    for test in (
        test_entrypoint_distinguishes_homogenization_from_ai_or_originality_claims,
        test_references_define_coverage_and_authorization_contract,
        test_fixture_set_covers_valid_structure_and_unauthorized_comparison,
    ):
        test()
    print("modeling-anti-homogenization-auditor contract: OK")
