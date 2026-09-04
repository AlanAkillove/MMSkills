# 实施路线图

## 阶段 0：基础初始化（已完成）

- Git 仓库、目录、许可证、贡献规范、隐私规范；
- 全流程架构、角色边界、人工决策门；
- 多题选题、背景熟悉、文献 orientation 和理解确认的前置流程设计；
- 共享模板、质量模型、规则 profile 接口；
- CUMCM 2026 官方 AI 细则和格式规范快照；
- 反同质化与 AI 披露设计草案。
- 中性 TeX 论文模板、赛事格式映射和 TeX/PDF 版式预检 skill（本轮新增）。

## 阶段 1.0：三角色工作台（进行中，0.3.0-rc2）

按 ADR 0009 冻结 0.3 方向，不把算法知识库做成选型入口，也不再增加 skill：

1. 已完成：`math-modeling` 入口、三角色指南、编排器降级、术语 establish/audit、results snapshot、run_summary、可行性探测、图表 placement、本地 citation 对照、终检胶水、PDF 机械视觉 QA、可选 DSH 薄适配；
2. 已收口：router 复合意图/unknown 语义、旧架构附录、文献事件驱动落盘、snapshot 相对路径与 freeze gate、preflight required/optional unassessed；
3. 待做：联网文献发现（仍须与核验分开）；有 pymupdf 时再补光栅页抽查的宿主验证；
4. 发布门：真实 Agent 回放（“继续问题三”“根据这些论文继续推模型”“检查图 8”“精修 5.3”、test1 / 26A）。不能把本阶段 pytest 写成 0.3.0 实践成功。DSH 不是发布门。适配器复制整个 `skills/` 树，不能假装宿主只发现 `math-modeling`。

对应决策见 [`docs/adr/0009-role-oriented-workbench.md`](adr/0009-role-oriented-workbench.md)。

## 阶段 0.9：动作门运行时补全（已完成）

0.2.2 不做 0.3.0，也不新增 skill，只清 0.2.1 残留的旧语义：

1. registry 增加 `action_gates`；`blocking` 按当前动作计算；`adoption_satisfied()` 要求 human-confirmed；
2. Safe next action 不再无条件读取 freezer manifest；
3. 继续瘦身 naturalizer、审稿、结构、实验和图表 skill；
4. 默认附录移出通用 TeX；CUMCM AI 义务字段改为四态；
5. 增加 live 回放协议，但**尚未**用真实宿主重跑 test1。

对应决策见 [`docs/adr/0008-action-gates-at-runtime.md`](adr/0008-action-gates-at-runtime.md)。

## 阶段 0.8：去流程中心化与 2026 AI 规则对齐（已完成）

0.2.1 针对“意图优先仍只是排序、SKILL 仍像 SOP、2025 AI 细则被带入 2026”做瘦身迭代，不新增 skill：

1. `depends_on` 拆成 `execution_requires` / `adoption_requires` / `recommended_after`；探索性建模不再被文献、熟悉、差异化或完整数据审计硬阻断；
2. 确认挂到动作：explain/explore/propose 可继续，adopt/freeze/submit 才硬确认；用户可感知参数收敛为 `working_depth`；
3. 缩短模型、数据、熟悉和编排器的 `SKILL.md`，完整 SOP 移入 `references/`；默认先回答用户再按需落盘；
4. 默认 TeX 只保留排版，正文章节示例移到 `examples/`；列表密度按叙事性章节判断；
5. 增加脱敏论文回归量表；CUMCM 2026 AI 规则明确不再要求参考文献列 AI 工具或正文标注。

对应决策见 [`docs/adr/0007-thin-skills-and-action-gates.md`](adr/0007-thin-skills-and-action-gates.md)。真实宿主写作回放仍未替代机械测试。

## 阶段 0.7：意图优先与成文质量回归（已完成）

本轮针对真实项目试跑暴露的“流程先于用户目标”和“论文仍像流程产物”问题完成一次版本迭代：

