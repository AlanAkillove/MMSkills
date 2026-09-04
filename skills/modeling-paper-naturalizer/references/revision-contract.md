# 自然化修稿保真契约

## 修订前锁定表

```yaml
revision_contract:
  source_manifest_hash: null
  paper_version: null
  scope: null
  mode: signal-targeted
  locked:
    numbers_units: true
    formulas_commands: true
    citations_keys: true
    variables_labels: true
    claims_qualifiers: true
    terminology: true
    figures_tables: true
    assumptions_data_code: true
  author_samples: []
  human_confirmation_required: true
```

如果无法建立锁定表，先降为 `diagnose-only` 或明确写未核对项；不能假定“润色不会改变实质”。

## 修改记录字段

```text
revision_id | location | signal_id | claim_ids | evidence_ids | term_ids | figure_ids | before | after | problem_type | action | protected_content_touched | semantic_change | human_status | decision_id
```

`semantic_change` 使用 `none/possible/confirmed/unknown`。只要不是 `none`，就不能自动视为语言润色完成。

## 三类修订边界

- `language_only`：不改变对象、关系、范围、主张、数字、公式、术语或逻辑；可自动生成草案，但仍需抽查；
- `structure_preserving`：移动/合并/拆分句子或段落，但每条主张、证据和限定条件可回溯；需人工确认；
- `substantive_candidate`：涉及模型、假设、数据、实验、结论或主张边界，只能作为问题记录和候选建议，不能由本技能执行。

## 最低输出记录

`revision_log.md` 至少记录源文件/版本 hash、章节和原文锚点、段落功能、对应的主张/证据/术语/图表 ID、修改前后文本、动作、保护内容是否触碰、`semantic_change`、人工状态、`decision_id` 和未决风险。

`preservation_report.md` 至少报告源版本与修订版本、数字/单位/公式命令/引用键/变量标签的 token 对比、术语和主张—证据映射的对比、图表交叉引用、未读取材料、无法自动判断的差异、P0/P1 阻断项和人工确认状态。若未能执行某项对比，写 `unknown`，不写“已通过”。

## 长文续接

每块记录：论文版本/hash、章节范围、首尾锚点、已保护术语/主张、已完成修订 ID、未决风险和下一块。重启时先核对锁定表与上一块，不要从摘要重新发明术语或改变句意。
