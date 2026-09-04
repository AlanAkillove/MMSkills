# 负面信号登记

这些现象**不得单独**作为 AI-pattern / 模板化 finding。它们可以出现在学术论文里，也可以是阅读体验或术语规范问题。本表用来阻止误报，不是改写清单。

方法启发来自公开项目 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)（MIT）所报告的对照分析：流行“AI 味”清单中多项未获其语料支持。该项目语料因版权/隐私未公开，第三方无法核验；人类侧为公开文章，不是数学建模学术论文。因此本仓库**不复制其倍率或阈值**，只吸收“负面证据 + 白名单最小修改 + 作者风格优先”的方法。

| 不得单独作为 AI-template 证据 | 可以在哪里检查 |
|---|---|
| 句子较长 | Reader Experience |
| 句长比较均匀 | 一般不检查 |
| 段落长度相近 | 一般不检查 |
| 被动句 | 学术语言正常现象 |
| 名词化本身 | 学术语言正常现象 |
| 正文“首先/其次/最后” | 只检查逻辑功能或跨段机械重复 |
| 问句 | 不作为 AI 信号 |
| 比喻 | 不作为 AI 信号 |
| 句内排比 | 不作为 AI 信号 |
| 正式书面语 | 不作为 AI 信号 |
| 标准术语重复 | Terminology 正常现象 |
| 图表配色统一 | Figure consistency 正常现象 |
| 句首“因此/此外/然而” | 只检查无真实逻辑关系的机械重复 |
| 定义/列举用冒号 | 只检查空转提示语+冒号 |
| 破折号出现一次 | 只检查高密度或揭晓式堆叠 |
| 编号小标题“一、二、三” | 只检查同构编号且标题无信息功能 |

`rejected_as_ai_signal` 名称：`sentence_length_uniformity`、`paragraph_length_uniformity`、`passive_voice`、`question_sentence`、`metaphor_general`、`body_ordinal`、`in_sentence_parallelism`。
