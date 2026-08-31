"""Deterministic package checks for modeling-support-materials-auditor."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "modeling-support-materials-auditor"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "modeling-support-materials-auditor"


def test_entrypoint_sets_static_first_safety_boundary():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: modeling-support-materials-auditor" in content
    assert "description:" in content
    assert "TODO" not in content
    for phrase in (
        "rules_profile",
        "默认只读取元数据",
        "不执行陌生代码",
        "archive-and-safety",
        "privacy_and_safety",
        "reproduction_status",
        "P0",
        "P1",
    ):
        assert phrase in content


def test_references_define_manifest_archive_and_consistency_checks():
    content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    names = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
    required = {
        "support-contract.md",
        "archive-and-safety.md",
        "paper-support-consistency.md",
        "research-basis.md",
    }
    assert required <= names
    for name in required:
        assert name in content
    contract = (SKILL_DIR / "references" / "support-contract.md").read_text(
        encoding="utf-8"
    )
    safety = (SKILL_DIR / "references" / "archive-and-safety.md").read_text(
        encoding="utf-8"
    )
    consistency = (
        SKILL_DIR / "references" / "paper-support-consistency.md"
    ).read_text(encoding="utf-8")
    for phrase in (
        "support_manifest",
        "archive_sha256",
        "support_file",
        "identity_scan",
        "reproduction_status",
    ):
        assert phrase in contract
    for phrase in ("路径穿越", "符号链接", "默认静态检查", "授权运行最低条件"):
        assert phrase in safety
    for phrase in ("清单对照", "CUMCM profile", "静态文件存在不等于复现成功"):
        assert phrase in consistency


def test_fixture_set_covers_security_and_rule_fit():
    names = {path.name for path in FIXTURE_DIR.glob("*.md")}
    required = {
        "README.md",
        "expected-behavior.md",
        "positive-static-manifest.md",
        "positive-authorized-sandbox-run.md",
        "negative-appendix-mismatch.md",
        "negative-unsafe-execution.md",
        "negative-path-traversal.md",
        "negative-paper-support-mismatch.md",
        "negative-cumcm-rule-copy.md",
        "negative-identity-leak.md",
        "negative-ai-disclosure-missing.md",
    }
    assert required <= names
    expected = (FIXTURE_DIR / "expected-behavior.md").read_text(encoding="utf-8")
    for phrase in (
        "static_checked",
        "authorized_run_success",
        "陌生脚本",
        "路径穿越",
        "版本冲突",
        "不套 CUMCM",
        "身份泄露",
        "AI 详情缺失",
    ):
        assert phrase in expected
    path_risk = (FIXTURE_DIR / "negative-path-traversal.md").read_text(encoding="utf-8")
    assert ".." in path_risk and "绝对路径" in path_risk


if __name__ == "__main__":
    for test in (
        test_entrypoint_sets_static_first_safety_boundary,
        test_references_define_manifest_archive_and_consistency_checks,
        test_fixture_set_covers_security_and_rule_fit,
    ):
        test()
    print("modeling-support-materials-auditor contract: OK")
