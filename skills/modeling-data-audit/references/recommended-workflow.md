# 数据审计推荐工作流

本文件是按需读取的详细协议。查看缺失值、列含义或一张表的口径时，不要从头跑完整六步。原始数据不覆盖、来源与授权不伪造、泄漏风险不隐瞒是硬约束。

## 1. 建立不可覆盖的原始层

原始文件只读保存并记录 hash；任何清洗/中间结果写入新路径。若只有处理后文件，记录 `raw_unavailable`。

## 2. 建立数据字典与口径表

逐列记录名称、含义、类型、单位、范围、缺失编码、来源、时间/实体键、角色和论文使用位置。同名列口径不同时建立冲突项。

## 3. 审计质量与处理决定

报告缺失/异常/重复的可观察统计，再记录候选处理。不得以结果好坏作为唯一理由。

## 4. 审计时间/实体切分与泄漏

对每个特征标注生成时点；时间预测优先按时间切分，实体相关样本按实体分组。泄漏疑点需要代码/数据证据或标为 `unknown`。

## 5. 回查论文、代码、实验

核对样本量、变量/单位、清洗规则、切分、指标、图表数字和代码入口。论文与代码不一致时独立记录。

## 6. 人工确认

缺失/异常处理、外部数据、目标定义、样本切分、泄漏处置和影响结论范围的决定必须由人确认。

需要落盘时的最低记录：

```text
data_id | source_file | table_or_column | semantic_role | unit | source_anchor
version_hash | time_entity_scope | missing_encoding | quality_observation
transformation | leakage_status | reproducibility_status | impact
decision_needed | human_status | decision_id | notes
```

可选文件：`data_manifest.yaml`、`data_dictionary.md`、`data_audit.md`、`data_decisions.jsonl`、`data_reproduction.md`。
