# `modeling-claim-evidence-audit` fixtures

这些 fixture 测试主张强度和证据边界，不代表真实论文或竞赛结论。

- `positive-within-scope.md`：描述性和限定范围内的比较主张有对应证据。
- `positive-limited-claim.md`：只在测试场景成立的结果应保留边界。
- `negative-causal-overclaim.md`：相关图表被写成因果结论。
- `negative-optimality-overclaim.md`：候选算法中的最好值被写成全局最优。
- `negative-robustness-overclaim.md`：单一参数设置被写成鲁棒。
- `negative-accuracy-mismatch.md`：训练集指标/不一致指标被写成泛化准确性。
- `negative-evidence-conflict.md`：论文、代码和图表结果互相冲突。
