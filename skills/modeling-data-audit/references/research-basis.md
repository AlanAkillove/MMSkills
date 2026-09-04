# 设计依据与迁移边界

1. 历史项目中反复出现数据口径、单位、异常处理、代码—论文不一致和训练/测试泄漏；本 skill 将它们拆成 manifest、字典、变换决定和泄漏审计。
2. CUMCM 2026 格式规范要求支撑材料包含必要的可运行源代码、自主查阅的数据资料和大篇幅中间图表，并要求论文与支撑材料一致；本 skill 将这些要求作为可选规则 profile 输入，不把 CUMCM 文件要求泛化到其他赛事。
3. [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)的 evidence-first、artifact manifest 和一致性扫描提供工程启发；本 skill 按数模任务区分预测/解释/优化，不套用单一统计流程。
4. 与本项目的[假设账本](../../modeling-assumption-ledger/SKILL.md)、[模型架构](../../modeling-model-architect/SKILL.md)、[实验验证](../../modeling-experiment-validator/SKILL.md)和[主张—证据审查](../../modeling-claim-evidence-audit/SKILL.md)衔接；数据处理改变结论范围时必须进入人工确认。

数据审计不能证明数据真实、无偏或因果有效；它只能说明在已读范围和版本内，哪些问题已检查、哪些仍未知。
