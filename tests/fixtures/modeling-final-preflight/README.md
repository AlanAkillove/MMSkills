# `modeling-final-preflight` fixtures

这些脱敏片段测试最终预检的状态聚合和阻断边界，不是任何赛事的自动评分器。

- `positive-ready-for-human-signoff.md`：检查完成但仍需人工签核；
- `positive-frozen-manifest.md`：输入/输出 hash 与签核齐全后可冻结；
- `negative-profile-stale.md`：规则过期；
- `negative-p1-claim-open.md`：主张证据 P1 未关闭；
- `negative-unknown-render.md`：无渲染件；
- `negative-ai-disclosure-open.md`：AI 详情字段/人工核验缺失；
- `negative-support-identity.md`：支撑材料匿名阻断；
- `negative-version-conflict.md`：论文/代码/数据版本冲突；
- `expected-behavior.md`：状态优先级和签核规则。
