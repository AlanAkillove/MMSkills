---
name: modeling-figure-designer
description: "从数模论文的题目、主张、数据和读者任务出发，设计并制作清晰、美观、可复现、适合正文排版的图表、模型流程图和多面板图；用于选图、视觉系统、绘图脚本、可编辑源文件和渲染交付，不替代图表事实审计。"
---

# 数学建模论文图表设计与制作

把图表当作论证的一部分来设计。本技能是 **shared capability**：先回答“读者必须看见什么关系”，再决定数据和绘图，而不是编程手顺手出图。这里的“美观”指读者能迅速找到重点、编码与证据角色相符、目标尺寸可读、源文件可回溯。不替代图表事实审计；数值和主张边界由 `modeling-figure-table-auditor` 核对。没有源数据时只能做版式/可读性或非定量结构图。

## 何时使用

规划论文图、重绘拥挤或与主张脱节的图、统一视觉系统、制作流程图。**正式写整篇前应先做 visual-first planning**：模型与主要证据形成后，先 argument map 和图表/表信息设计，再实验出图，再写正文。不要从截图补造结果，不要靠截轴或删点“美化”。

## 硬约束

- 不手工改数值，不把装饰图当证据。
- 颜色/线型不得暗示未证明的因果、显著性或最优性。
- 遇到 P0/P1（隐藏证据、画错约束、与数据/主张不一致）先停美化。
- 没有渲染件时页面状态为 `unassessed`。

## 默认怎么帮用户

先直接回答当前图表问题：这张图让读者比较什么、该用什么图型、现在最大的误读风险。默认不先写全套 brief/storyboard/manifest。

读者应在约五秒内知道图在回答什么。需要制作或交接时，再保留绘图脚本、可编辑源和目标尺寸渲染。

每张图还要有放置角色：`diagnostic`（调试，默认不进正文）、`comparison`、`paper`、`appendix`。成熟度另记 `maturity`：`planned | produced | audited | reviewed | accepted`。`placement=paper` 只表示打算进正文，不表示已经审完。代码运行中未规划的图默认 `diagnostic`，不能因为看起来不错就塞进论文。升级为 `paper` 必须补 visual brief、`evidence_audit` 和独立 fresh-reader visual review。定量图做数据/单位审计；结构/流程/机理图做几何与术语审计。宁可少而承重，不要装饰清单。机械检查用 `math-modeling/scripts/figures/check_figure_placement.py`。promote 前运行 `math-modeling/scripts/resolve_quality.py --artifact-type paper_figure --target-state paper`。

完整协议见 [design-contract.md](references/design-contract.md)、[chart-selection.md](references/chart-selection.md)、[visual-system.md](references/visual-system.md)、[production-and-handoff.md](references/production-and-handoff.md)、[recommended-workflow.md](references/recommended-workflow.md) 和 [research-basis.md](references/research-basis.md)。
