---
name: modeling-problem-familiarization
description: "在选题和题面初读后，分轮带领团队熟悉题目背景、对象机理、图表/空间时间关系、术语与相关文献，记录复述纠错和理解快照；理解未确认前可以讲解和探索，但不把理解写成已冻结的题意、模型或结论。"
---

# 数学建模题目熟悉与背景学习

## 何时使用

选题后需要读懂背景、图示关系复杂、或用户说“带我读题 / 让我理解主要内容”时调用。默认在对话里讲解，不生成 `question_map.md`。用户要求把已确认题意整理成正式问题地图时，再转交 `modeling-problem-intake`。只需核验引用时转交文献 skill。

它不是模型选择器。可以解释候选概念和比较文献迁移边界；正式的模型候选比较仍需在理解确认后采用。不要从算法名称开始熟悉题目。对象与机理清楚后，稳定下来的中英文名称写入 `terminology_table.md`（establish），不要等到写论文再统一。领域知识不承重时不必强行检索文献。

## 硬约束

- 不得把搜索摘要或模型记忆当文献证据，不得把外部结论写成本题事实。
- “论文使用过某方法”只是方法先例；“该方法适合本题”必须逐项比较对象、数据、假设和验证条件。
- 不得用“用户没有反对”代替有范围的复述。`human-confirmed` 需要确认范围和 `decision_id`。
- 不得在理解确认前把暂定方向写成正式模型选择、冻结假设或论文主张。

## 默认怎么帮用户

分轮讲解，不要一次倒出整本教科书。每轮围绕一个可验证主题：Agent 说明 → 团队复述/提问 → 核对题面/图示/外部知识差异。请团队用自己的话重述对象与关系，而不是只问“看懂了吗”。

需要组织学习材料时，用四层地图区分 `direct` / `visual` / `inferred` / `external` / `unknown`：题目背景、对象与关系、测量与数据、任务语义。文献条目使用 `literature_insight_id`，并写清可迁移部分与文献迁移边界。

默认先在对话里完成讲解。只有跨会话、用户要求留痕、`working_depth=full` 或最终交付时，才落盘 `understanding_checkpoint.md`（含 `team_restatement_or_questions`）、背景地图和开放问题。

## 停止条件

关键图、附件或来源缺失，或题面与历史解释冲突：标 `blocked`，不要猜测。用户明确要求探索模型时，可以展示暂定候选，但必须标明尚未确认。

详见 [familiarization-contract.md](references/familiarization-contract.md)、[recommended-workflow.md](references/recommended-workflow.md) 与 [research-basis.md](references/research-basis.md)。
