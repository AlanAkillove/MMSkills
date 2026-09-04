# 数模学术语言信号登记

独立重写的候选信号，不是外部 11 条规则的拷贝。机械扫描只产出 `candidate`。是否构成模板化仍由 Agent 结合题目、证据和风格基线判断。

字段：`signal_id`、`layer`、`detection`、`academic_transfer`、`false_positive_contexts`、`repair_action`、`protected_content`、`source_basis`、`mmskills_rationale`。

## evidence-backed（高转移）

```yaml
signal_id: SYN-ISO-SENT
name: 相邻句句法同构
layer: evidence-backed
trigger: 连续三句及以上共用同一主语框架（如“对问题X，本文建立……”）且未引入不同输入/约束/结果
detection: mechanical
academic_transfer: high
false_positive_contexts: 题面要求逐问作答、步骤清单本身必须平行
repair_action: 保留各问事实，打破无信息的同构外壳
protected_content: 数字、模型名、变量
source_basis: MMSkills 数模摘要/分问叙述观察；外部对照研究仅作方法启发
mmskills_rationale: 分问同构是竞赛稿常见空转，与题目特异性冲突
```

```yaml
signal_id: SYN-EMPTY-COLON
name: 空转提示语加冒号
layer: evidence-backed
trigger: “核心是：/原因如下：/本文主要工作如下：”等前半句无信息，只宣布后文
detection: mechanical
academic_transfer: high
false_positive_contexts: 定义句“记为：/定义为：”、公式后解释、合法列表标题
repair_action: 删空转壳，让对象或结果直接出现
protected_content: 列表项内容、数字
source_basis: 内部模板稿观察
mmskills_rationale: 冒号本身合法；空转壳才是问题
```

```yaml
signal_id: SYN-ZERO-ANAPHORA
name: 段首评论缺回指
layer: evidence-backed
trigger: 非首段以“值得注意的是/需要指出的是”起句且未点明对象
detection: mechanical
academic_transfer: high
false_positive_contexts: 紧接指明“该压降/式(12)”
repair_action: 补回指或并入上一结果句
protected_content: 主张边界
source_basis: 内部阅读摩擦；外部项目报告过类似篇章现象（语料不可核验）
mmskills_rationale: 同时损害阅读路径，可交 Reader 补充
```

```yaml
signal_id: LEX-PERSONIFY
name: 理想化人格喻体
layer: evidence-backed
trigger: “该模型如同一个智慧决策者”等职业/人格拟人，且无说明功能
detection: mechanical
academic_transfer: high
false_positive_contexts: 题面本身是人/组织决策对象
repair_action: 改回对象—机制—结果
protected_content: 模型名称与方程
source_basis: 数模论文极少需要人格喻体
mmskills_rationale: 包装性表达，易掩盖机制
```

## contextual（条件使用）

```yaml
signal_id: SYN-REFRAME
name: 虚假翻案
layer: contextual
trigger: “这不仅是 A，更是 B”且文中没有旧解释→新解释的论证
detection: mechanical
academic_transfer: conditional
false_positive_contexts: 确实比较了两种问题表述并给出证据
repair_action: 写成实际对象与任务；禁止无依据升格
protected_content: 问题类型、约束
source_basis: 内部高承诺包装观察
mmskills_rationale: occurrence ≠ finding
```

```yaml
signal_id: SYN-TRIAD
name: 无功能并列框架
layer: contextual
trigger: 跨段/跨子问机械重复同一并列壳，或三点没有真实论证功能
detection: semantic
academic_transfer: conditional
false_positive_contexts: 题面三个并列任务、真实步骤顺序
repair_action: 按问题驱动层次合并或拆开
protected_content: 步骤事实
source_basis: 内部成稿
mmskills_rationale: 问题不在“三”或“首先其次”，在无功能重复
```

```yaml
signal_id: DISC-CONNECTOR
name: 句首连接词机械重复
layer: contextual
trigger: 连续句首“因此/此外/然而”且没有真实因果/并列/转折
detection: semantic
academic_transfer: conditional
false_positive_contexts: 作者全文稳定使用“因此，由式(n)可得”
repair_action: 删无功能连接，保留真实推理
protected_content: 公式引用、结论强度
source_basis: 学术篇章标记在数模中合法
mmskills_rationale: 不得改成口语“也/其实”
```

```yaml
signal_id: DISC-THIS-MEANS
name: “这表明”复述
layer: contextual
trigger: “这表明/这意味着”只重复前一句，没有新推论
detection: semantic
academic_transfer: conditional
false_positive_contexts: 后接新的适用范围或定量结论
repair_action: 删除复述或并入证据句
protected_content: 数字与模态词
source_basis: 内部套话
mmskills_rationale: 连接词本身不是 AI 信号
```

```yaml
signal_id: PUNC-DASH
name: 破折号高密度
layer: contextual
trigger: 同一段多次揭晓式破折号，打断论证
detection: mechanical
academic_transfer: conditional
false_positive_contexts: 一次解释性破折号、变量说明
repair_action: 改为括号或独立句
protected_content: 被解释的术语
source_basis: 学术论文可合理使用破折号
mmskills_rationale: occurrence ≠ finding
```

## rejected_as_ai_signal

`sentence_length_uniformity`、`paragraph_length_uniformity`、`passive_voice`、`question_sentence`、`metaphor_general`、`body_ordinal`、`in_sentence_parallelism`、`colon_count`、`dash_count`。详见 [negative-signal-registry.md](negative-signal-registry.md)。
