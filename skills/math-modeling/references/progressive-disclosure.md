# Progressive disclosure

Never preload the workflow. Load capability from the user's current intent outward.

## Layer 0 — Router

只知道：用户现在想做什么、手头有哪些材料、属于哪个角色。
禁止：完整阶段图、stage registry、process-freezer、全部 specialist 清单当作本轮 SOP。

入口：`skills/math-modeling/SKILL.md`。确定性分流：`scripts/route_role.py`（高置信度提示；无 `current_role` 时 `continue_local` / `检查图` / `数值` 返回 `unknown`，不要猜 modeler）。

## Layer 1 — Role guide

确定角色后读取对应 `references/roles/*.md`。
只包含该角色职责、何时调用哪些 specialist、哪些决定属于人类。

## Layer 2 — Specialist

只加载当前任务需要的 skill。Modeler 需要文献时再读 `modeling-literature-evidence`，不要把 assumption/data/experiment 一并打开。

## Layer 3 — Reference / tool

specialist 真正执行具体检查时再读其 `references/` 或运行脚本。例如 citation 核验才读 DOI 规则；实际导出图才读 figure 规格。

## 开销约束

一次局部请求（续写一问、改摘要、解释一个符号）合理加载：

```text
math-modeling + 一个角色 + 0~2 个 specialist
```

不合理：rules → topic → literature → familiarization → data → model → experiment → writer → reviewer。

## 落盘

只在跨会话、重要人类决策、结果/模型将成为下游输入、最终提交/审计时写文件。
