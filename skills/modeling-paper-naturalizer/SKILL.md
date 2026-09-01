---
name: modeling-paper-naturalizer
description: "在锁定数字、公式、引用、术语、主张和题目特征后，将数学建模论文的模板化中文表达改得自然、直接、连贯且保留作者意图。用于诊断、最小改写、段落重构和修稿后保真核对；不承诺规避检测器、不改核心模型或结论。"
---

# 数学建模论文自然化修稿

本技能把“去 AI 味儿/降模板化”解释为学术表达自然化和信息保真，不以规避任何检测器为功能目标。可以改结构、句式和空话，但不能改题意、模型、数据、公式、数字、引用、术语含义、因果强度或结论边界。

## 何时使用

中文段落自然化、模板化诊断后修稿、术语/证据已冻结后的语言调整。不要用来补建模、改结论、编造经历，或在主张未锁定时全篇改写。

## 硬约束

- 数字、单位、变量、公式、代码、引用键、图表/章节编号和文件名锁定；不全局替换术语。
- 不删除真实失败、局限、必要合规声明或题目要求的固定结构。
- 不用同义词拼贴、故意口语化或虚构细节制造人味。
- P0（保护内容或题意被改、无法核对前后是否相同）和 P1（主张强度/范围变化）未关闭时，不得声称保真完成。
- `human-confirmed` 必须有确认人、日期、范围和 `decision_id`。

## 默认怎么帮用户

先直接改用户指定的段落或回答当前诊断问题。默认不先读全套问题地图/假设账本/证据矩阵，也不先生成三份文件。缺材料时仍可局部修订，但要标明保真边界。

用户未指定时：方法/结果/公式用 `minimal-edit`；空泛引言可用 `paragraph-rebuild`；高风险先 `diagnose-only`。

只有跨会话、用户要求留痕、`working_depth=full` 或最终交付时，才落盘 `revised_text.md`、`revision_log.md` 和 `preservation_report.md`。模式、保护清单、五步流程和防御性声明处理见 references。

完整协议见 [revision-contract.md](references/revision-contract.md)、[naturalization-patterns.md](references/naturalization-patterns.md)、[protected-syntax.md](references/protected-syntax.md)、[recommended-workflow.md](references/recommended-workflow.md)、共享的[防御性声明处理协议](../../references/defensive-statement-protocol.md) 和 [research-basis.md](references/research-basis.md)。
