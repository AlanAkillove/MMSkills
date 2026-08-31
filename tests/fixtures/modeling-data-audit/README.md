# `modeling-data-audit` fixtures

这些脱敏片段测试数据证据、口径、处理决定和泄漏边界，不代表具体统计结论。

- `positive-traceable-data.md`：来源、单位、处理、时间切分和代码入口可追溯；
- `negative-overwrite-raw.md`：原始数据被覆盖；
- `negative-unit-drift.md`：同名列/变量单位和口径冲突；
- `negative-silent-outlier-delete.md`：为提高指标静默删异常；
- `negative-time-leakage.md`：未来信息和全数据预处理泄漏；
- `negative-entity-leakage.md`：同一实体跨训练测试；
- `negative-unknown-source.md`：外部数据来源/授权不明；
- `negative-paper-code-mismatch.md`：论文、代码和图表不一致；
- `expected-behavior.md`：未知状态、人工决定和停止条件。
