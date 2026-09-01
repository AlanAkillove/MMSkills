# 全流程架构设计

## 1. 项目定位与职责边界

MathModelingSkills 是一个面向数学建模论文生产过程的 Agent skill 集合。它服务于“人类负责问题判断与最终决策，Agent 负责检索、整理、候选生成、机械执行和多轮审查”的协作方式。

职责边界如下：

- 参赛队确认题目、假设、模型、结果和最终结论；
- 自然化修稿以清晰、准确和作者可核对为目标；
- 赛事页数、AI 规则和交付要求通过目标赛事 profile 适配；
- 语言层修改与题意、证据、模型和结论审查保持分工。

## 2. 生命周期状态机

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

上图是编排器推荐图的阅读索引；阶段 ID、执行依赖、采用依赖、软建议、人工边界和顺序以 [`schemas/stage-registry.json`](../schemas/stage-registry.json) 为唯一来源。`TOPIC_SELECTION`、`LITERATURE_EVIDENCE` 和 `PROBLEM_FAMILIARIZATION` 不应被合并成一个“背景分析”阶段：它们分别解决全题目选取、来源学习和团队理解确认。用户明确要求局部工作时，只要 `execution_requires` 满足就可以开始；正式采用仍看 `adoption_requires`。

状态不是简单的章节清单，而是帮助不同会话复原工作的可复核记录。核心决定、关键证据和最终交付必须可追踪；可选 review checkpoint 和过程 artifact 不应变成每轮工作的必填表。任何阶段发现上游证据不足时，应回退到相应范围或降低表述强度，而不是用语言润色掩盖缺口。

## 3. 技能分层

### 3.1 编排层

`modeling-pipeline-orchestrator` 只负责识别入口、检查前置条件、调用专项技能、保存状态、提示人工确认和处理回退，不负责自行写出未经验证的实质内容。

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

这些名称已经对应首轮实现的技能目录；后续是否合并或拆分，必须通过兼容性说明、迁移记录和 fixtures 回归，而不能只为减少目录数量而改变职责边界。

## 4. 共享项目状态

