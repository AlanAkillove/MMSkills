# 题目熟悉 skill 的设计依据

- 历史会话中，团队在正式建模前反复要求先读懂题面、结构和背景，并在每轮讨论中纠正对对象关系的误解；因此本 skill 把复述—核对—checkpoint 设为独立阶段。
- `modeling-problem-intake` 的证据状态和图示边界被用于背景地图；本 skill 不把可视化讲解变成新的题面事实。
- `modeling-literature-evidence` 原有的来源身份、定位、支持范围和不支持范围契约被扩展为 orientation 模式；文献学习与引用核验仍保留不同目标。
- `modeling-model-architect` 的人工模型决策门被前置依赖保护：理解确认只解锁后续建模讨论，不直接产生 adopted 模型。
- `docs/research/historical-project-findings.md` 和 `docs/research/source-register.md` 是项目级设计输入；它们不构成某一具体题目的背景答案，也不授权复制历史项目内容。
