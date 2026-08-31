# Expected behavior

1. 编排器只生成计划，不改论文、代码、数据、模型和核心结论。
2. 依赖未通过时，下游不能被标为 ready；blocked/stale/superseded 不能作为通过条件。
3. 并行分支必须独立产出和合并，人工门不能因“没有 needs_human 字段”而被默认为通过。
4. 未知 stage、非法状态、schema 缺失字段和缺失结构应被拒绝，而不是静默忽略。
5. 计划必须提醒读取最新 snapshot/hash、人工确认和禁止越权动作。
6. 没有 ready 阶段时，安全动作应指向人工门或阻断项，不应建议打开不存在的 ready 输入。
7. `contest-fast` 与 `research-full` 必须产生不同的 effective stage policy；canonical 依赖不得被改写。
