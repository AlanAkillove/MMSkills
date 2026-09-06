# 架构说明

本文描述 **0.3 默认运行结构**。用户和 Agent 的主路径是三角色入口与事件驱动落盘，不是阶段流水线。完整赛程图、项目状态清单、运行档位和阶段依赖属于编排器的完整编排路径，见文末附录；不要把附录当成普通对话的操作规程。

## 1. 项目定位与职责边界

MathModelingSkills 是面向人机协作的数学建模工作台。用户和 Agent 默认通过 `math-modeling` 看到三个角色（建模手、编程手、论文手）；现有专项技能按需加载。人类拥有建模判断，Agent 负责理解、检索、推导、实现、核验和起草。

职责边界如下：

- 参赛队确认题目、假设、模型、结果和最终结论；
- 自然化修稿以清晰、准确和作者可核对为目标；
- 赛事页数、AI 规则和交付要求通过目标赛事配置适配；
- 语言层修改与题意、证据、模型和结论审查保持分工。

## 2. 默认认知入口

普通对话只走三角色入口，不读取阶段图，不预加载 `schemas/stage-registry.json` 或过程冻结器。

```text
math-modeling
  -> 一个角色（modeler | computationalist | writer）
  -> 该角色的 capability index（问题维度，高召回）
  -> 完成当前任务所需的最少专项技能
  -> 当前任务需要的参考资料 / 工具
```

普通单任务通常 0–2 个专项技能（预算，不是硬上限）。复合任务按能力覆盖选择最小集合。产物跨越质量边界时由 `resolve_quality.py` 约束；最终审稿必须独立 Subagent。

`route_role.py` 是高置信度提示器。没有可靠当前角色时，“继续问题三”“检查图”“数值”应返回 `unknown` / `requires_context`，不要默认建模手。

`modeling-pipeline-orchestrator` 只负责完整赛程初始化、跨会话恢复、全面审计和提交诊断。局部请求（续写一问、改摘要、根据已读论文推模型、精修 5.3）不得长出流程计划。

详细分层见 [`skills/math-modeling/references/progressive-disclosure.md`](../skills/math-modeling/references/progressive-disclosure.md)。

## 3. 当前架构边界

当前 0.3 系列按以下边界运行：

1. 默认只路由到建模手 / 编程手 / 论文手。现有专项技能保留，不合并成单一流程。
2. 普通交互不经过编排器，不预加载阶段注册表。编排器只用于完整赛程、恢复、全面审计和提交诊断。
3. 渐进加载五层：路由 → 角色 → capability index → 专项技能 → 参考资料/工具。不预加载完整工作流。L1.5 负责发现，完整 Skill 负责执行。
4. 建模遵循问题先行、文献辅助。不建设用于模型发现的算法知识库。文献不足时可以提出暂定候选，但必须标明文献支持与模型知识来源。
5. 术语在建模阶段建立 `terminology_table.md`；写作阶段只检查用词漂移。
6. 能由脚本确定的检查写成工具。结果快照、运行摘要、图表几何、本地引用对照、PDF 机械页面检查和终检胶水属于工具层。
7. 事件驱动留痕：不因为技能被调用而创建文件。采用、冻结、提交仍按动作门由用户确认。
8. 写作审查只报告可定位、可解释的语言信号。句长、被动句、问句等不得单独作为模板化证据。终稿精修默认按信号做最小修改；不输出 AI 分数或作者身份。
9. 赛题来源年份与提交规则年份分离。未解析 `rules_profile_id` 时不得声称合规。
10. 官方规则与写作策略分开：后者在 `profiles/writing/`。CUMCM 中文终稿的 itemize、boxed 公式、孤立参考文献、单独问题重述章由预检机械执行。目标页数属于项目 preference，不是公共默认。
11. 最终成稿审阅必须使用独立 Subagent，从磁盘重读稿件。承重章节完成后做 scoped review；全文审阅仍然必须保留。
12. 契约测试通过不能宣称真实 Agent 行为已经验证。
13. Independent Quality Control：审计查对错，审阅评质量，挑战找反例。`quality-policy.yaml` 由 `scripts/resolve_quality.py` 执行。缺少当前 hash 的审查证据时允许讨论，不允许标记 adopted / frozen / paper / assembled。一个承重单元一次 Subagent。
14. 图表前置：正式写整篇第一轮只加载论证与图表计划，讨论后再写正文。未规划运行图默认 `diagnostic`。`placement` 与 `maturity` 分开。`figure-designer` 是 shared capability，可进入任意角色候选。
15. CUMCM 中文写作策略禁止单独的「问题重述」章（不是官方法条）。必要题面事实并入问题分析或各问建模。

