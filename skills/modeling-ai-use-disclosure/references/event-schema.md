# AI 使用事件模式

本模式把“会话中发生过一次 AI 交互”与“最终论文采用了什么”分开。它是内部审计台账，不等于把原始会话全文复制给赛事组织者。

## 事件最小记录

每行一个 JSONL 事件，字段建议如下。字段值不能由模型凭空补齐；未知值使用 `unknown`，不使用空字符串掩盖缺失。

| 字段 | 含义 | 允许值/要求 |
| --- | --- | --- |
| `event_id` | 稳定事件 ID | 不含姓名和密钥，创建后不随措辞修改而变化 |
| `event_family` | 交互所属事件族 | `problem_understanding`、`literature_or_source`、`solution_candidate`、`code_or_computation`、`figure_or_table`、`result_interpretation`、`structure_planning`、`language_polish`、`format_check`、`disclosure` 或 `other` |
| `source_ids` | 原始证据 | 一个或多个 `source_id`；至少有一个定位或明确为 `E0` |
| `stage` | 论文/项目阶段 | `topic_selection`、`problem_intake`、`literature_evidence`、`problem_familiarization`、`assumption`、`data`、`model`、`experiment`、`writing`、`revision`、`formatting`、`disclosure`、`unknown` |
| `tool` | 工具身份 | `name`、`developer`、`version_or_model`、`identity_status` |
| `purpose` | 当次使用目的 | 具体到任务，不写“辅助论文”这类空泛词 |
| `input_scope` | 提供给 AI 的材料范围 | 文件/段落/问题/数据的摘要；不得保存秘密和未授权原文 |
| `output_summary` | AI 输出摘要 | 只摘要可披露内容；原始输出不可见时标 `summary_only` |
| `adoption` | 采用关系 | `not_adopted`、`partially_adopted`、`adopted_after_edit`、`adopted_as_is`、`unclear`、`not_applicable` |
| `human_modification` | 人工修改 | `none`、`minor`、`substantial`、`rewrote`、`unknown`；必须配简短说明 |
| `human_verification` | 人工核验 | `not_needed`、`checked_against_source`、`recomputed`、`rerun_code`、`cross_checked`、`author_reviewed`、`pending`、`unknown` |
| `substantive_risk` | 内容实质风险 | `none`、`language_only`、`supporting`、`modeling_relevant`、`core_decision`、`conclusion_relevant`、`unknown` |
| `evidence_level` | 证据强度 | `E3` 原始可见；`E2` 可核查摘要；`E1` 最终产物间接线索；`E0` 口述/推测 |
| `record_status` | 记录状态 | `confirmed`、`proposed`、`partial_history`、`conflict`、`unknown`、`privacy_blocked` |
| `artifact_refs` | 最终产物关联 | 论文章节/图表/代码/数据的稳定 ID；没有关联则 `[]` |
| `rule_refs` | 规则映射 | 赛事 profile 中的规则 ID；缺 profile 时 `policy_unknown` |
| `notes` | 补充说明 | 说明证据不足、冲突和下一步确认，不写隐藏提示或隐私 |

## 工具身份

`tool.identity_status` 使用 `confirmed`、`partially_known`、`unknown` 或 `conflict`。版本、模型、插件和调用渠道是不同事实：例如“ChatGPT 网页端”不能自动写成某个模型版本；“模型版本未知”不能被当前日期下的默认版本替换。

## 人工控制与规则状态

`substantive_risk` 与赛事规则状态是两个轴：语言润色可能内容风险低但仍需披露；一次未采用的模型建议内容风险高但最终论文没有采用。另设：

- `rule_status`: `required`、`recommended`、`not_applicable`、`unknown`、`conflict`；
- `human_confirmation`: `pending`、`confirmed`、`rejected`、`not_available`；
- `verification_note`: 具体说清楚核验依据，例如“重新运行脚本并与表 3 比较”，不要只写“已核对”。

## 事件族去重

相邻追问、同一任务的多次微调可共享一个 `event_family`，但不应掩盖不同结果：

1. 先按来源分组，再按阶段、目的和产物关联判断是否是同一事件族；
2. 只合并内容和人工决定均相同的重复调用；
3. 一次调用产生多个独立建议时，可以一个事件配多个 `output_refs`，也可以拆成多个事件，但要在 `notes` 说明拆分依据；
4. 事件合并不等于提高证据等级，合并后的等级取能支持该事件的最高可靠等级，并保留全部 `source_ids`；
5. 不能为了满足“每项都有提示词”而编造被截断的原文。使用 `prompt_status: complete|partial|summary_only|unavailable` 明示完整程度。

## 最终审计前的必答问题

每条进入 PDF 的事件都应能回答：

1. 这是原始记录、摘要、最终产物线索还是作者口述？
2. AI 提议什么，团队实际采用什么？
3. 谁作出核心决定，改了什么，怎样验证？
4. 它影响的是语言、支撑材料、模型路径、数据/实验还是结论？
5. 如果无法回答，是否被标为未知并进入人工确认队列？
