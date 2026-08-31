# 跨审查 finding 协议

审稿、主张—证据、术语、图表、AI 模板化、反同质化和阅读体验 skill 关注点不同，但它们经常观察到同一个底层问题。每个 skill 可以保留自己的报告和透镜字段，跨 skill 交换时必须使用 `schemas/finding.schema.json` 的共同 envelope。

## 记录规则

每条 finding 至少提供：

- 稳定的 `finding_id` 和 `source_skill`；
- 一个 `finding_type`、`P0–P3` 严重性和 `open/needs_human/resolved` 等状态；
- 可定位的 `evidence_anchors`，每个锚点说明位置和证据状态；
- 可观察事实 `observation`、审查解释、影响和可验收的 `acceptance_test`；
- `deduplication.canonical_issue_key` 和 `deduplication.relation`；
- 人工状态和 `decision_id`（只有已经确认时才填写确认 ID）。

`finding.schema.json` 是字段的机器契约；各 skill 的 Markdown 表格是角色特有字段的补充，不得把补充字段当作共同必需字段。

## 去重与合并

1. 每个专项审查开始前先读取当前 `finding_register.jsonl`（没有则明确记录“尚未建立”）。
2. 新发现先按“底层问题 + 版本范围”生成 `canonical_issue_key`，再比较已有 finding 的锚点、主张/术语/图表 ID 和证据状态。
3. `new` 表示没有对应底层问题；`duplicate` 表示同一问题和同一证据，不得新建第二条开放问题；`supplement` 表示提供了新的透镜或证据；`upgrade/downgrade` 表示严重性或范围有证据变化；`conflict` 表示事实、范围或严重性不能合并。
4. 合并时保留所有原始 `finding_id`、来源 skill、证据锚点和版本；不得因为“看起来相同”静默删除或覆盖较早记录。
5. 只有在没有事实冲突、且人工确认了处理方式后，才把 canonical finding 标记为 `resolved`。自动脚本只能合并记录和报告冲突，不能替人关闭问题或提升结论。

## 与报告的关系

`review_report.md`、`terminology_audit.md` 等是面向人的投影；`review_findings.jsonl`、`figure_table_findings.jsonl` 等是专项输入。编排器负责把专项记录合并为 `finding_register.jsonl`，自然化和终检只读取已接受的范围，不把多个重复意见叠加成虚假的问题数量。

长论文分块时，下一块沿用 `finding_id`、`canonical_issue_key` 和版本 hash；上下文压缩不得重新命名同一个底层问题。若旧记录缺少锚点或无法恢复，标记为 `unknown`/`needs_human`，而不是补写“已核实”。
