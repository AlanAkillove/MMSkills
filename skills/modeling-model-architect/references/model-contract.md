# 模型注册契约

## Model registry entry

```yaml
model:
  model_id: MOD-0001
  status: baseline | candidate | adopted | rejected | failed | unknown | conflict
  task_ids: []
  anchor_ids: []
  name: null
  purpose: null
  variables: []
  parameters: []
  objective: null
  constraints: []
  units_and_domains: []
  assumptions: []
  data_requirements: []
  baseline_relation: null
  fit_to_problem: high | medium | low | unknown
  interpretability: high | medium | low | unknown
  compute_cost: low | medium | high | unknown
  implementation_cost: low | medium | high | unknown
  reproducibility: ready | partial | unavailable | unknown
  validation_plan_ids: []
  failure_boundary: null
  user_summary: null
  input_output_plain: null
  tradeoffs: []
  key_risks: []
  potential_benefit: null
  evidence_basis: []
  unknowns: []
  next_validation_priority: high | medium | low | unknown
  understanding_check: not-asked | incomplete | answered | unknown
  comprehension_status: not_presented | explained | needs-reexplanation | user-confirmed | unknown
  evidence_ids: []
  code_entry: null
  version_hash: null
  adoption_reason: null
  rejection_reason: null
  human_status: unreviewed | needs-human-confirmation | human-confirmed | rejected | unknown
  decision_id: null
```

`fit_to_problem` 描述任务适配，`evidence_ids` 描述已有证据，`human_status` 描述团队确认；三者不能互相替代。

`user_summary` 到 `comprehension_status` 是用户决策支持层，不是新的科学证据。`understanding_check` 记录是否提出过输入/输出、关键假设和代价/风险的复述问题；`answered` 不等于同意或采用。`potential_benefit` 必须写成预期或待验证收益；`unknowns` 不得被省略；`next_validation_priority` 只表示下一步验证顺序，不表示采用推荐。

## 决策记录

```text
decision_id | model_id | action | alternatives | evidence_ids | reason
assumption_impact | data_impact | validation_impact | paper_claim_impact
decision_owner | decided_at | status | notes
```

`action` 可为 `adopt/reject/continue/pause/revisit`。没有人类确认的候选不能写入最终模型或“本文创新”。
