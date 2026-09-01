# 题目熟悉的推荐工作流

本文件是按需读取的详细协议。简单题可以一轮讲完；复杂题再按对象、数据、图示或文献边界拆分。

## 四层背景地图

建立学习材料时按层组织，并区分 `direct`、`visual`、`inferred`、`external`、`unknown` 和 `conflict`：

1. 现实背景：系统为什么存在、研究对象是谁、过程如何发生。
2. 对象与关系：实体、层级、空间/时间顺序、流向、可观测量；图示比例不自动成为数学条件。
3. 测量与数据：数据如何产生、单位、采样范围、缺失/噪声含义。
4. 任务语义：每个子问要求解释、估计、预测、比较、设计还是优化。

## 文献学习账本

每条 `literature_insight_id` 至少记录来源、它支持什么、不支持什么、可迁移思想、与本题的异同。后来被采用的思想应连到具体 `model_decision_id`。

## 多轮理解循环

1. Agent 用题目对象和一个短示例说明当前概念。
2. 团队用自己的话复述，写入 `team_restatement_or_questions`。
3. 区分题面事实、图示观察、外部知识和暂定理解。
4. 把 `round_id`、冲突和修正写入 `understanding_checkpoint.md`。
5. 会改变对象、关系、单位或子问的未决问题保持 `blocked`。

## 完成门

只有团队确认对象、子问输入输出、术语/图示没有结构性冲突、核心来源边界和未知范围后，状态才可为 `human-confirmed`。确认理解不等于确认模型。

可选落盘文件：`problem_background_map.md`、`literature_orientation_ledger.md`、`understanding_checkpoint.md`、`familiarization_open_questions.md`。
