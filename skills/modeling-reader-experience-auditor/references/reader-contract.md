# 阅读体验审计契约

## 范围 manifest

```yaml
reader_audit:
  paper_version: null
  source_manifest_hash: null
  target_reader_paths:
    - fast-review
    - technical-reproduction
    - non-specialist
  target_competition: null
  target_year: null
  text_materials: []
  rendered_materials: []
  unassessed_materials: []
  scope: null
  status: draft
```

## 读者任务

```yaml
reader_task:
  task_id: READ-0001
  reader_path: fast-review | technical-reproduction | non-specialist
  task: null
  entry_points: []
  required_information: []
  expected_locations: []
  observed_locations: []
  backtrack_count: unknown
  status: clear | partial | blocked | unknown | unassessed
```

## 单条阅读摩擦

```yaml
reader_finding:
  finding_id: READ-0001
  reader_path: fast-review
  severity: P0 | P1 | P2 | P3
  location:
    document: null
    page: null
    section: null
    paragraph_or_line: null
    object: null
  friction_type: extra_lookup | extra_backtrack | ambiguity | visual_block | attention_load | unknown
  observation: null
  evidence_anchors: []
  affected_task: null
  reader_cost: null
  interpretation: null
  minimal_action: null
  acceptance_test: null
  related_claim_ids: []
  related_term_ids: []
  related_figure_ids: []
  handoff: null
  confidence: high | medium | low | unknown
  human_status: unreviewed | needs-human-confirmation | human-confirmed | rejected | unknown
  decision_id: null
```

## 状态边界

`clear` 表示在当前材料范围内可定位完成；`partial` 表示需要回读或缺一项信息；`blocked` 表示无法完成任务；`unknown` 表示内容未读全或定义/证据不明确；`unassessed` 只用于未提供渲染件等无法检查的维度。未知和未评估不能写成通过。
