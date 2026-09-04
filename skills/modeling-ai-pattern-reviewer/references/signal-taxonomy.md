# 模板化信号分类

本表用于提出可核验观察，不是“AI 特征词典”，也不是作者归因器。同一信号必须结合题目、证据、学科惯例和作者风格基线判断。

信号分三层：

- `evidence-backed`：可定位的模板化表达，允许进入 AI-pattern finding（仍禁止来源归因）；
- `contextual`：只有在缺少真实论证功能、跨段机械重复或与题目脱节时才升级；
- `readability-only`：句长、节奏、导航负担等，移交 `modeling-reader-experience-auditor`，**不得**记为 AI-pattern。

完整条目见 [academic-signal-registry.md](academic-signal-registry.md)。禁止单独使用的现象见 [negative-signal-registry.md](negative-signal-registry.md)。机械候选扫描见 `scripts/scan_language_signals.py`（输出 `candidate`，不是 error/AI 分数）。

## 五层观察

| 层面 | 可进入 AI-pattern 的观察 | 需要的对照 |
|---|---|---|
| 结构 | 每个子问复制相同章节套路；背景/创新/展望可替换到别题；模型清单与题目特征无关 | 子问映射、题目特有事实、差异化账本 |
| 句法/篇章 | 跨段重复结构、无功能并列框架、相邻句句法同构、空转提示语+冒号、虚假翻案、段首评论缺回指；没有新增信息的防御性声明簇 | 同一论文其他段落、作者保留的实验/失败段、读者任务、防御性声明协议 |
| 词汇/术语 | 抽象名词堆叠、宣传性形容词、无功能高承诺词、同义词轮换、理想化人格喻体 | 术语账本、定义/证据、普通直接表达 |
| 论证/证据 | 贡献/创新/结论没有 claim/evidence 锚点；主张强度相同而证据责任不同；局限只用模板句 | 主张—证据矩阵、实验登记、假设账本 |
| 图表/交付 | 图表装饰性强；图注只是“如图所示”；不同证据任务使用同一叙述模板 | 图表注册、源代码、图表回答的问题 |

图表配色统一、标准术语重复不是本层信号。

## 已降级、不得再当 AI-pattern

以下曾出现在经验清单中，现降级：

| 旧说法 | 0.3.1 处理 |
|---|---|
| 均匀三点式 / 正文“首先、其次、最后” | 不因“三”或序数词报 AI-pattern；只检查无功能并列或跨段机械重复（`SYN-TRIAD` / `SYN-ISO-SENT`） |
| 长句叠加 | 移交 Reader Experience |
| 每段同节奏 / 句长均匀 / 段长均匀 | 不再作为 AI-pattern |
| 过度对称 | 必须有跨句/跨段结构证据，不能凭语感 |
| 问句、比喻、句内排比、被动句、名词化本身 | `rejected_as_ai_signal` |
| 连接词过密 / 句首“因此” | 只在连续机械重复或没有真实逻辑关系时作 `DISC-CONNECTOR` candidate |

## 风格基线

作者/用户明确指定风格 > 同一论文已人工确认的成熟章节 > 目标学科/数模学术规范 > MMSkills 通用规则。通用 signal 与作者稳定写法冲突时，作者风格优先；题意、证据和学术规范仍高于风格偏好。

## 防御性声明簇的专门判据

`defensive_statement_cluster` 是句法/篇章或论证/证据层的子类型，不是作者来源判断。候选句常包含元话语、自我免责或预先否认，但只有同时满足以下条件才提高置信度：

1. 在相邻句、同一小节或多个结论位置重复相同功能；
2. 删除或合并后不会丢失新的对象、条件、证据、范围、局限或合规要求；
3. 声明打断了结果—证据—边界的顺序，造成可定位的阅读负担。

若声明承担 `scope_boundary`、`uncertainty`、`limitation` 或 `ethics_compliance` 功能，应记录为需要保留/合并的保护内容，而不是删除目标。具体动作按共享的[防御性声明处理协议](../../../references/defensive-statement-protocol.md)执行。

## 记录格式

```yaml
signal_id: SYN-ISO-SENT
layer: evidence-backed | contextual | readability-only
status: candidate
locations: []
observed_pattern: null
contrast_or_anchor: []
reader_or_argument_impact: null
alternative_explanations: []
confidence: high | medium | low
severity: P0 | P1 | P2 | P3
repair_options: []
requires_human_decision: true
```