明确不做：算法百科、固定候选/图数量、强制基线、把普通对话做成阶段流水线、按词频改写、把通用中文写作阈值硬套数模论文、把写作偏好写成官方规则、所有 Skill 都强制 Subagent。

## 4. 技能分层

### 4.1 入口与编排层

`math-modeling` 是默认认知入口。`modeling-pipeline-orchestrator` 是完整赛程/恢复/诊断入口，不负责自行写出未经验证的实质内容。

### 4.2 研究与建模层

- `modeling-topic-selection`
- `modeling-problem-familiarization`
- `modeling-problem-intake`
- `modeling-rules-profile`
- `modeling-literature-evidence`
- `modeling-data-audit`
- `modeling-assumption-ledger`
- `modeling-model-architect`
- `modeling-experiment-validator`
- `modeling-distinctiveness-coach`

这些是内部专项技能，不是每轮必跑的阶段。采用模型所需的是**语义证据**（题意口径已经人类确认），不是某个技能名称已经执行完毕。

### 4.3 论文与质量层

- `modeling-paper-architect`
- `modeling-figure-designer`（shared：论证与视觉计划，不只属于编程手）
- `modeling-figure-table-auditor`
- `modeling-claim-evidence-audit`
- `modeling-terminology-auditor`
- `modeling-paper-reviewer`
- `modeling-ai-pattern-reviewer`
- `modeling-anti-homogenization-auditor`
- `modeling-paper-naturalizer`
- `modeling-reader-experience-auditor`
- `modeling-paper-writer`
- `modeling-tex-paper-production`
- `modeling-final-preflight`

### 4.4 过程与合规层

- `modeling-ai-use-disclosure`
- `modeling-support-materials-auditor`
- `modeling-process-freezer`

这些名称已经对应实现目录；后续是否合并或拆分，必须通过兼容性说明、迁移记录和样例回归。

## 5. 事件驱动状态

不要为完整而维护一份每轮必填的项目状态树。先在对话里解决问题；跨会话、人类决策、结果将成为下游输入、或最终提交时才落盘。

0.3 默认会碰到的产物：

- `terminology_table.md`：建模阶段建立；写作只检查用词漂移。解释一个符号不落盘。
- `results_snapshot.json`：可含多条主张；机械产物是快照，有决策编号后才升级为已冻结。路径必须是仓库相对定位符；来源在项目根目录外应报错，除非显式允许外部来源。
- `run_summary.json`：探索期轻量复现摘要（含 Python/OS/git revision），不是实验报告。
- `decision_log.md` / 决策编号：采用 / 冻结 / 提交等动作门。
- 文献综合默认留在对话；进入模型依据、引用审计、跨会话或提交时才写文献台账或引用矩阵。

不确定字段不得默认为“已确认”。完整文件清单只用于编排器恢复，见附录 A.2。

## 6. 人类决策门

人工边界按 **动作** 生效，不是按阶段节点永远阻断。Agent 不能替人最终采用，但在确认前仍可以提出候选、解释和暂定产物。

核心决定包括：选题、题意口径、关键假设、模型采用、不可逆数据处理、结果冻结、主要结论、AI 披露事实、最终提交文件。审稿/术语/图表等检查点默认不阻断用户明确要求的局部工作。

确认应写入带决策编号的记录，不能只留在一次不可追溯的口头对话中。工具不得把机械快照写成已经冻结。

## 7. 上下文与长文处理

针对长论文和长会话，技能采用四层记忆：

1. **原始材料**：论文、代码、数据、会话或导出文件；
2. **分块索引**：章节、段落、页码、表图、会话轮次和文件哈希；
3. **结构化状态**：当前真正存在的术语表、证据、决策和快照，而不是空账本模板；
4. **审查摘要**：仅保留未解决问题、来源锚点和下一步动作。

任何摘要都不能替代需要逐字核对的原始材料。

## 8. 统一质量门

每个局部任务至少回答：

- 这一步解决的实际问题是什么？
- 使用了哪些证据？证据是否直接支持结论？
- 是否引入了新的假设、术语、数字或因果关系？
- 是否把题目特征抹平成通用模板？
- 哪些内容仍需人确认？
- 如果上下文被截断，如何可靠续接？