1. 编排器新增 `user_intent`、`collaboration_mode` 和 `recommended_after`，把硬依赖、软建议、核心决策门与可延后的 review checkpoint 分开；默认档位调整为 `contest-standard`，局部解释、探索、续写和修稿不再被可选审查清单无故阻断；
2. 新增 `modeling-paper-writer`，明确以段落和题目特异性为中心，摘要在主体稳定后形成，禁止内部编号、过程记录、占位符和模板化防御性声明进入正文；
3. `modeling-final-preflight` 新增标准库成文清洁检查脚本，覆盖草稿标记、占位符、内部 ID、过程话语、重复防御性元话语、摘要密度、失效引用和分点过密，并可用本地成熟论文作风格参照，不把参照论文变成固定模板；
4. 将“推荐工作流、用户目标优先、最小读取”原则下沉到主要研究、图表、审查和交付 skill，同时保留原始数据不覆盖、来源不伪造、核心决定由人确认、陌生代码不自动执行等真正的安全/正确性硬边界；
5. 使用 `real-projects-tests/test1` 的 TeX 成稿做只读回归：新检查器确实定位到草稿标记、占位符、内部编号、过程性话语、单段高密度摘要和列表密度问题。该结果只证明检查器能发现已知风险，不代表 Agent 已完成自动修稿或真实宿主行为已经通过。

对应设计决策见 [`docs/adr/0006-intent-first-adaptive-workflow.md`](adr/0006-intent-first-adaptive-workflow.md)。下一步仍需在脱敏真实项目上比较不同协作档位下的用户打断、返工量和正文质量，不能用 fixture 或机械检查替代模型级评估。

## 阶段 0.6：合同运行时效力（已完成）

架构本身保持冻结。本阶段把 ADR 0004 的合同接到运行时：

1. `canonical graph + run profile = effective_stage_policy`，档位真正改变 ready 集合和产物投影；
2. `route_pipeline.validate_state()` 先跑 schema，再跑跨字段语义检查；
3. finding 合并按 `canonical_issue_key` 分组并 union 锚点，冲突不得静默覆盖；
4. registry 区分 `core_decision` 与 `review_checkpoint`；
5. Codex 行为 runner 已接入，但 CI 仍只用 fixture；真实宿主结果稳定前 compatibility 保持 `fixture_only`。

该阶段完成后，继续通过本轮 0.7 迭代补足真实论文成文质量和用户意图路由；进入下一轮行为评估前，仍需在脱敏真实项目上比较 `contest-standard` 与 `contest-fast` 的耗时、人工打断、重复 finding 和返工量。

## 阶段 0.5：架构收敛与行为回归

GPT 评审指出，当前主要风险不是技能数量不足，而是阶段/字段重复、行为验证不足和完整流程的时间成本。因此本阶段先冻结共同基础：

1. `schemas/stage-registry.json` 作为阶段图唯一来源，并将写前 `distinctiveness_coach` 接入模型前路径；
2. `schemas/*.schema.json` 统一状态、决策、证据、finding、模型、实验和 AI 使用事件字段；
3. 由 finding protocol 合并多审查角色的共同问题，保留来源、锚点和冲突；
4. 用结构化行为场景回归人工门、全题目盘点、理解确认和 finding 去重；
5. 以 `research-full`、`contest-standard`、`contest-fast` 三档控制过程材料粒度，并明确不可压缩项；
6. 文档统一为“通用架构 + CUMCM-first 规则实现”，其他赛事另行核验。

本阶段完成不等于完成真实宿主 Agent 的模型级评估；行为 fixtures 是可重复的最低回归层，仍需在脱敏真实项目中执行只读串联。

## 阶段 1：最小可运行闭环

目标：在不依赖自动生成核心模型的前提下，让一篇数模论文能形成可追溯的“题意—假设—主张—证据—审查—自然化—预检”链。

交付：

1. `modeling-topic-selection`（已完成首轮实现与契约测试）；
2. `modeling-literature-evidence` 的 orientation 模式（已完成首轮实现与契约测试）；
3. `modeling-problem-familiarization`（已完成首轮实现与契约测试）；
4. `modeling-problem-intake`（已完成首轮生产实现与契约验证）；
5. `modeling-assumption-ledger`（已完成首轮生产实现与契约验证）；
6. `modeling-claim-evidence-audit`（已完成首轮生产实现与契约验证）；
7. `modeling-terminology-auditor`（已完成首轮生产实现与契约验证）；
8. `modeling-paper-reviewer`（已完成首轮生产实现与契约验证）；
9. `modeling-paper-naturalizer`（已完成首轮生产实现与契约验证）；
10. `modeling-final-preflight`（已完成首轮生产实现与契约验证）。

