---
name: modeling-experiment-validator
description: "把数模论文中的计算、仿真、对照、敏感性和稳健性分析登记为可复核实验；核对数据/模型/指标/随机设置/输出与主张是否一致，不替作者挑最好结果或把实验观察写成证明。"
---

# 数学建模实验与验证

把“有结果”转成可复核实验：问题、设置、基线、输出、失败和范围。不替作者挑最好结果，不编造运行，不把一次观察写成证明。

## 何时使用

候选比较、基线/消融、敏感性、修稿后回归、代码—论文核对。没有代码/数据时不要补写结果。数据清洗交给 `modeling-data-audit`，最终选模交给 `modeling-model-architect`。

## 硬约束

- 不删除失败运行、负结果或不利基线。
- 不反复调参后只保留测试集最好结果。
- 不能运行时状态必须是 `unverified/unknown`。
- `validation_status` 的 `verified` 只表示输入/输出/范围已核对，不等于模型真理。
- `result_verification`（审计：算对了吗、划分有没有泄漏）不等于 `result_interpretation_review`（审阅：这些数能否支持准备写入论文的主张、baseline 是否公平、能不能写“明显提高”）。冻结 claim-bearing 结果前，后者由独立 Subagent 完成。
- P0：输出不可追溯、关键结果冲突或明显泄漏。P1：只报最好结果或基线不公平。

## 默认怎么帮用户

先直接回答当前问题：这个结果支持哪条主张、缺什么设置、失败有没有留下。默认不先写五份实验材料。

解释已有结果时，先做结果—主张核对。新增实验或把结果当最终证据时，再补齐输入、随机设置和 `output_hashes`。常用类型包括 `baseline_comparison`、`sensitivity`、`uncertainty_or_repetition`；不是每个模型都需要全部类型。没有有意义对照时不要编造 baseline。普通试算只写轻量 `run_summary.json`，不要每轮实验报告；正式写稿前才 freeze `results_snapshot`。

只有跨会话、留痕、`full` 或最终交付时，才落盘 registry、验证矩阵和复现清单。

完整字段见 [experiment-contract.md](references/experiment-contract.md)、[validation-matrix.md](references/validation-matrix.md)、[uncertainty-and-sensitivity.md](references/uncertainty-and-sensitivity.md)、[reproducibility.md](references/reproducibility.md)、[recommended-workflow.md](references/recommended-workflow.md) 和 [research-basis.md](references/research-basis.md)。
