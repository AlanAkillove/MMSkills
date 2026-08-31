# AI 工具使用详情技能：设计草案

> 状态：Draft。本文给出调研和接口设计；最终字段、措辞、提交位置和原始问答要求以目标赛事最新官方规则为准。

## 1. 目标

在论文和支撑材料完成后，依据明确授权的本地日志、项目会话和人工补充信息，生成一份真实、可核查、与目标赛事规则匹配的 `AI工具使用详情.pdf`，并同时保留机器可读的审计记录。

该 skill 的重点是如实记录：

- 使用了哪些工具、版本或模型（能确认到什么程度）；
- 在哪个阶段、出于什么目的使用；
- Agent 提供了什么建议、代码、文字、图表或检索线索；
- 团队采纳了哪些、如何修改、如何验证；
- 哪些核心决定由人作出；
- 哪些记录无法完整恢复，需要人工确认或保守披露。

## 2. 适用入口

### `posthoc-history`

读取用户明确指定的 ChatGPT/Codex 项目或任务会话，按分页和 turn 建立索引。适合用户没有预先记录完整日志的情况。

### `local-ledger`

以项目目录中的 `ai_logs/usage.jsonl`、`session_manifest.json` 和人工决策记录为主。适合比赛过程中已经维护过程记录的情况。

### `hybrid`（默认建议）

本地日志作为主证据，历史会话只用于补充和交叉核对；冲突时保留冲突，不自动选择“更好看”的版本。

无论哪种模式，都不能默认扫描整个 ChatGPT 账号；必须有项目/任务范围、时间范围或会话 ID 的明确边界。

历史会话的授权、分页、证据等级、事件去重、匿名化和失败状态见 [AI 使用历史读取协议](../references/ai-use-history-protocol.md)。该协议明确只使用用户可见消息、最终回复、公开工具输出和人工决策记录，不读取或披露系统消息、隐藏提示词或隐藏推理过程。

## 3. 来源优先级

1. 目标赛事最新官方 AI 规则；
2. 目标赛事最新论文格式与支撑材料规范；
3. 学校、赛区或组织方的附加通知；
4. 正式出版伦理/审稿规范；
5. 开源项目和社区实践。

高层来源冲突时，不能用社区经验覆盖官方规则。每条规则都记录赛事、年份、来源 URL/路径、发布日期、访问日期和适用范围。

## 4. 事件 schema（初稿）

每条 AI 使用事件建议包含：

```yaml
event_id: AIE-0001
source:
  type: codex_thread | chatgpt_thread | local_log | file | human_statement
  thread_id: null
  thread_title: null
  turn_or_page: null
  locator: null
  timestamp: null
  timestamp_status: exact | approximate | unknown
tool:
  name: null
  model_or_version: null
  developer: null
stage: topic_selection | intake | literature_orientation | problem_familiarization | research | data | modeling | coding | experiment | figure | writing | review | formatting | disclosure | unknown
action:
  type: topic_selection | question_analysis | background_orientation | literature_search | source_summary | data_organization | model_candidate | code_generation | debugging | experiment_design | figure_generation | language_editing | formatting | review | other
  purpose: null
  prompt_excerpt: null
  prompt_status: verbatim | partial | summarized | unavailable
  output_excerpt: null
  output_status: verbatim | partial | summarized | unavailable
human_control:
  adoption: all | partial | none | unclear
  human_modification: null
  human_verification: null
  decision_owner: human | agent | shared | unclear
  related_decision_log: null
risk:
  substantive_risk: low | medium | high | unknown
  rule_status: allowed | restricted | prohibited | unknown
  disclosure_required: yes | no | unclear
evidence:
  confidence: high | medium | low
  notes: null
```

字段名是内部接口草案；面向赛事的 PDF 不应机械暴露所有内部字段。

## 5. 提取原则

- 原始会话存在时，精确引用只能来自原始会话；摘要不能伪装成逐字记录。
- 找不到工具版本、模型、时间、完整输出或采纳情况时写“未能从现有记录确定”，不能猜测。
- 同一个事件在多个会话出现时合并为“事件族”，保留全部来源锚点和冲突说明。
- 需要披露的“关键交互记录”必须说明是完整、节选还是摘要。
- 只能确认 Agent 提议过某模型，不能因此写成团队采用了该模型。
- 只能确认文字被生成过，不能因此写成最终论文直接使用；必须读取版本差异、人工改稿记录或由作者确认。
- 不从论文成品反推不存在的会话过程。成品只能作为交叉核验材料，不能补造 prompt/response。

## 6. 风险分类：两条轴分开

不能把“内容风险低”直接等同于“比赛一定允许”。内部审计同时使用两条轴：

### 6.1 实质风险

- `low`：格式整理、拼写/标点、明确要求下的局部语言检查；
- `medium`：资料整理、代码语法/调试建议、候选模型、实验设计建议、图表脚本、结构建议；
- `high`：核心模型、关键假设、数据处理、结果解释、创新性和最终结论由 Agent 主导或未经人验证地直接采用。

### 6.2 规则状态

- `allowed`：目标规则明确允许，仍需满足真实性和责任要求；
- `restricted`：需要声明、限制用途、附加材料或人工核验；
- `prohibited`：规则明确禁止，或涉及比赛保密、抄袭、伪造、未经授权外传；
- `unknown`：当前没有足够的官方规则证据，必须升级人工确认。

