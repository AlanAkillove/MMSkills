# 分板块细化设计方案（v0.1）

本文件把总架构拆成可实现、可测试的工作块。每个工作块先有设计卡，再创建 skill；如果一个 skill 同时承担多个工作块而无法单独测试，应重新拆分。

## 0. 共同 skill 契约

每个 skill 的入口 `SKILL.md` 都应包含：

```text
触发条件 / 非触发条件
输入材料与读取顺序
状态文件与证据锚点
工作阶段与停止条件
人类确认门
输出文件与机器可读字段
不确定性和失败处理
硬性禁令
相关 references / scripts / examples
```

推荐采用 `manifest + static fragments + on-demand references` 的结构：入口只负责识别任务轴和加载必要片段；长规则、长词表和样例不全部进入每次上下文。这是对开源 academic skills 工程实践的借鉴，具体内容仍按数模需求重新设计。

## 1. 基础状态与规则块（P0）

### 1.1 `modeling-pipeline-orchestrator`

- 输入：用户目标、已有材料、赛事 profile、当前状态文件；
- 输出：阶段判断、前置缺口、下一步建议、checkpoint 和状态更新；
- 人类门：每次跨越题意、模型、数据、结论和最终提交边界时确认；
- 禁止：自行完成实质建模、替人选择方案、绕过阻断项；
- 测试：缺材料、状态冲突、长文断点、用户要求直接跳过核心确认。

### 1.2 `modeling-rules-profile`

- 输入：赛事名/年份/赛区、官方规则、格式 PDF、学校附加通知；
- 输出：`rules_profile.yaml`、来源登记、冲突和过期警告；
- 人类门：确认目标赛事和适用版本；
- 禁止：用搜索摘要替代官方原文；没有来源时写成确定规则；
- 测试：CUMCM 2025/2026 差异、统计建模与 CUMCM 字段差异、规则不可访问。

### 1.3 `modeling-project-state`

这是共享状态契约，可作为内部支持包，不一定作为独立触发 skill。负责建立版本、hash、分块索引、checkpoint、状态迁移和隐私标签。

## 2. 题意、模型和数据块（P0/P1）

### 2.1 `modeling-problem-intake`

- 目标：把题面转成对象、关系、子问题、变量、目标、约束、边界和歧义；
- 关键方法：文字与图示分离；直接事实、合理推断和待确认问题分层；先列反例/极端情形；
- 输出：`question_map.md`、对象/变量表、歧义清单、题目特有事实清单；
- 人类门：确认题意解释和不确定边界；
- 反模式：从图片风格臆测结构、把常见题型套入题面、先选算法再解释问题。

### 2.2 `modeling-assumption-ledger`

- 目标：让每个假设都有依据、必要性、影响、边界和验证方式；
- 输出：`assumption_ledger.md`；
- 人类门：确认改变题意或结论范围的关键假设；
- 反模式：为方便计算默默改变题目、把假设写成事实、用“合理”代替解释。

### 2.3 `modeling-data-audit`

- 目标：审计来源、口径、缺失、异常、单位、时间顺序、样本切分、泄漏、授权和可复现性；
- 输出：数据字典、清洗日志、数据审计报告、处理决策；
- 人类门：异常值规则、外部数据采用、训练/测试策略；
- 反模式：为了结果好看删除异常、把预测指标当决策指标、只报告最优切分。

### 2.4 `modeling-model-architect`

- 目标：先建立可解释基线，再比较候选模型的适配性、复杂度、数据需求、可验证性、表达成本和用户理解成本；
- 输出：`model_registry.md`、`model_candidate_cards.md`、`model_decision_brief.md`、候选比较表、放弃理由、差异化账本更新；
- 人类门：用户通过本题对象复述候选的用途/关键假设/主要风险后，由团队确认模型、目标函数、约束和复杂度取舍；
- 反模式：为了“先进”选择 LSTM/深度模型/复杂优化、只列算法名、用总分或单一推荐替代分项证据、无失败方案和基线。

### 2.5 `modeling-experiment-validator`

- 目标：把实验变成可复现的验证链，而不是结果截图；
- 输出：`experiment_registry.jsonl`、基线、敏感性、稳健性、误差/置信信息和复现命令；
- 人类门：实验是否足以支撑主要主张；
- 反模式：只展示最好结果、混淆置信区间与预测区间、忽略空集/边界/极端输入。

## 3. 反同质化块（P0/P1）

### 3.1 `modeling-distinctiveness-coach`（写前和建模中）

