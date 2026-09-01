# 实验验证的推荐工作流

本文件是按需读取的详细协议，不是每轮必须执行的 SOP。用户只要解释已有结果时，先做主张核对；要把结果写入论文结论时，再补齐设置、失败和复现信息。

## 常用验证类型

`baseline_comparison`、`holdout_or_cross_validation`、`feasibility_or_constraint`、`sensitivity`、`robustness`、`ablation`、`uncertainty_or_repetition`、`edge_case`、`reproduction`。选择哪类由题目和主张决定。

## 需要完整登记时的顺序

1. 先写验证问题、比较对象和成功/失败判据。
2. 固定数据/模型/代码版本、切分、参数、随机种子和指标。
3. 保留全部预先定义的对照和失败，不只保存最好运行。
4. 报告范围、不确定性和失败边界；没有设计时不补显著性。
5. 回归图表、论文数字和主张矩阵。人工确认后才可标 `verified`。

## 需要落盘时的最低交付

`experiment_registry.jsonl`、`validation_matrix.md`、`reproduction_manifest.yaml`。每条记录保留 `output_hashes` 和 `validation_status`。
