# 假设账本字段契约

本文件只在建立或审查 `assumption_ledger.md` 时按需读取。`status` 表示假设的生命周期，不等同于证据强度；证据状态仍需单独记录。

## 推荐结构

```markdown
# Assumption Ledger

## 0. Scope and coverage
- status: draft | needs-human-confirmation | human-confirmed | blocked
- source_manifest: ...
- model/data/code/version scope: ...
- unread_materials: ...

## 1. Assumption register
| assumption_id | type | statement | source/evidence_ids | evidence_status | scope | severity | lifecycle | confirmer/decision_id |

## 2. Necessity and alternatives
| assumption_id | problem solved | why needed | weaker/alternative assumption | what changes if relaxed |

## 3. Impact map
| assumption_id | object/variable | data | feasible set/constraint | equation/algorithm | metric/figure | claim/conclusion | direction_known |

## 4. Validity boundary and failure trigger
| assumption_id | valid_domain | edge_case_or_trigger | expected_failure_mode | claim_limit |

## 5. Validation and sensitivity plan
| assumption_id | check | data/code/experiment entry | acceptance_or_observation | result_status | evidence_ids |

## 6. Human decisions
| decision_id | confirmer | date | confirmed_scope | decision | conditions | follow_up |

## 7. Handoff
...

## 8. 长材料 checkpoint

```yaml
assumption_checkpoint:
  chunk_id: null
  source_manifest_hash: null
  source_range: null
  last_assumption_id: null
  processed_sources: []
  high_risk_open_items: []
  evidence_gaps: []
  next_chunk: null
```

`high_risk_open_items` 和 `evidence_gaps` 必须引用已登记的 `assumption_id`/`evidence_id`；不能因为某块尚未读取就写成“无其他假设”。跨块续接时不重命名已有假设，版本/hash 变化则把受影响条目降为待确认。
```

## 类型枚举

建议使用能说明来源/功能的类型，而不是给所有内容贴 `reasonable`：

- `problem_fact`：题面提供的条件；
- `team_assumption`：队伍主动作出的简化或解释；
- `derived_condition`：从已确认材料推导出的条件；
- `computational_convenience`：计算、离散化、近似或实现所需的便利条件；
- `data_assumption`：关于采样、缺失、测量、误差、代表性或切分的前提；
- `causal_or_distributional`：关于独立性、分布、因果、平稳性、外推或机制的前提；
- `unknown_or_conflict`：来源不足或材料冲突时的占位记录。

## 证据状态与生命周期

`evidence_status` 至少使用 `direct`、`visual`、`inferred`、`unknown`、`conflict`、`external`；`external` 只能提供背景，不能覆盖题面或人类决定。`lifecycle` 使用：

- `proposed`：待人确认的候选；
- `accepted`：人类明确接受，且记录确认范围；
- `accepted_with_limits`：接受但只在指定范围内有效；
- `needs-validation`：允许暂时用于实验，但不能支撑最终强结论；
- `rejected`/`retired`：已否定或被替代，保留原因；
- `blocked`：关键证据/确认缺失，禁止模型冻结。

## 严重性

沿用项目质量模型的 `P0`–`P3`：

- `P0`：可能改变题意对象、核心目标/约束、数据口径或主要结论，或存在代码/正文/题面冲突；未处理时阻断模型冻结；
- `P1`：明显影响参数、结果、验证或主要主张，但边界可局部限定；修复或限缩结论后才能冻结；
- `P2`：局部假设、说明或可复现性缺口，不改变主要结论但应补充；
- `P3`：只影响表达或低风险实现细节，不能为了修复它引入更高等级漂移。

## 最小规则

- 每条假设至少有一个 `source/evidence_id`，或者明确写 `unknown` 并说明缺口；
- 假设的 `scope` 必须落到子问题、变量、数据、模型、实验或结论，不能只写“全文”；
- `direction_known: false` 时不得写出具体偏差方向或数值影响；
- `result_status` 可用 `not-run`、`inconclusive`、`supports-within-scope`、`contradicts`，不能用“验证通过”替代实际观察；
- 人类确认只能确认具体条目和条件，不能用一次笼统签字覆盖未读取材料。

## 假设拆分示例

“忽略道路拥堵，车辆速度恒定且所有需求点都可到达”至少拆为：拥堵忽略、速度假设、可达性条件。它们的证据、失效情形和对时间/可行域的影响不同，不能合并成一个无边界的“交通状况合理”。
