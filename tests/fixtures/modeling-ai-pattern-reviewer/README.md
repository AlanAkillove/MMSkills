# `modeling-ai-pattern-reviewer` fixtures

这些 fixture 测试“可观察信号 + 证据边界”，不测试 AI 来源归因。

- `positive-discipline-not-template.md`：标准章节和必要重复不应被误报。
- `positive-topic-specific.md`：即使有正式句式，只要题目特征和证据真实，不能贴模板标签。
- `negative-generic-contribution.md`：可替换到其他题目的贡献/展望模板。
- `negative-uniform-paragraphs.md`：每个子问相同节奏且缺少独特证据。
- `negative-high-register-packaging.md`：高承诺术语包装普通操作。
- `negative-claim-evidence-detach.md`：语言很完整但主张与证据断链。
- `negative-defensive-statement-cluster.md`：重复自我免责但没有新增范围、证据或条件。
- `positive-required-boundary.md`：有效的适用范围和验证边界不应被误报或删除。
- `negative-unauthorized-similarity.md`：未经授权的跨论文比较应被阻止，而不是输出相似度结论。
