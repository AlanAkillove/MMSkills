# 数据审计契约

## Manifest

```yaml
data_manifest:
  project: null
  paper_version: null
  source_manifest_hash: null
  raw_data_status: available | partial | unavailable | unknown
  files:
    - data_id: DATA-0001
      path_or_uri: null
      role: raw | derived | external | output | unknown
      format: null
      size_bytes: null
      sha256: null
      source: null
      collected_at: null
      time_range: null
      authorization: authorized | restricted | unknown | not_applicable
      notes: null
  status: draft
```

## 数据字典条目

```yaml
data_dictionary_entry:
  data_id: DATA-0001
  source_file: null
  table_or_column: null
  semantic_role: id | feature | target | weight | timestamp | category | text | geometry | derived | unknown
  description: null
  type: null
  unit: null
  scale_or_range: null
  missing_encoding: []
  entity_key: null
  time_key: null
  source_anchor: null
  paper_locations: []
  transform_ids: []
  leakage_status: not_checked | suspected | cleared | unknown
  human_status: unreviewed | needs-human-confirmation | human-confirmed | rejected | unknown
  decision_id: null
```

## 审计 finding

```text
finding_id | dimension | severity | location | observation | evidence_anchors
impact | alternative_explanation | proposed_action | acceptance_test
confidence | human_status | decision_id | notes
```

`observation` 必须可由文件、代码、日志、论文或题面定位；统计未运行、代码未读或文件不存在时写 `unknown`，不能写“没有问题”。

## 清洗/变换决定

```yaml
transform_decision:
  decision_id: DATA-DEC-0001
  input_data_ids: []
  output_data_id: null
  operation: filter | impute | cap | aggregate | normalize | encode | join | feature | label | split | other
  rule: null
  evidence: []
  alternatives: []
  selected_by_human: null
  expected_impact: null
  validation: null
  status: proposed | applied | rejected | unknown
```
