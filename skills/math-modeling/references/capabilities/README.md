# Capability Index (L1.5)

这一层解决懒加载悖论：不把完整 Skill 读进上下文，但仍要让 Agent **发现**自己还需要谁。

它不是又一份可选文档。确定角色后必须进入决策路径：

1. 先看角色指南里的问题维度表；
2. 再运行 `scripts/route_capabilities.py`（`route_role.py` 会调用它）；
3. 只对命中的最小集合加载完整 `SKILL.md`。

`mandatory_consideration` 表示候选阶段不能忘掉，不表示必须跑完整流程。
Working set 只缓存角色、最近能力和 artifact 指针，不缓存 Skill 正文；显式换任务时失效。

质量策略（audit / review / challenge、artifact 成熟度）见 [`quality-policy.yaml`](quality-policy.yaml)。执行器是 `scripts/resolve_quality.py`，不是 workflow 引擎，也不新增公开 Skill。跨角色能力见 [`shared.yaml`](shared.yaml)。
