# 主张—证据矩阵字段契约

## 推荐表结构

```csv
claim_id,claim_text,claim_type,claim_role,section,location,qualifiers,scope,claim_strength,evidence_ids,evidence_type,evidence_locator,evidence_status,evidence_scope,related_model,related_experiment,related_figure,validation_gap,verdict,severity,audit_confidence,proposed_action,human_verified,decision_id,notes
```

## 字段说明

| 字段 | 要求 |
|---|---|
| `claim_id` | 稳定 ID，例如 `C-001`；修订后沿用，不因换句子重编号 |
| `claim_text` | 保留主张原文和限定词；不要只保留关键词 |
| `claim_type` | 描述、比较、预测、因果、优化、鲁棒、推广、数学、方法或决策主张 |
| `claim_role` | `core`、`supporting` 或 `context`；用于确定阻断优先级，不代表主张真假 |
| `location` | 页码/段落/句子/图注等可回读位置 |
| `qualifiers/scope` | 对象、时间/空间、样本、工况、数据集和限定条件 |
| `claim_strength` | 原文承诺的强度，如观察、支持、优于、显著、最优、证明、普适 |
| `evidence_ids` | 一条或多条来源锚点；没有证据写空并把状态设为 `missing`/`unverified`，不能伪造 ID |
| `evidence_type` | `proof/derivation/computation/data/experiment/simulation/figure/code/citation/definition/human-decision` 等 |
| `evidence_status` | `direct/partial/indirect/missing/contradictory/unknown` |
| `evidence_scope` | 证据实际覆盖的对象、范围和条件 |
| `validation_gap` | 还缺什么验证，或为什么不能从现有材料推出该主张 |
| `verdict` | `supported-within-scope`、`partially-supported`、`overstated`、`unverified`、`contradicted`、`not-applicable` |
| `severity` | 沿用项目 `P0`–`P3` |
| `audit_confidence` | 对本次审查判断的 `high`/`medium`/`low` 置信度；不等于主张成立概率 |
| `proposed_action` | `retain`、`limit`、`add-evidence`、`remove`、`human-review` 等建议，不是自动执行命令 |
| `human_verified` | 只有具体人工核验后才为 `true`；默认 `false` |

## 证据与主张的最小对应

- `proof/derivation` 可以支持定义域内的形式数学结论，但不能单独支持现实预测或因果解释；
- `computation/simulation` 支持“在给定代码、参数、输入和实现下得到某结果”，不能自动支持全局最优或现实规律；
- `data/experiment` 支持观测范围内的描述或比较，是否因果、显著、可推广取决于设计和不确定性报告；
- `figure` 必须核对数据、单位、图例和生成代码；一张图的存在不是证据强度；
- `citation` 只能支持来源实际说过且适用于当前对象/条件的内容，不能用泛引文装饰主张；
- `human-decision` 记录采用/限缩/拒绝决定，不是替代事实或实验的证据。

若主张依赖假设，`evidence_scope` 或 `notes` 还应引用对应 `assumption_id`，并写成“在该假设/输入/实现下支持”；不允许用 `supported-within-scope` 掩盖条件被省略。

## 状态约束

`human_verified: true` 需要确认人、日期、主张范围和 `decision_id`。`supported-within-scope` 也必须写范围；没有证据的核心主张不能以“暂定支持”绕过 `unverified`。
