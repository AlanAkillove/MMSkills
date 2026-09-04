# Changelog

本文件记录可复用技能和共享契约的变化。

## [Unreleased] 0.3.0-rc2

### Changed

- Router 把“根据这些论文继续推模型”一类复合意图放在 generic literature 之前，路由到 `modeling-model-architect` + `modeling-literature-evidence`；测试断言 specialists，不只断言 role。
- `unknown` 表示脚本不能判断：先用显式意图、会话上下文和当前 artifact，再问用户。
- freeze 在 source 位于 repo root 外时默认报错，需 `--allow-external-source` 才记录绝对路径。
- 终检胶水区分 `required_unassessed` / `optional_unassessed`；缺少 paper profile 时不再打印 OK；`--json-out` 在补齐零检查状态之后写盘。
- 局部文献讨论不生成 `literature_insight_id`；只在持久化、跨会话 handoff 或正式模型依据时分配。

## [0.3.0-rc]

### Changed

- `modeling-pipeline-orchestrator` 降为完整赛程、恢复、full audit 和提交诊断入口。
- Router 不再把无上下文的 `continue_local` 猜成 modeler；输出 `confidence` / `matched_rule` / `requires_context`，缺少角色时为 `unknown`。
- `architecture.md` 把 stage 图、`project_state` 清单、三套 profile 和旧实施顺序降为 legacy/full-orchestration 附录。
- `modeling-literature-evidence` 默认对话综合；ledger/matrix 仅在跨会话、进入模型依据、citation-audit 或提交时落盘。
- `modeling-model-architect` 的正式采用改为语义证据（题意口径尚未人类确认），不再要求先跑名为 `problem_familiarization` 的 skill。
- `results_snapshot.json` 改为多 claim、仓库相对路径；机械产物是 `snapshot`，有 `decision_id` 后才是 `frozen`。
- 终检胶水零检查输出 `UNASSESSED`；PDF 纸张从赛事 profile 传入；身份扫描不再把 `.edu.cn` 当 P1。
- 术语 drift 脚本明确为 mechanical scan；`run_summary` 记录 Python/OS/git revision；citation 对照允许无 DOI，标题允许副标题差异。
- DSH 适配器文档改为：复制整个 `skills/` 树，不能强制宿主只发现 `math-modeling`。
- Writer / 终检默认消费 `terminology_table` 与 `results_snapshot`；`pytest.ini` 把测试范围限制在 `tests/`，避免本地嵌套副本干扰收集。

### Added

- 极薄的 `math-modeling` 统一入口与 Modeler / Computationalist / Writer 角色指南；普通任务不预加载编排器和 stage registry。
- ADR 0009：problem-first、literature-guided 工作台；不建设用于模型发现的算法知识库。
- `terminology_table.md` 与术语 `establish` / `audit` 模式；机械 drift 扫描脚本。
- 轻量 results snapshot、`run_summary.json`、可行性探测记录（禁止打分）、图表 `placement` 与 PNG 几何检查。
- 本地 DOI 规范化 / citation 字段对照 / DOI 去重；终检 `check_workbench_artifacts.py`。
- 可选 DeepSeek Harness `native-adapter` 镜像（`hosts/deepseek-harness/`），不改写源 skill，不是发布门。
- PDF 机械视觉 QA：纸张尺寸、空白页、文本抽取、元数据/路径泄露；光栅未安装时记 `unassessed`。

## [0.2.2] - 2026-09-01

### Changed

- `blocking` 改为当前动作的 `action_gates`：探索模型不再显示 blocking core gate；`data_audit` 的 adopt/freeze/submit 仍为 required。
- `adoption_requires` 对 core decision 前置检查 `human-confirmed` 和 `decision_id`，不再把单独的 `status: passed` 当成已经采用。
- Safe next action 按 `working_depth` 和用户意图生成；light/local turn 直接继续当前任务，不强制读取 process-freezer manifest。
- 瘦身 naturalizer、paper-reviewer、paper-architect、experiment-validator 和图表类 `SKILL.md`；SOP 移入 `references/recommended-workflow.md`。
- 默认 TeX 附录改为 `\mmIncludeAppendix` 开关，复现/支撑材料章节移到 `examples/cumcm-appendix.tex`。
- CUMCM 2026 对参考文献列 AI、正文标注、参考文献后未使用声明和全文交互日志改为 `not_required`，不再用布尔 `false` 表达“禁止”。

