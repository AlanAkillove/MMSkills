# Progressive disclosure

Never preload the workflow. Load capability from the user's current intent outward.

现有懒加载解决的是“不要读太多”。L1.5 解决的是“在不读太多的情况下，仍然知道自己还需要读什么”。

```text
L0  Global Kernel     math-modeling/SKILL.md
L1  Role Router       roles/*.md + route_role.py
L1.5 Capability Index 问题维度卡片 + route_capabilities.py   ← 高召回
L2  Full Specialist   SKILL.md                              ← 高精度
L3  Reference / Tool  references/、scripts/
        ↖ Session Working-Set Cache（可选，不缓存 Skill 正文）
```

## Layer 0 — Kernel

只知道：用户现在想做什么、手头有哪些材料、属于哪个角色。
禁止：完整阶段图、stage registry、process-freezer、全部 specialist 清单当作本轮 SOP。

入口：`skills/math-modeling/SKILL.md`。确定性分流：`scripts/route_role.py`（高置信度提示；`unknown` 表示脚本不能判断，先用会话上下文和当前 artifact，再问用户；不要猜 modeler）。

## Layer 1 — Role guide

确定角色后读取对应 `references/roles/*.md`。角色指南必须带问题维度表，不能只有一行 Skill 名称映射。

## Layer 1.5 — Capability Index

自动进入决策路径，不是可选附录。数据：`references/capabilities/{role}.yaml`。脚本：`scripts/route_capabilities.py`。

路径：`query → task facets → capability retrieval → candidate specialists → minimal coverage`。
`mandatory_consideration` 保证关键能力进入候选；真正加载哪些完整 Skill 仍由当前任务决定。产物跨越质量边界时读 `quality-policy.yaml`：审计可由工具/同上下文完成，审阅与挑战必须独立 Subagent。

## Layer 2 — Specialist

只加载当前任务需要的 skill。Modeler 需要文献时再读 `modeling-literature-evidence`，不要把 assumption/data/experiment 一并打开。

## Layer 3 — Reference / tool

specialist 真正执行具体检查时再读其 `references/` 或运行脚本。例如 citation 核验才读 DOI 规则；实际导出图才读 figure 规格。

## 开销约束

一次局部请求（续写一问、改摘要、解释一个符号）合理加载：

```text
math-modeling + 一个角色 + 0~2 个 specialist
```

这是典型局部任务预算，不是 Router 硬上限。明确的复合任务按 capability coverage 选择最小集合。这仍不是全流程预加载。

最终成稿审阅必须使用独立 Subagent：重新读取磁盘上的 `.tex`/`.pdf`，不把写作 rationale 当作质量证据。承重章节完成后做 scoped review；写整篇前考虑 visual plan。未规划图保持 diagnostic。

不合理：rules → topic → literature → familiarization → data → model → experiment → writer → reviewer。

## Working set

可记录当前角色、最近能力和 artifact 指针。显式换角色、换问题维度、或用户说“重新建模”时失效。不要因为 Skill 被调用就创建该文件。

## 落盘

只在跨会话、重要人类决策、结果/模型将成为下游输入、最终提交/审计时写文件。
