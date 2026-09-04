# 全流程架构设计

本文描述 **0.3 默认运行结构**。用户和 Agent 的主路径是三角色入口与事件驱动落盘，不是 stage 流水线。完整赛程图、`project_state` 清单、运行档位和 `depends_on` 语义属于编排器的 legacy/full-orchestration 路径，见文末附录；不要把附录当成普通对话的 SOP。

## 1. 项目定位与职责边界

MathModelingSkills 是面向人机协作的数学建模工作台。用户和 Agent 默认通过 `math-modeling` 看到三个角色（建模手、编程手、论文手）；现有 specialist 按需加载。人类拥有建模判断，Agent 负责理解、检索、推导、实现、核验和起草。

职责边界如下：

- 参赛队确认题目、假设、模型、结果和最终结论；
- 自然化修稿以清晰、准确和作者可核对为目标；
- 赛事页数、AI 规则和交付要求通过目标赛事 profile 适配；
- 语言层修改与题意、证据、模型和结论审查保持分工。

## 2. 默认认知入口

普通对话只走三角色入口，不读取阶段图，不预加载 `schemas/stage-registry.json` 或 process-freezer。

```text
math-modeling
  -> 一个角色（modeler | computationalist | writer）
  -> 0~2 个 specialist
  -> 当前任务需要的 reference / 工具
```

`route_role.py` 是高置信度提示器。没有可靠 `current_role` 时，“继续问题三”“检查图”“数值”应返回 `unknown` / `requires_context`，不要默认建模手。

`modeling-pipeline-orchestrator` 只负责完整赛程初始化、跨会话恢复、full audit 和提交诊断。局部请求（续写一问、改摘要、根据已读论文推模型、精修 5.3）不得长出流程计划。

详细分层见 [`skills/math-modeling/references/progressive-disclosure.md`](../skills/math-modeling/references/progressive-disclosure.md)。决策见 [ADR 0009](adr/0009-role-oriented-workbench.md)。

## 3. 技能分层

### 3.1 入口与编排层

`math-modeling` 是默认认知入口。`modeling-pipeline-orchestrator` 是完整赛程/恢复/诊断入口，不负责自行写出未经验证的实质内容。

### 3.2 研究与建模层

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

这些是内部 specialist，不是每轮必跑的阶段。采用模型所需的是**语义证据**（题意口径已经人类确认），不是某个 skill 名称已经执行完毕。

### 3.3 论文与质量层

- `modeling-paper-architect`
- `modeling-figure-designer`
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

### 3.4 过程与合规层

- `modeling-ai-use-disclosure`
- `modeling-support-materials-auditor`
- `modeling-process-freezer`

这些名称已经对应实现目录；后续是否合并或拆分，必须通过兼容性说明、迁移记录和 fixtures 回归。

## 4. 事件驱动状态

不要为完整而维护一份每轮必填的 `project_state` 树。先在对话里解决问题；跨会话、人类决策、结果将成为下游输入、或最终提交时才落盘。

0.3 默认会碰到的产物：

- `terminology_table.md`：建模阶段建立；写作只做 drift。解释一个符号不落盘。
- `results_snapshot.json`：可含多条 claim；机械产物是 `snapshot`，有 `decision_id` 后才升级为 `frozen`。路径使用仓库相对 locator。
- `run_summary.json`：探索期轻量复现摘要（含 Python/OS/git revision），不是实验报告。
- `decision_log.md` / `decision_id`：adopt / freeze / submit 等 action gate。
- 文献综合默认留在对话；进入模型依据、citation-audit、跨会话或提交时才写 `literature_orientation_ledger.md` 或 citation matrix。

不确定字段不得默认为“已确认”。完整文件清单只用于编排器恢复，见附录 A.2。

## 5. 人类决策门

人工边界按 **动作** 生效（0.2.2 action gate），不是按 stage 节点永远阻断。Agent 不能替人最终采用，但在确认前仍可以提出候选、解释和暂定产物。

核心决定包括：选题、题意口径、关键假设、模型采用、不可逆数据处理、结果冻结、主要结论、AI 披露事实、最终提交文件。审稿/术语/图表等 review checkpoint 默认不阻断用户明确要求的局部工作。

