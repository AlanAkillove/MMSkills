# 选题阶段字段契约

## 题目卡片

每个 `topic_id` 建议保留以下字段：

```text
topic_id:
statement_snapshot_id:
source_scope:
read_status: complete | partial | blocked | conflict
neutral_summary:
object_and_system:
subproblem_ids:
task_types:
inputs_outputs:
data_and_attachments:
background_prerequisites:
verification_work:
team_fit:
time_and_compute_load:
evidence_ids:
unknowns:
risks:
distinctiveness_opportunities:
selection_status: candidate | primary_candidate | fallback_candidate | not_selected | unknown
```

`topic_id` 在整个项目中保持稳定；题面变更应产生新的 `statement_snapshot_id`，不能原地覆盖旧版本。`unknown` 表示尚未知道，不等于负面评价或可以由 Agent 补全的假设。

## 分项比较字段

```text
topic_id, dimension, assessment, evidence_ids, implication,
unknowns, conflict_ids, next_check, human_status
```

建议维度为：

| dimension | 判断对象 | 不应替代的结论 |
|---|---|---|
| `problem_comprehension` | 题面对象、关系和子问是否容易被团队准确复述 | “这题一定简单/困难” |
| `background_load` | 需要补齐的领域知识与学习时间 | “文献多所以适合” |
| `data_readiness` | 数据/附件是否可得、口径是否明确、清洗负担如何 | 数据一定可用 |
| `modeling_prerequisites` | 需要的数学、统计、优化、仿真或机理知识 | 已经选定某算法 |
| `validation_feasibility` | 是否有可区分方案的验证入口 | 结果会好/会得奖 |
| `team_fit` | 成员能力、时间和表达资源的匹配 | Agent 替团队组队 |
| `time_compute_cost` | 比赛窗口内实现、运行和复核的负担 | 复杂就是先进 |
| `evidence_traceability` | 外部事实、数据口径和方法先例是否可核查 | 引用越多越好 |
| `result_uncertainty` | 关键输入、可行性、评价指标或结论可能有多大未知 | 获奖概率 |
| `topic_specificity` | 题目约束能否触发真实的建模/验证取舍 | 强行制造创新 |

这些维度相互独立记录。若团队想做排序，Agent 只能输出“按已确认约束筛除/保留”的理由链，不能输出未经人确认的综合分数。

## 人工选题事件

```text
decision_id:
date:
primary_topic_id:
fallback_topic_id:
compared_topic_ids:
constraints_considered:
evidence_ids:
reasoning:
earliest_validation_task:
reversal_conditions:
decision_maker:
status: draft | human-confirmed | superseded
```

`human-confirmed` 只表示团队确认了选择及其范围，不表示该题容易、模型正确或结果有保证。若题面版本、团队资源或比赛规则变化，重新打开选题比较并保留旧事件。