- 输入：题面、问题地图、候选模型、数据观察、团队已有决策；
- 输出：`distinctiveness_ledger.md`、题目特有锚点、可保留的真实观察、候选路径比较和人类问题清单；
- 核心检查：哪些结构只能由本题解释，哪些内容只是通用模板；
- 人类门：确认团队愿意承担的差异化路径，不允许 Agent 自行“创造创新”；
- 反模式：为了避免常见模型而复杂化、把换名词当创新、删除真实失败过程。

### 3.2 `modeling-anti-homogenization-auditor`（成稿后）

审查五层：题目特征、模型路径、证据组织、术语/贡献叙述、表达/图表。可在用户授权的内部论文库中做相似性线索扫描，但在竞赛窗口内不得使用它绕过赛事对外部交流或材料浏览的限制。

输出至少包括：

- 题目特有锚点在正文中的证据位置；
- 通用模板段落和与题目脱节的模型/图表；
- 高度雷同的贡献/结论表达，仅作为文本线索；
- “可保留的真实差异”与“强行创新风险”；
- 具体补写、删除、合并或回退到标准术语的建议；
- 人工需要确认的差异化决策。

不能输出原创度百分比、AI 率、抄袭结论或作者身份判断。

## 4. 论文结构与证据块（P0/P1）

### 4.1 `modeling-paper-architect`

- 目标：从问题地图、差异化账本和主张—证据矩阵推导章节和段落，而不是从固定目录反向填内容；
- 输出：章节目的、段落功能、图表位置、主张/证据/边界映射；
- 反模式：算法清单、摘要先夸贡献后补证据、每节都使用相同三段式。

### 4.2 `modeling-claim-evidence-audit`

- 目标：检查主张是否有直接证据，证据强度是否匹配措辞，因果/比较/最优/鲁棒等强词是否有相应验证；
- 输出：`claim_evidence_matrix.csv`、阻断问题、需降级的表述和缺失实验清单；
- 人类门：确认主张强度和是否补实验；
- 反模式：把“模型给出结果”写成“证明普适规律”，把相关性写成因果性。

### 4.3 `modeling-figure-designer`

- 目标：从读者任务、证据角色、题目特征和正文版式出发，选择图型、编排多面板、建立视觉系统并制作可复现/可编辑的图表与模型结构图；
- 输入：题目/问题地图、论文蓝图、主张—证据矩阵、数据与实验注册、术语账本、目标赛事格式和已有绘图源；
- 输出：`figure_design_brief.md`、`figure_storyboard.md`、`figure_design_manifest.yaml`、绘图代码/可编辑源、目标尺寸渲染件和视觉自检；
- 人工门：确认展示范围、删留结果、颜色语义、关键标注、题目特异性和最终版本；
- 反模式：只套样式、选错图型、用装饰填空、只靠颜色编码、用生造术语包装普通结果、从截图补造数据；
- 边界：设计阶段的视觉自检不能替代图表事实审计，数字/单位/主张/来源仍交给下游审计技能。

### 4.4 `modeling-figure-table-auditor`

- 目标：每张图/表回答一个明确问题，数据、单位、图例、正文解释、代码和结论一致；
- 输出：图表注册表、证据角色、可读性/碰撞/数值一致性报告；
- 反模式：图表只做装饰、颜色表示不清、正文重复数字而不解释、图表与模型脱节。

## 5. 术语、审稿和自然化块（P1）

### 5.1 `modeling-terminology-auditor`

- 写前模式：建立标准术语、定义、缩写、单位和必要的新术语预算；
- 成稿模式：机械统计变体，再打开上下文判断是否是真差异；
- 输出：`terminology_ledger.md`、必改项、可接受变体、疑似生造术语；
- 硬规则：新术语必须有定义、功能和重复使用价值；普通事实优先用标准表达；
- 禁止：全篇同义词轮换、三个以上形容词堆名词、用“定律/证书/审计/语义/鲁棒”等高承诺词包装局部事实。

### 5.2 `modeling-paper-reviewer`

采用多个审查透镜而不是固定多个“人格”：题意与问题、数学/模型、数据/实验、论文论证、竞赛合规。每个透镜先独立冻结发现，再综合同一底层问题。

输出：摘要、主要优点、Major/P1、Minor/P2、证据锚点、为什么重要、修复验收标准、置信度和未评估范围。

禁止：编造实验/引用/审稿身份；为凑数量制造问题；把作者动机或 AI 身份当作审稿结论；把审稿报告直接改成作者回复。