### Added

- ADR 0008，以及明确“contract tests ≠ live 回放”的 `replay-protocol.md`。第一次真实 Agent 的 test1 重放仍待进行。

## [0.2.1] - 2026-09-01

### Changed

- 阶段依赖拆成 `execution_requires` / `adoption_requires` / `recommended_after`；文献、题目熟悉、差异化和完整数据审计不再硬阻断探索性建模。
- 人工确认按动作分级：解释、探索和建议可以继续；adopt / freeze / overwrite / submit 才硬确认。`data_audit` 降为 review checkpoint。
- 用户可感知参数收敛为 `working_depth`；`collaboration_mode` 保留为别名。默认先回答用户，完整账本仅在留痕、`full` 或最终交付时落盘。
- 缩短模型架构、数据审计、题目熟悉和编排器的 `SKILL.md`，把 SOP 移入 `references/`。
- 默认 TeX 改为纯排版入口，固定正文章节移到 `examples/generic-paper-scaffold.tex`。
- 成文检查的列表风险改为按叙事性章节的连续列表判断，不再使用全文 item 绝对阈值。
- CUMCM 2026 AI 规则按官网与本地 PDF 再核验：声明在参考文献前；详情 PDF 可附典型交互示例；**不再**要求参考文献列 AI 工具、正文标注或参考文献后的未使用声明。2025 对应条款登记为已替代。

### Added

- ADR 0007，以及脱敏的论文成文回归样本与人工量表。
- CUMCM 2026 AI 政策契约测试：禁止把 2025 的参考文献列工具/正文标注带入当届。

## [0.2.0] - 2026-09-01

### Changed

- 编排器改为 user intent priority：用户明确要求解释、探索、续写或局部修稿时，优先推进目标范围，不因可选 artifact 或 review checkpoint 缺失而改写任务顺序；未指定档位时默认使用 `contest-standard`。
- 阶段注册表新增 `recommended_after` 软建议，并将 `human_gate` 语义对齐为 core decision=`required`、review checkpoint=`optional`；论文写作不再硬依赖结构蓝图、实验、图表/术语审查报告，缺口由写作 skill 标记并由终检拦截最终采用。
- 运行时与状态 schema 增加 `user_intent`、`collaboration_mode`、`review_gates` 和协作策略；计划同时展示硬依赖、软建议、目标阶段和协作强度。
- 将写作入口从占位的 `author/agent writing` 替换为 `modeling-paper-writer`，明确段落优先、摘要后置提炼、术语克制和内部追踪层/论文成文层分离。
- `modeling-paper-architect`、`modeling-paper-naturalizer`、TeX 生产和人工门文档改为推荐流程，允许在不越过核心决策边界的前提下交付暂定分析和局部草稿。
- 通用 TeX 模板移除容易被直接复制进论文的可见示例正文、泛化公式和占位清单，保留注释式骨架。

### Added

- `skills/modeling-final-preflight/scripts/check_manuscript_quality.py`：检查草稿/待填残留、内部 ID、过程性话语、重复防御性元话语、摘要密度、失效交叉引用和列表密度；不计算 AI 率、原创度或相似度。
- 成文质量回归测试、论文写作 skill 契约测试和 ADR 0006。

## [0.1.0] - 2026-08-31

### Added

