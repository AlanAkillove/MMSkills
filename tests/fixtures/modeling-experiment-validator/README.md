# `modeling-experiment-validator` fixtures

这些脱敏片段测试实验注册、基线公平性、泄漏、敏感性/不确定性、失败记录和复现边界。

- `positive-registered-comparison.md`：问题、基线、切分、种子、输出和范围完整；
- `positive-constraint-check.md`：优化结果有可行性和边界验证；
- `negative-best-run-only.md`：只报最好运行；
- `negative-posthoc-split.md`：反复查看测试集后改方案；
- `negative-missing-seed-and-output.md`：缺版本/种子/输出 hash；
- `negative-robustness-claim.md`：少量场景被写成稳健；
- `negative-no-baseline.md`：没有公平对照；
- `negative-failed-run-deleted.md`：删除失败结果；
- `negative-paper-output-conflict.md`：论文、图表和实际输出不一致；
- `expected-behavior.md`：状态、范围和人工确认。
