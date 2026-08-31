# 反同质化审计契约

本契约的 YAML 记录是角色视图；跨审查 JSONL 记录还必须满足仓库根目录 [`schemas/finding.schema.json`](../../../schemas/finding.schema.json)，并通过 `deduplication` 与其他透镜关联。`risk` 只表示审计观察状态，不表示原创性或 AI 来源结论。

## 范围 manifest

```yaml
distinctiveness_audit:
  audit_version: null
  paper_version: null
  question_version: null
  source_manifest_hash: null
  competition: null
  competition_year: null
  scope: null
  read_materials: []
  unread_materials: []
  authorized_comparison_scope: null
  contest_confidentiality_window: null
  status: draft
```

## 锚点覆盖记录

```yaml
anchor_coverage:
  anchor_id: A-01
  anchor_text: null
  status: present | partial | absent | unknown | conflict | risk
  evidence_ids: []
  paper_locations: []
  model_locations: []
  validation_locations: []
  claim_ids: []
  figure_ids: []
  observation: null
  interpretation: null
  alternative_explanation: null
  impact: null
  severity: P0 | P1 | P2 | P3
  confidence: high | medium | low | unknown
  repair_type: restore_anchor | map_evidence | simplify | constrain_claim | human_decision | other
  acceptance_test: null
  human_status: unreviewed | needs-human-confirmation | human-confirmed | rejected | unknown
  decision_id: null
```

## 状态语义

- `present`：锚点不只出现于背景，且在模型、验证或结论中有可定位作用；
- `partial`：出现但缺少模型/证据/边界之一；
- `absent`：已读取足够材料后确认没有对应映射；
- `unknown`：题面、代码、数据或 ledger 未读全，暂不能判断；
- `conflict`：题面、论文、代码或版本之间不一致；
- `risk`：发现可能的模板抹平或强行创新，但仍需保留替代解释和人工判断。

不要将上述状态替换为 `原创/非原创`、`AI/非 AI` 或 `抄袭/非抄袭`。
