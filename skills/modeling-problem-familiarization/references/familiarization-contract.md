# 题目熟悉阶段字段契约

## 背景地图条目

```text
map_id:
topic_id:
statement_snapshot_id:
layer: reality | object_relation | measurement_data | task_semantics
item:
evidence_ids:
source_ids:
status: direct | visual | inferred | external | unknown | conflict
alternative_interpretations:
impact_if_wrong:
human_status: draft | needs_human | confirmed | blocked
```

背景地图的作用是帮助团队建立共同语义，不是提前写模型。`external` 只能说明背景或概念，不能覆盖题面；`inferred` 必须写出推断依据和替代解释。

## 文献思想条目

```text
literature_insight_id:
source_id:
evidence_locator:
source_question:
concept_or_mechanism:
method_precedent:
source_supports:
source_does_not_support:
transferable_idea:
non_transferable_boundary:
problem_match:
problem_difference:
question_map_anchor_ids:
future_model_decision_ids:
human_understanding_status: unread | partial | read_relevant_part | confirmed | conflict
```

`future_model_decision_ids` 在选定模型后补写，不能为了让文献“有用”而事后虚构迁移关系。

## 多轮 checkpoint

```text
round_id:
date:
focus:
materials_read:
agent_explanation:
team_restatement_or_questions:
evidence_checked:
discrepancies:
corrections:
new_unknowns:
affected_artifacts:
next_question:
status: partial | needs_human | blocked | human-confirmed
confirmed_by:
decision_id:
```

每一轮只记录可回到原材料的事实和真实的团队反馈。旧解释被纠正时保持旧记录并标记 `superseded`，不能抹掉导致返工的理解路径。

## 完成判据

`human-confirmed` 的最小范围是：对象/关键关系/边界、子问输入输出、关键术语与单位、核心来源的支持范围和不可迁移边界均已复述确认；剩余未知有明确影响和处置人。写回 pipeline 时使用 `passed + evidence_status: confirmed + decision_id`，这个状态不表示模型、实验或论文已完成。
