# 审稿 finding 契约

本文件的 YAML 示例保留审稿角色的阅读友好字段；跨 skill 传递的 JSONL finding 必须同时满足仓库根目录 [`schemas/finding.schema.json`](../../../schemas/finding.schema.json)。`lens`、`blocking` 和本角色的关联 ID 是补充字段，去重关系使用 `deduplication` 对象。

## 评审范围 manifest

```yaml
review_manifest:
  paper_version: null
  source_manifest_hash: null
  target_competition: null
  target_year: null
  scope: null
  read_materials: []
  unread_materials: []
  authorized_external_materials: []
  confidentiality_boundary: null
  mode: full
  status: draft
```

`source_manifest_hash` 建议使用 SHA-256。题面、论文、代码和数据版本不一致时，不把其中任一版本默认为真，应建立冲突 finding。

## 单条 finding

```yaml
finding:
  finding_id: REV-0001
  lens: question | model | data_experiment | claim_evidence | reader_expression | compliance
  severity: P0 | P1 | P2 | P3
  blocking: true
  location:
    document: null
    page: null
    section: null
    paragraph_or_line: null
    anchor: null
  observation: null
  evidence_anchors: []
  interpretation: null
  alternative_explanation: null
  why_it_matters: null
  confidence: high | medium | low | unknown
  related_claim_ids: []
  related_assumption_ids: []
  related_term_ids: []
  related_figure_ids: []
  repair_type: clarify | add_evidence | rerun | constrain_claim | reconcile | format | human_decision | other
  acceptance_test: null
  human_status: unreviewed
  decision_id: null
  deduplication:
    canonical_issue_key: null
    relation: new | duplicate | supplement | upgrade | downgrade | conflict
  notes: null
```

## 事实、判断、建议三层

- **事实**：能在论文、题面、代码、数据或规则来源中定位的内容；引用原文时保持必要长度，不改写成更强断言；
- **判断**：评阅者对适配性、支撑度、复原难度或风险的解释；明确是判断，不伪装成数据；
- **建议**：可验收的修复动作；不替作者决定模型或创造新证据。

## 严重性判据

严重性表示不修复会对题意、正确性、复核、合规或读者判断造成的影响，不表示“作者差”或“肯定错误”。

| 级别 | 典型判据 | 默认处理 |
|---|---|---|
| P0 | 题意/对象错读、关键公式/代码不一致、结果不可复核、保密/身份/明确规则阻断 | 阻断冻结；人工决定 |
| P1 | 核心假设无依据、模型不适配、数据泄漏、主要结论证据不足、强因果/最优/鲁棒承诺越界 | 先修复或限缩主张；人工确认 |
| P2 | 变量/图表/术语/引用/结构/阅读路径降低复原和判断效率 | 安排修稿；可作为有条件通过项 |
| P3 | 不影响实质的格式或局部冗余 | 可选修复 |

## 关闭条件

finding 只有在满足其 `acceptance_test` 且新版本 hash 已记录后才可标为 `resolved`。如果作者选择接受风险，应记录 `accepted-risk`、理由、确认人和 `decision_id`；未运行实验、未读取材料或团队尚未决定的事项不能标为已关闭。