每个建模项目建议有独立的状态目录，避免 Agent 只依赖长会话记忆：

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
├── ai_logs/
│   ├── usage.jsonl
│   ├── session_manifest.json
│   └── raw/                 # 默认本地保留，不提交公开仓库
└── support_manifest.md
```

### 4.1 关键字段原则

- 每条重要主张都有 `claim_id`、证据位置、证据强度和适用边界；
- 每个模型候选都有选择理由、放弃理由和人类决策者；
- 每个候选模型都有面向用户的用途、输入/输出、分项评估、代价、风险、未知、验证优先级和最小理解校验记录；
- 每场多题比赛都有全题目卡片、分项比较、主选/备选和人工选题记录；单题或已有选题必须显式记录不适用理由；
- 选题后的背景地图记录现实对象、对象关系、测量/数据过程和子问语义；核心文献以 `literature_insight_id` 记录可迁移思想与不可迁移边界；
- 多轮理解以 `round_id`、团队复述、差异、纠正和 `decision_id` 续接；理解确认只解锁正式建模，不等于模型采用；
- 每个实验都有数据版本、代码入口、参数、随机种子或不适用说明；
- 每个术语都有定义、首次出现位置、是否必要以及是否与已有术语冲突；
- 每项差异化设计都有题目依据、技术功能、验证证据和人类决策记录；
- 每条 AI 使用事件都有来源锚点、用途、输出采纳情况和人类验证状态；
- 审稿、术语、图表、阅读体验、AI 模板化和反同质化发现共享 `finding.schema.json`，相同底层问题保留来源但只形成一个 canonical finding；
- 不确定字段不得默认为“已确认”。

## 5. 人类决策门

注册表把人工边界分成 `core_decision` 和 `review_checkpoint`。以下节点是 `core_decision`，Agent 不能替人最终采用，但在确认前仍可以提出候选、解释和暂定产物：

1. 全部题目的比较范围、主选/备选和选题依据；
2. 题意和子问题的最终解释；
3. 背景、对象关系、术语/单位和核心文献迁移边界；
4. 关键建模假设及其适用范围；
5. 候选模型、目标函数、约束和评价指标的取舍；
5a. 团队是否通过本题对象复述理解候选模型的用途、关键假设、主要代价/风险和待验证点；
6. 删除异常、改切分、采用外部资料或覆盖后续模型所用数据（查看缺失值本身不是门）；
7. 实验是否足以支撑主张；
8. 哪些结构、指标、图表或叙事方式真正体现本题特征；
9. 论文中的主要结论、创新性表述和局限性；
10. AI 使用详情、采纳/修改描述和最终提交文件；
11. 官方 TeX/Word 模板、格式开关、PDF 页面和最终可提交版本。

审稿意见是否采纳、术语/图表/阅读体验等 `review_checkpoint` 默认不阻断用户明确要求的工作，但最终采用前仍须人核对。确认应写入 `decision_log.md`，不能只留在一次不可追溯的口头对话中。

## 6. 上下文与长文处理

针对长论文和长会话，技能采用四层记忆：

1. **原始材料**：论文、代码、数据、会话或导出文件；
2. **分块索引**：章节、段落、页码、表图、会话 turn 和文件 hash；
3. **结构化状态**：问题地图、术语账本、证据矩阵、差异化账本、事件日志；
4. **审查摘要**：仅保留未解决问题、来源锚点和下一步动作。

任何摘要都不能替代需要逐字核对的原始材料。对于 AI 披露，若规则要求原始 prompt/response，必须回到原始记录；只有摘要时只能报告“无法从现有记录完整恢复”。

## 7. 统一质量门

每个阶段至少回答：

- 这一步解决的实际问题是什么？
- 使用了哪些证据？证据是否直接支持结论？
- 是否引入了新的假设、术语、数字或因果关系？
- 是否把题目特征抹平成通用模板？
- 哪些内容仍需人确认？
- 如果上下文被截断，如何可靠续接？

输出质量不以“更复杂、更像论文、更高级”为标准，而以正确性、可解释性、读者可读性、可复核性、题目适配性和规则适配性为标准。

## 8. 机器契约与运行档位

共享机器可读契约位于 [`schemas/`](../schemas/)，其中 `stage-registry.json` 是阶段图的唯一来源，`finding.schema.json` 是跨审查共同问题的 envelope。Markdown 模板服务于讨论，不能替代结构化状态；修改共享字段时必须同步更新 skill、fixtures 和迁移说明。

项目可按 [`profiles/`](../profiles/) 选择 `research-full`、`contest-standard` 或 `contest-fast`。未指定时使用 `contest-standard` 的平衡默认。档位只调整中间产物、审查组合和协作强度，不移除 `core_decision`、失败证据、未决事项、AI 使用事实或最终冻结。`review_checkpoint` 可以被档位延后，但不能被当成已经通过。编排器将 canonical 阶段图、档位和 `user_intent` 合成为 `effective_stage_policy`。

阶段执行采用“硬依赖 + 软建议”两层：`depends_on` 决定是否能开始，`recommended_after` 只提示更合适的先后。默认允许先形成可回退草稿，再按风险运行审稿、AI 模板化、反同质化、阅读体验和自然化审查；内部状态与最终论文正文分离。

## 9. 研究与实现顺序

1. 先冻结阶段注册表、共享 schema、finding 去重协议、质量模型、反同质化检查项和规则适配接口；
2. 再实现前置闭环：全题目盘点 → 选题人工门 → 题意地图 → 文献学习 → 多轮理解确认；
3. 再实现最小论文闭环：题意 → 证据 → 写作 → 成文清洁/审查 → 自然化 → 预检；
4. 在写作前接入差异化设计、模型选择和作者决策记录；
5. 然后接入实验/支撑材料和 AI 使用披露；
6. 最后根据真实论文运行结果拆分或合并 skills。

这样可以避免先写一批互相重复、无法共享状态的提示词。