输出质量不以“更复杂、更像论文、更高级”为标准，而以正确性、可解释性、读者可读性、可复核性、题目适配性和规则适配性为标准。

机械脚本（术语漂移、引用对照、PDF 纸张、快照哈希）只证明它们检查到的确定项。脚本通过不是语义审查通过。

## 9. 机器契约

共享机器可读契约位于 [`schemas/`](../schemas/)。`finding.schema.json` 仍是跨审查共同问题的信封。`stage-registry.json` **只服务于编排器** 的完整赛程/恢复/提交路径，不是普通对话的加载清单。

修改共享字段时必须同步更新技能、样例和迁移说明。运行档位只在调用编排器时生效，见附录 A.3。

---

## 附录 A. 完整编排路径

以下内容**不是** 0.3 默认入口。仅当用户明确要求完整赛程、跨会话恢复、全面审计或提交诊断时，由 `modeling-pipeline-orchestrator` 使用。该路径对应历史的 full-orchestration 附录，不要当成普通对话的操作规程。

### A.1 阶段图阅读索引

来源仍是 [`schemas/stage-registry.json`](../schemas/stage-registry.json)。阶段编号、执行依赖、采用依赖、软建议、人工边界和顺序以该文件为唯一来源。用户明确要求局部工作时，只要执行依赖满足就可以开始；正式采用仍看采用依赖，且核心决定前置需要人类确认。计划中的阻断状态跟随当前动作的动作门。

```text
RULES_PROFILE
  -> TOPIC_SELECTION
  -> LITERATURE_EVIDENCE (orientation)
  -> PROBLEM_FAMILIARIZATION
  -> PROBLEM_INTAKE
  -> DISTINCTIVENESS_COACH
  -> (ASSUMPTION_LEDGER || DATA_AUDIT)
  -> MODEL_ARCHITECT
  -> EXPERIMENT_VALIDATOR
  -> PAPER_ARCHITECT
  -> FIGURE_DESIGN
  -> (FIGURE_TABLE || CLAIM_EVIDENCE || TERMINOLOGY)
  -> DRAFT
  -> PAPER_REVIEW
  -> (AI_PATTERN || ANTI_HOMOGENIZATION || READER)
  -> NATURALIZER
  -> SUPPORT
  -> AI_DISCLOSURE
  -> FINAL_PREFLIGHT
  -> PROCESS_FREEZER
```

选题、文献证据和题目熟悉不应被合并成一个“背景分析”阶段。任何阶段发现上游证据不足时，应回退到相应范围或降低表述强度。

阶段执行采用“硬依赖 + 软建议”两层：历史字段 `depends_on` 与执行依赖对齐；软建议只提示更合适的先后。

### A.2 编排器恢复用的项目状态清单

完整赛程或跨会话恢复时，项目可以有独立状态目录。这不是每轮工作的必填表：

```text
project_state/
├── project_profile.yaml
├── rules_profile.yaml
├── topic_cards.md
├── topic_comparison.md
├── topic_selection_brief.md
├── question_map.md
├── problem_background_map.md
├── literature_orientation_ledger.md
├── understanding_checkpoint.md
├── familiarization_open_questions.md
├── data_dictionary.md
├── assumption_ledger.md
├── decision_log.md
├── model_registry.md
├── model_candidate_cards.md
├── model_decision_brief.md
├── experiment_registry.jsonl
├── claim_evidence_matrix.csv
├── terminology_table.md
├── terminology_ledger.md
├── figure_design_brief.md
├── figure_storyboard.md
├── figure_design_manifest.yaml
├── distinctiveness_ledger.md
├── figure_table_registry.md
├── tex_build_manifest.yaml
├── tex_layout_audit.md
├── issue_log.md
├── finding_register.jsonl
├── run_profile.yaml
├── results_snapshot.json
├── ai_logs/
│   ├── usage.jsonl
│   ├── session_manifest.json
│   └── raw/                 # 默认本地保留，不提交公开仓库
└── support_manifest.md
```

### A.3 运行档位

项目可按 [`profiles/`](../profiles/) 选择 `research-full`、`contest-standard` 或 `contest-fast`。未指定且走编排器时使用 `contest-standard`。档位只调整中间产物、审查组合和协作强度，不移除核心决定、失败证据、未决事项、AI 使用事实或最终冻结。编排器将规范阶段图、档位和用户意图合成为有效阶段策略。
