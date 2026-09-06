---
name: modeling-terminology-auditor
description: "在建模阶段建立共享术语与符号表，并在成稿后检查论文是否偏离已确定的概念语言。用户检查术语规范、用词漂移或统一叫法时应考虑本技能；识别同义漂移、生造高级术语和高承诺词语滥用。用于 establish 与 audit 两种模式，不做机械同义词替换。"
---

# 数学建模术语规范

让读者清楚同一个对象叫什么。建模阶段用 `establish` 逐步形成 `terminology_table.md`；写作/终检用 `audit` 做 drift regression，不再从头重建账本。

术语状态：`standard` / `project-defined` / `candidate` / `alias` / `deprecated` / `unknown` / `conflict`。不为普通事实生造高级感名称。

## 何时使用

- `establish`：理解题目、读文献、定模型时登记中英文规范名、定义、符号和单位。
- `audit`：成稿或修稿后，把正文/图注/代码与已有术语表比较。

不要只改拼写、不要全篇机械替换、不要在用户要求“全部换成高级词”时执行该目标。

## 硬约束

- 不机械全局替换；不改变数字、公式、单位、引用或主张强度。
- 同义漂移、异义复用、层级漂移必须落到具体概念，不能只说“不统一”。
- 高承诺词（鲁棒、最优、机制、普适等）要有定义或证据，否则回退直接描述。
- 不替 Research Chair/用户决定新术语是否代表创新。
- 解释一个已有符号时不要落盘；用户明确“全文统一叫 X”时才更新术语表。
- 标准术语在正文中重复出现不是 AI-pattern；那是本技能的正常现象。未登记高承诺词或生造包装名才进入 audit。

## 默认怎么帮用户

先直接回答当前用词问题。`establish` 只改用户触及的几行；`audit` 默认对照 `terminology_table.md`（若只有旧的 `terminology_ledger.md` 则沿用）。需要留痕或最终交付时再写 audit 报告。

机械别名/过期名扫描可用 `scripts/check_terminology_drift.py`。它只检查表中列出的 deprecated/ambiguous aliases 和少量写死的包装词模式，是 **mechanical drift scan**。脚本输出 `OK` 不表示全文没有 AI 生造术语、高承诺词或概念层级漂移；那些仍须由 LLM 对照术语表做语义审查。字段见 [terminology-schema.md](references/terminology-schema.md)；新词判据见 [term-decision-rubric.md](references/term-decision-rubric.md)；跨产物核对见 [cross-artifact-consistency.md](references/cross-artifact-consistency.md)；模式细节见 [recommended-workflow.md](references/recommended-workflow.md) 和 [research-basis.md](references/research-basis.md)。
