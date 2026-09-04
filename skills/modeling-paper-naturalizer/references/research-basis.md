# 设计依据与迁移边界

1. [Chinese Academic Natural Revision](https://github.com/xiaofenggan01/aigc-reduce) 等公开项目的共同实践强调先诊断、结构级修改、保留学术语域、分块处理和不承诺检测器规避。本技能吸收这些原则，但按数模的题面、模型、数据、公式、代码和图表约束重建。
2. [academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer/blob/main/SKILL.md) 强调保留主张、作者声音、数字和证据，先审查再修改；本技能增加主张矩阵、假设账本、题目特异性和人工确认。
3. [Nature Portfolio 写作指南](https://www.nature.com/nature-portfolio/for-authors/write) 强调主发现清楚、必要术语解释、直接句子和图表服务于信息传递；本技能只迁移可读性原则，不迁移期刊格式或风格。
4. 本项目的[模板化痕迹审查](../../modeling-ai-pattern-reviewer/SKILL.md)、[术语规范审查](../../modeling-terminology-auditor/SKILL.md) 和[主张—证据审查](../../modeling-claim-evidence-audit/SKILL.md) 规定了自然化前的上游锁定和回退边界。
5. [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)（MIT）启发了负面证据、白名单最小修改和作者风格优先；不复制其 11 条规则或统计倍率，也不把通用中文写作阈值套到数模论文。

自然化不等于检测器规避、作者身份伪造或口语化；任何无法确认的实质变化都应保留为人工待决问题。