确认应写入带 `decision_id` 的记录，不能只留在一次不可追溯的口头对话中。工具不得把机械 `snapshot` 写成已经 `frozen`。

## 6. 上下文与长文处理

针对长论文和长会话，技能采用四层记忆：

1. **原始材料**：论文、代码、数据、会话或导出文件；
2. **分块索引**：章节、段落、页码、表图、会话 turn 和文件 hash；
3. **结构化状态**：当前真正存在的术语表、证据、决策和快照，而不是空账本模板；
4. **审查摘要**：仅保留未解决问题、来源锚点和下一步动作。

任何摘要都不能替代需要逐字核对的原始材料。

## 7. 统一质量门

每个局部任务至少回答：

- 这一步解决的实际问题是什么？
- 使用了哪些证据？证据是否直接支持结论？
- 是否引入了新的假设、术语、数字或因果关系？
- 是否把题目特征抹平成通用模板？
- 哪些内容仍需人确认？
- 如果上下文被截断，如何可靠续接？

输出质量不以“更复杂、更像论文、更高级”为标准，而以正确性、可解释性、读者可读性、可复核性、题目适配性和规则适配性为标准。

机械脚本（术语 drift、citation 对照、PDF 纸张、snapshot hash）只证明它们检查到的确定项。脚本 `OK` 不是语义审查通过。

## 8. 机器契约

共享机器可读契约位于 [`schemas/`](../schemas/)。`finding.schema.json` 仍是跨审查共同问题的 envelope。`stage-registry.json` **只服务于编排器** 的完整赛程/恢复/提交路径，不是普通对话的加载清单。

修改共享字段时必须同步更新 skill、fixtures 和迁移说明。运行档位 `research-full` / `contest-standard` / `contest-fast` 只在调用编排器时生效，见附录 A.3。

---

## 附录 A. Legacy / full-orchestration

以下内容**不是** 0.3 默认入口。仅当用户明确要求完整赛程、跨会话恢复、full audit 或提交诊断时，由 `modeling-pipeline-orchestrator` 使用。

### A.1 阶段图阅读索引

来源仍是 [`schemas/stage-registry.json`](../schemas/stage-registry.json)。阶段 ID、`execution_requires`、`adoption_requires`、软建议、人工边界和顺序以该文件为唯一来源。用户明确要求局部工作时，只要执行依赖满足就可以开始；正式采用仍看采用依赖，且 core decision 前置需要 `human-confirmed`。计划中的 `blocking` 跟随当前动作的 `action_gates`。

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

`TOPIC_SELECTION`、`LITERATURE_EVIDENCE` 和 `PROBLEM_FAMILIARIZATION` 不应被合并成一个“背景分析”阶段。任何阶段发现上游证据不足时，应回退到相应范围或降低表述强度。

阶段执行采用“硬依赖 + 软建议”两层：历史字段 `depends_on` 与 `execution_requires` 对齐；`recommended_after` 只提示更合适的先后。

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

项目可按 [`profiles/`](../profiles/) 选择 `research-full`、`contest-standard` 或 `contest-fast`。未指定且走编排器时使用 `contest-standard`。档位只调整中间产物、审查组合和协作强度，不移除 `core_decision`、失败证据、未决事项、AI 使用事实或最终冻结。编排器将 canonical 阶段图、档位和 `user_intent` 合成为 `effective_stage_policy`。

### A.4 历史实现顺序（已完成，不再作为 0.3 主工作）

1. 冻结阶段注册表、共享 schema、finding 去重协议、质量模型和规则适配接口；
2. 前置闭环：全题目盘点 → 选题人工门 → 题意地图 → 文献学习 → 多轮理解确认；
3. 最小论文闭环：题意 → 证据 → 写作 → 成文清洁/审查 → 自然化 → 预检；
4. 写作前接入差异化设计、模型选择和作者决策记录；
5. 接入实验/支撑材料和 AI 使用披露。

0.3 主工作是语义收口与真实 Agent 验证，不再按这份 stage-centric 顺序增加 skill。
