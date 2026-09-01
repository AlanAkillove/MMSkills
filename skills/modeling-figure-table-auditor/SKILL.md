---
name: modeling-figure-table-auditor
description: "审计数模论文图表的证据角色、数据/单位/图例/标签、正文解释、代码来源、数值一致性、可读性和复现入口；不把装饰图当证据，不替作者改数据或夸大结论。"
---

# 数学建模图表审计

逐张图/表回答：它服务哪个问题、来自什么数据、支撑哪条主张、读者应看什么、能否复核。检查数据/单位/图例/标签、正文解释和数值一致性。不把装饰图当证据，不改原始数据。

## 何时使用

成品图表审计、图表与主张对齐、渲染后可读性检查。不要从图片反推精确数值，不要替作者挑最好图。

## 硬约束

- 不编造来源、误差、样本量或显著性。
- 不为观感删不利点或截断轴。
- P0：图表/正文/数据关键数字冲突或误导核心结论。P1：单位不明或图表不支撑主要主张。
- 没有渲染件时视觉状态为 `unassessed`。

## 默认怎么帮用户

先直接回答当前核对问题：这个数字从哪来、单位对不对、正文有没有把局部结果写成普适。默认不先生成五份审计材料。

核对主张时保留 `claim_ids` 和 输出 hash。需要留痕或最终采用时，再写 registry、audit 和 findings。

完整协议见 [figure-contract.md](references/figure-contract.md)、[data-and-claim-checks.md](references/data-and-claim-checks.md)、[visual-checks.md](references/visual-checks.md)、[recommended-workflow.md](references/recommended-workflow.md) 和 [research-basis.md](references/research-basis.md)。
