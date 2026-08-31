# 支撑材料审计契约

## 支撑 manifest

```yaml
support_manifest:
  project: null
  target_competition: null
  target_year: null
  rules_profile_id: null
  paper_path: null
  paper_sha256: null
  appendix_file_list: []
  archive_path: null
  archive_sha256: null
  archive_format: zip | rar | directory | none | unknown
  authorization: static_only | authorized_sandbox_run | unknown
  privacy_scope: null
  files: []
  status: draft
```

## 文件条目

```yaml
support_file:
  support_id: SUP-0001
  path: null
  normalized_path: null
  size_bytes: null
  sha256: null
  file_type: source | data | chart | model | config | documentation | ai_disclosure | executable | unknown
  listed_in_appendix: true
  expected_role: null
  identity_scan: clear | suspect | unknown | not_checked
  safety_status: safe_to_list | suspicious | blocked | unknown
  read_status: metadata_only | text_read | binary_unread | failed
  reproduction_status: not_attempted | static_checked | authorized_run_success | authorized_run_failed | blocked | unknown
  related_claim_ids: []
  related_experiment_ids: []
  related_figure_ids: []
```

## finding

```text
finding_id | dimension | severity | rule_ids | paper_location | support_path
file_hash | observation | evidence_anchors | impact | safety_status
reproduction_status | proposed_action | acceptance_test | confidence
human_status | decision_id | notes
```

报告中不要嵌入完整个人路径、敏感数据或危险脚本内容；用安全的相对路径、hash 和最小必要片段定位。
