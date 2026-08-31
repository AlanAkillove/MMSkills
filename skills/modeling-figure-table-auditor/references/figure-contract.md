# 图表注册契约

图表注册和角色 finding 可以保留本文件的专属字段；跨审查 JSONL finding 必须满足仓库根目录 [`schemas/finding.schema.json`](../../../schemas/finding.schema.json)，并把图表字段作为补充字段。

## 图表条目

```yaml
figure:
  figure_id: FIG-0001
  figure_type: line | bar | scatter | heatmap | map | flow | schematic | table | equation | other
  title: null
  caption: null
  paper_locations: []
  question_ids: []
  reader_tasks: []
  claim_ids: []
  evidence_ids: []
  experiment_ids: []
  model_ids: []
  source_data_ids: []
  source_code_entry: null
  data_filter_aggregation: null
  x_axis: {name: null, unit: null, range: null}
  y_axis: {name: null, unit: null, range: null}
  groups_series: []
  time_entity_scope: null
  uncertainty_display: null
  output_hash: null
  rendered_version: null
  status: planned | verified | partial | unassigned | conflict | unknown | unassessed
  human_status: unreviewed | needs-human-confirmation | human-confirmed | rejected | unknown
  decision_id: null
```

## 证据角色

`descriptive` 描述数据/分布，`comparative` 比较预先定义的对象，`trend` 展示范围内变化，`relationship` 展示关联，`sensitivity` 展示参数变化，`feasibility` 展示约束/边界，`process` 展示流程，`result_table` 汇总结果。证据角色必须与 claim/evidence 的范围一致。

## finding 记录

```text
finding_id | figure_id | issue_type | severity | location | observation
evidence_anchors | impact | proposed_action | acceptance_test
confidence | human_status | decision_id | deduplication | notes
```
