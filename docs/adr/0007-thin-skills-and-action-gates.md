# ADR 0007：瘦身技能、动作门与排版/内容分离

- 状态：accepted
- 日期：2026-09-01
- 适用版本：0.2.1

## 背景

0.2.0 把用户意图做成了路由优先级，但仍用 `depends_on` 阻断探索；SKILL.md 过长，Agent 容易把推荐流程执行成 SOP。真实回放还显示默认 TeX 章节骨架会诱导固定论文结构，而列表密度的绝对阈值会误伤合理的假设/步骤列表。

## 决策

1. 阶段依赖改为三层：`execution_requires`（没有这些材料则无法执行当前任务）、`adoption_requires`（探索可以开始，adopt/freeze/submit 前必须满足）、`recommended_after`（质量建议）。`depends_on` 仅作为 `execution_requires` 的兼容别名。
2. 人工确认从“整个 stage 是否有门”转向动作级别：`explain < explore < propose < execute_reversible < adopt < freeze/submit`。查看数据、比较模型、写暂定草稿不硬阻断；删除异常、冻结核心模型、覆盖文件或提交才硬确认。
3. 用户可感知参数收敛为 `working_depth = light | standard | full`。`collaboration_mode` 与运行档位仍可存在，但只作为兼容别名或产物/审查偏好，不再叠出另一套工作流引擎。
4. 常驻 `SKILL.md` 保持薄：触发条件、少量硬约束、默认先直接回答用户。完整 SOP、字段表和账本移入 `references/`。默认不落盘；跨会话、用户要求留痕、`full` 或最终交付时才写 ledger。
5. 默认 TeX 只负责排版（`templates/tex/main.tex` + `body.tex`）。原正文章节骨架移到 `examples/generic-paper-scaffold.tex`，明确不是默认入口。
6. 成文检查的列表风险按章节位置判断：问题分析、路线、结果解释、讨论、结论中连续使用列表才提示；不以全文 `\item` 计数作为风格禁令。
7. 增加脱敏的论文回归样本和人工量表，覆盖摘要、段落、列表、过程痕迹等可观察差异；不计算与任何成熟论文的相似度，也不把成熟论文写成必须模仿的模板。

## 保留的硬边界

不得编造数据、文献、实验或 AI 使用历史；不得静默修改已确认的模型/假设/结果；不得把未知写成确定结论；最终模型、关键假设、核心结论和投稿版本仍由人类确认。

## 后果

- 用户说“比较几个模型”时，`model_architect` 可以在文献/熟悉/完整数据审计尚未通过时进入探索；
- 要把模型写成已采用时，仍需要题意范围（`adoption_requires: problem_intake`）；
- Agent 更可能先回答用户，而不是先生产 question_map 和账本；
- 旧状态若只写 `depends_on` 或 `collaboration_mode`，运行时仍可映射到新字段。
