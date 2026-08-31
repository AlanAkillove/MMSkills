# `modeling-paper-reviewer` fixtures

这些脱敏片段只测试审稿角色的边界与 finding 契约，不代表完整论文或竞赛评分标准。

- `positive-clear-scope.md`：题意、模型、结果边界清楚，不应为了凑问题而误报；
- `negative-question-mismatch.md`：论文遗漏题目条件/子任务；
- `negative-assumption-silent.md`：关键独立性假设未说明；
- `negative-model-evidence.md`：复杂模型名称没有适配理由或基线；
- `negative-causal-overclaim.md`：观察性结果被写成因果/最优结论；
- `negative-results-repro.md`：只有截图/最好结果，缺少复核入口；
- `negative-reader-path.md`：变量、图表和结论之间存在回读摩擦；
- `negative-unauthorized-similarity.md`：相似性线索没有授权范围，必须阻断比较而不是定性；
- `expected-behavior.md`：记录应观察到的审稿行为。