验收：对多题比赛能逐题形成比较卡片并保留人工选题依据；选定题目能形成背景地图、文献思想边界和多轮理解快照；随后论文的数字、公式、引用、主张、术语和修订前后差异可以被复核；未知内容不会被补造。

## 阶段 2：反同质化与阅读体验

目标：在写作前保留题目特征，在成稿后识别“合理但千篇一律”的模型、结构、术语、图表和表达。

交付：

1. `modeling-distinctiveness-coach`（已完成首轮生产实现与契约验证）；
2. `modeling-anti-homogenization-auditor`（已完成首轮生产实现与契约验证）；
3. `modeling-reader-experience-auditor`（已完成首轮生产实现与契约验证）；
4. 题目特征、差异化、读者摩擦 fixtures。

验收：

- 能区分合理通用结构和模板化填充；
- 能指出论文缺少的题目特异性证据；
- 不为了制造差异而引入复杂模型/新术语；
- 不输出原创度百分比、AI 率或作者归因。

## 阶段 3：数据、模型和实验

目标：将写作前的质量控制延伸到数据和模型选择，减少后期因证据不足返工。

交付：数据审计、模型注册、实验注册、敏感性与稳健性检查、图表设计与制作、代码—论文一致性检查、文献与来源证据链（已完成首轮实现与契约验证）。

验收：关键实验可复现，训练/测试切分无泄漏，模型复杂度有选择理由，结论强度与证据一致。

图表设计技能的额外验收：图型由变量关系和读者任务决定；多面板没有重复角色；颜色、字号、单位和标注在目标页面可读；定量图保留源数据/代码/版本；设计自检与事实审计分流。

## 阶段 4：AI 披露与交付

目标：从本地日志和明确授权的 ChatGPT/Codex 历史会话，生成真实、精简、赛事适配的 AI 使用详情 PDF。

交付：

1. `modeling-ai-use-disclosure`（已完成首轮实现与契约验证）；
2. CUMCM 2026 规则 profile 与本地格式规范快照（已完成；其他赛事 profile 仍需逐项核验）；
3. 结构化 AI 使用事件、内部审计字段、人工确认队列模板（已完成）；
4. PDF 生成、文本/敏感信息/版式检查脚本（已完成，并用 draft/final/失败样例验证）。

验收：完整历史、部分历史、未知版本、未知采纳、重复事件、隐私阻断和规则冲突都能正确处理；没有人工确认时不能标记为最终完成（已通过脱敏 fixtures 验证）。

## 阶段 5：真实项目回归

使用一篇已脱敏、已冻结的真实项目论文运行只读回归，记录：

- 发现的问题与历史人工修改是否一致；
- 是否引入新术语和新问题；
- 是否减少重复返工；
- 是否误报模板化；
- 产物是否能在上下文压缩后续接；
- PDF 和支撑材料是否可交付。

首轮真实项目回归已完成，但本轮新增的共享 schema、finding 合并、行为场景、运行档位和写前差异化默认路由尚未计入该结论。下一次只读回归应重点检查：真实 Agent 是否按 canonical finding 去重、是否在理解确认前保持模型未决、是否能在不同 profile 间保留核心证据，以及文档压缩后能否续接。

图表设计技能以及本轮新增的选题/题目熟悉前置链是在原有回归之后增强的，尚未被计入上述真实项目回归结论；下一轮回归应重点检查全题目比较、文献 orientation、理解 checkpoint、图型选择、题目特异性、多面板取舍、中文字体和正文实际嵌入效果。

## 阶段 6：开源发布

当前状态：进入发布准备。

已具备：API/工具说明、安装与目录说明、版本策略、变更日志、贡献者指南、脱敏示例、许可证与安全边界文档。

发布前仍需完成：全量 validators/tests 回归、相对链接和脚本可移植性核对、更多赛事 profile 的来源核验、Word 交付验证和 PDF 正文/附录分段计数，以及对所有样例和日志字段的隐私复查。规则 profile 不应因为仓库公开而暴露用户私人会话或未公开竞赛材料。
