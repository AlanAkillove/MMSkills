---
name: modeling-model-architect
description: "组织数模问题的可解释基线、候选模型、适配条件、复杂度、验证成本、失败边界和团队决策；为不熟悉模型的用户附带分项评估、通俗解释和确认问题，帮助降低理解负担，但不替人选择最终模型或编造结果。"
---

# 数学建模模型架构

## 何时使用

用户要比较候选、解释某条路径、登记基线，或检查论文模型是否与题意/代码一致时调用。用户只要求探索时，可以暂列 `candidate`，不得写成 `adopted`。

不要用本技能代替实验运行、数据清洗或最终选模。没有题面或用户描述时，先问清对象和任务，再比较。

## 硬约束

- 最终目标函数、关键假设、核心模型和采用/放弃决定由团队确认；不替人选择最终模型。
- 先给可解释基线，再谈更复杂候选。不把算法名称当创新，不为避免同质化强行引入深度学习或复杂优化。
- 不编造训练结果、最优性、鲁棒性、因果或文献依据。代码跑通不等于模型正确。
- 不使用总分、信心百分比、默认排序、单一“推荐”或把用户未回复当作确认。
- 理解校验请用户用本题对象复述输入/输出、一个关键假设和一个主要代价/风险；不能用“看懂了吗”或 Agent 自己的判断代替。
- 题意尚未经 `problem_familiarization` 确认时，正式采用停在缺口与候选；探索结果必须标为暂定。

## 默认怎么帮用户

先直接回答当前问题：这条路径回答什么、输入输出是什么、相对基线多了什么、最可能在哪里失败。默认不先写六份账本。

每个 `candidate` 仍分两层，但只在对话里给出用户真正需要的部分：

1. 专家层：变量/约束、假设、数据需求、验证计划和证据；
2. 用户层：用本题对象说明用途、适配、代价、风险和未知。用户层不使用总分。

状态只用 `baseline` / `candidate` / `adopted` / `rejected` / `failed` / `unknown`。`adopted` 不等于最优。

只有跨会话、用户要求留痕、`working_depth=full` 或最终交付时，才落盘 `model_registry.md`、`model_candidate_cards.md`、`model_decision_brief.md` 和带 `human_status` / `understanding_check` 的决策记录。详细字段、六步比较法和验证准备度按需读取 references。

没有 `literature_orientation_ledger` 或完整数据审计时，可以继续探索，但要把未核验来源和数据口径写成未知，不得在 adopt/freeze 时假装已经齐备。

## 停止条件

- `P0`：模型会改题意，或未确认却准备提交为最终模型。
- `P1`：任务不适配、关键假设/数据不可得、用户只看到黑箱总分，或核心主张没有验证路径。

未知就写未知。完整协议见 [model-contract.md](references/model-contract.md)、[baseline-and-fit.md](references/baseline-and-fit.md)、[user-decision-support.md](references/user-decision-support.md)、[validation-readiness.md](references/validation-readiness.md)、[recommended-workflow.md](references/recommended-workflow.md) 和 [research-basis.md](references/research-basis.md)。
