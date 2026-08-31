# 模型选择决策简报

> 面向不熟悉候选模型的团队成员。它压缩阅读路径，不压缩证据和不确定性；不能用作自动选模结果。

## 当前任务

- 题目子问题/任务：
- 目标变量与评价指标：
- 已确认约束和边界：
- 可解释性、时间、算力和数据限制：

## 先看差异

| 方案 | 一句话用途 | 相比基线新增什么 | 主要代价/风险 | 当前状态 |
|---|---|---|---|---|
| 基线 |  |  |  | baseline |
| MOD-0001 |  |  |  | candidate |
| MOD-0002 |  |  |  | candidate |

## 分项评估入口

详见 `model_candidate_cards.md`。这里不填写总分，不写“模型一定更好”或“Agent 推荐采用”。

- 当前最值得先验证的未知：
- 选择该验证的理由：
- 需要补充的题意/数据/资源：
- 各候选的关键反例或失败边界：

## 先做最小理解校验

让团队成员用自己的话回答，而不是只点击默认选项：

1. 每个候选在本题中把什么输入变成什么输出？
2. 每个候选的一个关键假设是什么，失效时会怎样？
3. 每个候选相比基线增加了哪项主要代价或风险？

各候选 `understanding_check`：`not-asked` / `incomplete` / `answered` / `unknown`

## 人类确认问题

1. 我们是否清楚每个候选的输入、输出和本题用途？
2. 我们是否知道每个候选至少一个关键假设和主要失败风险？
3. 我们是否接受为区分候选而进行的最小验证成本？
4. 本轮选择是 `adopt`、`reject`、`continue-validation`、`pause` 还是 `undecided`？

`decision_id`：
`decision_owner`：
`decided_at`：
`human_status`：`needs-human-confirmation` / `human-confirmed` / `unknown`
