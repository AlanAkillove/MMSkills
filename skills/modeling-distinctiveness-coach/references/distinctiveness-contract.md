# 差异化账本契约

## 项目 manifest

```yaml
distinctiveness_manifest:
  project: null
  competition: null
  year: null
  question_version: null
  source_manifest_hash: null
  scope: null
  status: draft
  human_confirmation_required: true
```

## 差异化条目

```yaml
distinctiveness_item:
  item_id: DIS-0001
  status: observed | team_decision | candidate | generic | forced_novelty_risk | unknown | conflict
  anchor_type: object | relation | constraint | time_space | objective | data | subproblem | other
  anchor_text: null
  evidence_ids: []
  evidence_anchors: []
  team_decision: null
  decision_id: null
  modeling_mapping: null
  validation_mapping: null
  claim_mapping: []
  figure_mapping: []
  alternative_paths: []
  rejection_reason: null
  complexity_cost: null
  failure_boundary: null
  forced_novelty_reason: null
  confidence: high | medium | low | unknown
  human_status: unreviewed | needs-human-confirmation | human-confirmed | rejected | unknown
```

## 允许进入正文的条件

一个差异化候选只有在满足下列条件后，才能被表述为团队的建模取舍或本题发现：

1. 有题面、数据、代码、实验或团队决策证据；
2. 能说明它改变了哪个变量、约束、验证、图表或结论边界；
3. 有可验收的推导、运行、对照或人工确认；
4. 不把局部结果外推为普适规律；
5. 不增加无法承担的复杂度、术语或合规风险。

“听起来不同”但不能回答这些问题的条目只能保留为 `candidate` 或 `forced_novelty_risk`。

## 长文/长会话续接

每轮记录 source hash、题面块首尾锚点、已提取的 anchor ID、已确认决策、未读材料、冲突、下一块和不允许重新解释的术语。重新开始时先合并旧账本，不能仅凭摘要重新生成“独特性”。