- 编排器现在把 canonical 阶段图与运行档位合成为 `effective_stage_policy`：`contest-fast` 会按 `max_post_draft_lenses` 选择审查透镜，并把未选中阶段标为 `skipped-with-policy`，但不改 canonical 依赖；
- 路由入口先用 `pipeline-state.schema.json` 做 Draft 2020-12 校验，再检查 human-confirmed/decision_id、skipped/reason、current_stage 和 depends_on 冲突；
- finding 合并改为按 `canonical_issue_key` 分组，union 全部证据锚点和关联 ID，并在 open/resolved 或 human_status 冲突时进入 `needs_human`；
- 阶段注册表增加 `gate_type`（`core_decision` / `review_checkpoint` / `none`），profile 不能取消核心决策门；
- 增加 Codex 行为 runner `tests/behavioral/run_host_case.py`：可规范化已有响应或在显式 `--execute` 时调用宿主，缺失宿主记为 `not_run` 而非通过。
- 统一阶段注册表 `schemas/stage-registry.json`，将 `distinctiveness_coach` 纳入默认模型前路径，并修正文档、路由脚本与终检顺序漂移；
- 增加 pipeline state、decision、evidence、finding、model、experiment 和 AI use event 的机器可读 schema，以及跨审查 finding 去重/冲突协议和合并脚本；
- 增加 `research-full`、`contest-standard`、`contest-fast` 运行档位，明确在时间压缩下仍不可移除的人工门和证据；
- 增加候选模型人工门、全题目选题、背景熟悉防跳模和跨审查去重的行为级回归场景与正反响应 fixtures；
- 明确项目定位为通用流程架构 + CUMCM-first 规则实现，避免把单赛事规则误写成通用规范。

### Changed

- 根 README 流程蓝图与 canonical registry 对齐为选题 → 文献/理解确认 → 问题地图；
- run-profile schema 收紧透镜枚举，并增加 registry 交叉校验，避免 `problem_familiarisation` 这类拼写错误通过。

