---
name: modeling-paper-architect
description: "从题意、假设、差异化账本、模型注册、实验和主张证据搭建数模论文的章节/段落/图表契约；让每一节服务明确问题和证据，不先套模板，不替作者编写核心内容。"
---

# 数学建模论文结构架构

在写作前或重构时，把题目子问题映射到主张、证据、章节和图表。**Visual argument plan 是一等对象**：正式写整篇前先确定每条承重主张用哪张图/表回答什么读者问题，再让 Writer 围绕这些证据写。提供可调整的建议，不把蓝图变成审批流程，也不代替选模型、补实验或直接完成正文。

## 何时使用

搭建目录和论证主线、重组已有草稿、对齐摘要/结论与证据。不要在没有任何可核对材料时生成完整论文，也不要用固定目录证明质量。

## 硬约束

- 不从固定目录反向填充题目，不为每节强行套三段式。
- 不编造题目事实、模型、数字、实验、引用或创新点。
- 题意、关键假设、模型取舍、数据处理、实验结论和最终摘要/结论是人工确认门。
- P0：结构会改题意或把未确认内容写成定论。P1：主要主张无承重段落，或摘要/结论与验证范围冲突。

## 默认怎么帮用户

先直接回答当前结构问题：这一节要回答哪一问、缺哪条证据、相邻节怎么接。默认不先生成五份蓝图文件。

一个 `section_contract` 仍应能说出：该节任务、主张/证据、段落功能、不应出现的填充。整篇写作还应有 `visual_plan`：每张拟进正文的图/表写清 `reader_question`、支撑的 claim、比较什么、放在哪一节之后。不要写“曲线应该先降后升”这类预设结论。未规划的运行图默认 `diagnostic`，不能因为看起来不错就进正文。

CUMCM 中文写作 profile 下，不要规划单独的「问题重述」章；必要对象和任务并入问题分析或各问建模。

需要交接或最终采用时，再落盘 `paper_blueprint.md`、`section_contracts.yaml`、`argument_map.md`。承重单元成熟度只用 `draft` / `candidate` / `reviewed` / `accepted-for-assembly`；写完最多称为 candidate，独立审阅前不得说“这一部分已经完成且质量良好”。

完整字段见 [blueprint-contract.md](references/blueprint-contract.md)、[argument-mapping.md](references/argument-mapping.md)、[section-and-paragraph-functions.md](references/section-and-paragraph-functions.md)、[recommended-workflow.md](references/recommended-workflow.md) 和 [research-basis.md](references/research-basis.md)。