### 5.3 `modeling-ai-pattern-reviewer`

识别“可观察的文本与结构信号”，例如套话开头、连接词过密、均匀三点式、抽象名词堆叠、过度对称、空洞因果、贡献/展望模板、长句叠加、术语包装、表达层级与证据不匹配，以及没有新增信息的防御性声明簇。

输出每条信号的原文位置、具体例子、影响、置信度和可读性导向的修复建议；防御性声明另记录功能、重复范围和保留/合并/删除建议。不得说“这段一定由 AI 写成”，不得依赖 detector 分数。

### 5.4 `modeling-paper-naturalizer`

处理顺序固定为：

```text
锁定数字/公式/引用/代码/主张
  -> 诊断结构、证据和段落功能
  -> 删除无信息套话与重复
  -> 恢复标准术语和题目特异性
  -> 合并或删除无信息的防御性声明，保留有效边界
  -> 调整句长、连接和语气
  -> 前后差异核对
  -> 生成变更日志与未决问题
```

默认是最小必要改动；如果结构问题不能靠已有材料修复，必须提出缺口，不得补造事实。输出可选 `diagnose`、`minimal-edit`、`paragraph-rebuild`、`section-revision` 四种模式。

## 6. 阅读体验与交付块（P1）

### 6.1 `modeling-reader-experience-auditor`

用三条读者路径检查：

1. 快速评阅者：摘要、问题回答、关键结果和结论能否在短时间定位；
2. 技术读者：变量、假设、算法、参数、验证和代码入口能否复原；
3. 非本专业读者：术语、图表和因果关系是否足够解释。

输出阅读摩擦地图、断裂位置、信息负担、应删/应移/应补内容和优先级。它不以“越详细越好”为目标。

### 6.2 `modeling-support-materials-auditor`

检查论文附录列出的文件与压缩包实际内容、代码可运行性、数据版本、图表来源、环境说明、身份信息和文件大小是否一致。该 skill 只依据规则 profile 检查，不把 CUMCM 限制套给其他比赛。

### 6.3 `modeling-final-preflight`

整合数学/数据/引用/术语/图表/阅读/格式/隐私/支撑材料/AI 披露检查。P0/P1 未关闭时阻断“冻结”，P2/P3 形成可接受风险清单，但由人决定是否提交。

## 7. AI 使用披露块（P0/P1）

### 7.1 `modeling-ai-use-disclosure`

详细设计见 [ai-disclosure-design.md](ai-disclosure-design.md)。其核心接口是：规则 profile + 明确授权的会话/日志范围 + 事件 schema + 人工确认队列 + PDF 渲染/验证。

### 7.2 `modeling-process-freezer`

在最终提交前固定论文、代码、数据、支撑材料、规则 profile、AI 事件和报告的版本/hash，生成交付清单。任何冻结后的修改都必须产生新版本，不覆盖旧记录。

## 8. 实现依赖图

```text
rules-profile ───────────────┐
problem-intake ──┐          │
assumption-ledger ─┼─> model-architect ─> experiment-validator ─┐
data-audit ───────┘                                             │
                                                                v
distinctiveness-coach ─> paper-architect ─> figure-designer ─> figure-table-auditor
        │                                      │                    │
        └────────────> claim-evidence-audit ───┼────────────────────┘
        │                                      │
        └────────────> terminology-auditor ────┼─> reviewer
                                               │       │
                                               v       v
                                      reader-experience  anti-homogenization
                                               \       /
                                                v     v
                                          naturalizer
                                                │
                                                v
                              support-materials + final-preflight
                                                │
                                                v
                                       ai-use-disclosure
                                                │
                                                v
                                       process-freezer
```

## 9. 第一轮实现顺序

1. 共享 schema、规则 profile、问题/假设/决策/主张/术语/差异化/图表设计模板；
2. `modeling-problem-intake`、`modeling-assumption-ledger`、`modeling-claim-evidence-audit`；
3. `modeling-distinctiveness-coach` 和 `modeling-anti-homogenization-auditor`；
4. `modeling-terminology-auditor`、`modeling-paper-reviewer`、`modeling-paper-naturalizer`；
5. `modeling-reader-experience-auditor`、`modeling-final-preflight`；
6. `modeling-ai-use-disclosure` 及 PDF 脚本；
7. 数据/实验/图表设计与支撑材料的工程化增强；
8. 使用一篇真实但已脱敏的数模论文做全流程回归，再决定合并或拆分技能。