- 初始化开源项目骨架；
- 建立全流程数模技能的总架构、反同质化设计、质量模型和分板块调研计划；
- 建立 AI 使用详情披露的规则适配与证据追踪设计草案。
- 增加跨审稿、自然化和阅读体验技能共用的防御性声明处理协议，并补充正反例契约测试。
- 完成首个生产级技能 `modeling-problem-intake` 的入口、图示/几何读取协议、字段契约、长题面 checkpoint 和脱敏正反例。
- 完成第二个生产级技能 `modeling-assumption-ledger` 的入口、假设字段契约、影响/验证指南、长材料 checkpoint 和脱敏正反例，并完成契约验证。
- 完成第三个生产级技能 `modeling-claim-evidence-audit` 的入口、主张矩阵 schema、强度校准表、证据审查工作流和脱敏正反例，并完成契约验证。
- 完成第四个生产级技能 `modeling-terminology-auditor` 的入口、术语账本 schema、保留/回退判据、跨产物一致性检查、共享模板和脱敏正反例，并完成契约验证。
- 完成第五个生产级技能 `modeling-ai-pattern-reviewer` 的入口、五层信号分类、模板化审查协议、研究依据和脱敏正反例，并完成契约验证。
- 完成第六个生产级技能 `modeling-paper-naturalizer` 的入口、修订保真契约、自然化模式、受保护语法、研究依据和脱敏正反例，并完成契约验证。
- 完成第七个生产级技能 `modeling-paper-reviewer` 的入口、六个数模审查透镜、finding 契约、独立审查工作流、研究依据和脱敏正反例，并完成契约验证。
- 完成第八个生产级技能 `modeling-distinctiveness-coach` 的入口、题目锚点—路径账本、强行创新护栏、研究依据和脱敏正反例，并完成契约验证。
- 完成第九个生产级技能 `modeling-anti-homogenization-auditor` 的入口、五层题目特异性覆盖审计、相似性授权防护、研究依据和脱敏正反例，并完成契约验证。
- 完成第十个生产级技能 `modeling-reader-experience-auditor` 的入口、三条读者路径、视觉/导航检查、研究依据和脱敏正反例，并完成契约验证。
- 完成第十一个生产级技能 `modeling-rules-profile` 的入口、规则来源/版本 schema、冲突与新鲜度处理、本地格式 PDF 核验依据和脱敏正反例，并完成契约验证。
- 完成第十二个生产级技能 `modeling-data-audit` 的入口、数据 manifest/字典契约、质量与缺失处理、时间/实体泄漏审计和脱敏正反例，并完成契约验证。
- 完成第十三个生产级技能 `modeling-model-architect` 的入口、基线优先模型注册、适配/复杂度比较、验证准备度和脱敏正反例，并完成契约验证。
- 完成第十四个生产级技能 `modeling-experiment-validator` 的入口、实验注册、验证矩阵、公平比较、不确定性/敏感性、复现契约和脱敏正反例，并完成契约验证。
- 完成第十五个生产级技能 `modeling-paper-architect` 的入口、章节/段落契约、论证映射、篇幅与图表计划和脱敏正反例，并完成契约验证。
- 完成第十六个生产级技能 `modeling-figure-table-auditor` 的入口、图表证据契约、数据/主张/单位核对、视觉检查和脱敏正反例，并完成契约验证。
- 完成第十七个生产级技能 `modeling-support-materials-auditor` 的入口、支撑 manifest、压缩包与执行安全、论文一致性和脱敏正反例，并完成契约验证。
- 完成第十八个生产级技能 `modeling-final-preflight` 的入口、八层提交前检查目录、状态/阻断/签核契约和脱敏正反例，并完成契约验证。
- 完成第十九个生产级技能 `modeling-literature-evidence` 的入口、来源/主张证据契约、检索与版本核验、引用安全边界和脱敏正反例，并完成契约验证。
- 完成第二十个生产级技能 `modeling-ai-use-disclosure` 的入口、会话授权与事件 schema、隐私/对账/规则映射、草稿与最终版 PDF 生成校验及渲染检查。
- 完成第二十一个生产级技能 `modeling-process-freezer` 的入口、状态谱系、SHA-256 manifest、上下文交接、冻结签核和哈希失效测试，并完成契约验证。
- 完成第二十二个生产级技能 `modeling-pipeline-orchestrator` 的入口、全流程依赖图、返工影响矩阵、人工门、只读路由脚本和未知状态失败测试，并完成契约验证。
- 完成第二十三个生产级技能 `modeling-figure-designer` 的入口、图表设计契约、选图规则、视觉系统、制作/交接流程、开源实践依据和脱敏正反例，并完成契约验证。
- 增强 `modeling-model-architect` 的用户决策支持：为候选模型增加通俗用途、分项评估、证据/未知、验证优先级、候选卡片和决策简报，并用理解确认门阻止总分、单一推荐和沉默同意替代人类决策。
- 增加跨 Agent 安装教程与可复制安装提示词：先探测宿主能力，再在原生标准目录、宿主适配器、插件/扩展、项目 instructions、单条提示词和阻断状态之间选择；补充依赖闭包、权限、安全、验证、manifest、升级与回滚要求。
- 增加 `modeling-tex-paper-production` 与 `templates/tex/`：从既有数模 TeX 实例提炼中性写作骨架，按 CUMCM、COMAP、MathorCup 和研究生数模的差异拆分赛事 profile，补充 XeLaTeX 构建、PDF 渲染、许可证、匿名、页数、AI 声明和版式审计边界。
- 将安装教程和 README 安装入口切换为公开仓库 `https://github.com/AlanAkillove/MMSkills`，补充 Git 获取源代码与项目级短安装提示词，同时保留跨宿主适配边界。
- 修正通用规则模板和 CUMCM 2026 profile 的 0.2 schema 对齐、YAML 引号与保守 `draft` 状态；补充编排器无 ready 阶段的安全动作测试。
- 增加开发依赖清单和 GitHub Actions 质量工作流，覆盖契约测试、YAML 解析、Python 编译和披露 PDF 草稿校验。
- 发布产物已移除本机磁盘路径和 Windows 用户名，并将命令统一为跨平台占位符。

### Pending

- 扩充 CUMCM 以外的赛事规则 profile，并在实际比赛前重新核验时效性；
- 持续用脱敏真实项目验证各 skill 的串联、返工影响和保守人工门；
- 评估本地日志采集/脱敏工具及 PDF/Word/LaTeX 交付验证工具是否需要独立拆分；
- 完成开源发布前的依赖、许可证、敏感信息和文档核对。
