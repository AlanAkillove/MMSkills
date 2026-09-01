---
name: modeling-data-audit
description: "审计数模论文使用的数据来源、口径、版本、单位、缺失/异常处理、时间与实体切分、泄漏、授权和可复现性；保留原始数据与决策证据，不为追求结果自动删除或改造数据。"
---

# 数学建模数据审计

## 何时使用

建模前摸底、清洗前检查、预测题切分、或论文/代码/图表口径核对时调用。用户只问“有没有缺失值”时，直接观察并报告，不要升级成完整审计包。

不要在没有数据文件或摘要时推测数据特征，也不要覆盖原始文件。

## 硬约束

- 不覆盖或静默修改原始数据；清洗结果写入新路径，并保留 SHA-256 hash。
- 不编造来源、样本量、权限、单位或清洗结果。程序运行成功不等于数据正确。
- 查看缺失/口径是 explain/explore；删除异常、改切分或让后续模型使用处理后数据，才需要人类确认（`human_status`）。
- 不默认 i.i.d.、正态、无泄漏或代表性成立。泄漏未检查时写 `unknown/unverified`，不能写成“没有泄漏”。
- 不在未授权范围内传播个人、敏感、未公开赛题或队伍数据。

## 默认怎么帮用户

先回答用户眼前的问题。完整审计可按需覆盖六个维度：`provenance`、`semantics`、`quality`、`transformation`、`split_leakage`、`reproducibility`。局部任务只取相关维度，未检查的不得写成已确认。

默认不生成五份产物。只有跨会话、用户要求留痕、`working_depth=full` 或最终交付时，才落盘 manifest、字典、`data_audit.md` 和决定记录。

## 停止条件

- `P0`：来源/授权不明却准备提交，原始数据被覆盖且无法恢复，或明显未来信息泄漏。
- `P1`：口径/单位冲突，或处理/切分会改变主要结论。

详细字段见 [data-contract.md](references/data-contract.md)、[quality-and-missingness.md](references/quality-and-missingness.md)、[split-and-leakage.md](references/split-and-leakage.md)、[recommended-workflow.md](references/recommended-workflow.md) 和 [research-basis.md](references/research-basis.md)。