这两条轴的交叉结果只用于提示风险，不替代目标赛事规则判断。

## 7. 工作流

```text
确认赛事与规则版本
  -> 确认可读取的项目/任务/文件范围
  -> 建立来源索引与去重事件族
  -> 按阶段和用途抽取 AI 事件
  -> 交叉核对论文、代码、支撑材料和决策日志
  -> 标记采纳、改动、验证和未知字段
  -> 生成内部审计报告与人工确认清单
  -> 人工逐项确认/修正
  -> 依据赛事模板生成 AI工具使用详情.pdf
  -> PDF 文本、页数、身份信息、来源和版式预检
  -> 冻结版本并记录 hash/生成日期
```

## 8. 预期输出

```text
output/
├── ai_use_trace.jsonl          # 机器可读事件，含来源锚点和不确定性
├── ai_use_audit.md             # 内部审计报告和人工确认清单
├── AI工具使用详情.pdf           # 面向目标赛事的最终披露文件
└── disclosure_manifest.json    # 规则版本、输入 hash、生成器版本、确认状态
```

如果目标赛事要求把披露内容直接放入论文或附录，PDF 只是内部交付形式，最终排版位置由规则 profile 决定。

## 9. 人工确认门

生成 PDF 前至少确认：

1. 工具/模型清单是否完整且没有猜测版本；
2. 每项用途与阶段是否准确；
3. 关键问答是完整、节选还是摘要；
4. 采纳、人工修改和验证描述是否符合实际；
5. 哪些模型、假设、实验和结论由团队最终决定；
6. 是否存在规则不确定、保密或需要删去的内容；
7. PDF 交付位置、文件名、页数和支撑材料是否满足目标赛事。

没有人工确认时，skill 只能输出草案和阻断提示，不能声称完成正式披露。

## 10. CUMCM 2026 适配器（已核验官方中文细则，仍需实现测试）

官方中文页面发布时间为 2026-08-03，规定自 2026-09-01 起试行。其关键要求应被实现为规则 profile，而不是散落在 prompt 中：

| 项目 | CUMCM 2026 要求 | 实现含义 |
|---|---|---|
| 适用工具 | 大语言模型、生成式 AI、代码辅助工具、AI 智能体等 | 事件采集不能只识别 ChatGPT；工具枚举可扩展 |
| 使用原则 | AI 非必需；核心建模与分析由参赛队主导；AI 参与内容逐项人工审查核实 | 披露报告必须记录人类决策和核验，不允许仅列工具名 |
| 论文声明 | 在参考文献之前二选一放置固定中文声明；未使用时也有固定句式 | 生成器必须按原文渲染，不把英文或自拟句子当默认模板 |
| 详情文件 | 使用 AI 时，支撑材料包含 PDF，文件名为“AI工具使用详情.pdf” | 文件名和提交位置由 profile 控制；生成前做规则检查 |
| 详情字段 | 工具名称/版本或型号；具体目的和环节；主要提示方式与使用过程；输出采纳、人工修改和核验主要情况（语言润色除外） | 事件 schema 支持完整/节选/摘要/未知；语言润色在该字段上有规则例外，但仍需如实记录 |
| 违规后果 | 故意隐瞒、虚假声明或未经必要人工审查核实直接将 AI 内容作为核心建模/分析成果，取消评奖资格 | `prohibited`/`unknown` 事件阻断正式合规输出并进入人工升级 |

根据同一赛事的 2026 年参赛规则和本地格式规范，另需适配：电子论文与支撑材料分开提交；电子论文不含承诺书和编号页，首页为摘要页；正文通常不超过 30 页、附录不限；支撑材料应包含可运行源代码等必要材料；电子论文和支撑材料均有文件大小/身份信息限制；参赛队对原创性、真实性和准确性负全部责任。竞赛期间还不得与队外人员讨论赛题，不得在指定交流平台浏览、发布或讨论赛题内容。

本适配器不能替代其他赛事规则。正式实现前还要补充 profile 的来源 hash、核验日期、冲突版本和测试 fixtures；AI 细则无法访问或字段无法确认时，只能生成内部草案，不能给出合规保证。

## 11. 披露语言的安全边界

报告可以说“记录显示 Agent 在某阶段提出了候选方案，团队随后进行了……验证/修改”，但不能把“Agent 提议过”写成“Agent 完成了模型”，也不能把“未找到记录”写成“没有使用”。

报告不应出现：

- 为了显得合规而虚构的完整 prompt/response；
- 未经验证的模型版本和日期；
- 把 AI 检测器分数作为作者身份证明；
- 把“核心内容由人类负责”当作不披露具体使用情况的理由；
- 对规则没有依据的“完全允许”或“完全禁止”。

## 12. 待研究与冻结项

- CUMCM 2026 AI 规定的完整官方正文、必填字段和提交方式；
- 其他主流数模赛事的规则差异矩阵；
- 历史会话 API/分页读取的最小授权方式；
- PDF 模板、字体、中文换行和脱敏校验；
- 如何由作者低成本确认大量事件而不造成“确认疲劳”；
- AI 使用日志的最小记录格式与本地隐私保护策略。
