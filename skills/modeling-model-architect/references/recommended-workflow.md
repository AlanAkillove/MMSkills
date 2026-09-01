# 模型比较的推荐工作流

本文件是按需读取的详细协议，不是每轮必须执行的 SOP。用户只要解释、比较或回查时，直接进入相关范围。最终采用、关键假设和评价指标仍由人决定。

## 1. 重建任务和模型对象

从题面或 `question_map` 列出任务类型（描述/估计/预测/分类/优化/仿真/决策等）、决策变量、状态/观测量、目标、约束、时间/空间边界和输出形式。对每一项写“模型要回答什么”，不从算法名反推题目。

## 2. 定义基线

选择与题目目标一致、参数少、可解释、可验证的最小基线；记录适用条件、不可处理之处、计算入口和评价方式。没有合理基线时标出原因，不为了形式拼一个不合适的模型。

## 3. 登记候选并做适配比较与用户解释

对每个候选填写：题目锚点/变量/约束映射、数据规模和质量要求、假设、可解释性、计算/实现成本、复现条件、验证实验、失败边界、表达成本、与基线的可比较指标和预计收益；再翻译成用户层分项评估。复杂度必须由题目结构或证据触发。

## 4. 检查假设和数据可用性

回查假设账本与数据审计；不自动添加独立同分布、正态、平稳、线性、因果、代表性、可行性或最优性假设。候选需要的数据、标签、时间顺序和计算资源若未确认，状态保持 `unknown`。

## 5. 设计最小验证矩阵

为每个重要模型安排能区分候选/基线的验证：对照、边界、敏感性、消融、误差、不确定性、时间/实体外推或可行性检查。只写验证计划和验收标准，不预填结果。

## 6. 用户理解、人工决策与版本化

请用户用本题对象复述每个候选的输入/输出、一个关键假设、一个主要代价/风险和当前未知。不把“看过”“未回复”或默认选项当作理解/同意。之后由团队确认采用、放弃、继续试验、暂停或暂不决定，并记录确认人、日期、理由、decision ID、代码/数据版本和对论文主张的影响。模型注册不可原地抹去旧路径。

## 需要落盘时的最低记录

```text
model_id | status | task_ids | anchor_ids | model_name
variables_constraints | assumptions | data_requirements | baseline_relation
interpretability | compute_cost | implementation_cost | reproducibility
validation_plan | failure_boundary | expression_cost | adoption_reason
rejection_reason | evidence_ids | code_entry | version_hash
user_summary | input_output_plain | tradeoffs | key_risks | unknowns
next_validation_priority | understanding_check | comprehension_status | human_status | decision_id | notes
```

关键判断分开记录：`fit_to_problem`、`evidence_strength`、`complexity_cost`、`validation_readiness`。

可选文件：`model_registry.md`、`model_candidate_cards.md`、`model_decision_brief.md`、`model_decisions.jsonl`、`model_validation_plan.md`、`model_open_questions.md`。只有跨会话、用户要求留痕、完整审计或最终交付时才生成。
