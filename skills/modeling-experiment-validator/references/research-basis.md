# 设计依据与迁移边界

1. CUMCM 2026 格式规范要求必要源程序可运行、支撑材料与论文内容相符；本 skill 将代码/数据/图表/论文的版本和输出映射作为复现契约，不把某一赛事的文件大小/提交字段硬编码为实验标准。
2. 本项目[数据审计](../../modeling-data-audit/SKILL.md)、[模型架构](../../modeling-model-architect/SKILL.md)和[主张—证据审查](../../modeling-claim-evidence-audit/SKILL.md)共同指出泄漏、只报最优、缺基线、结果越界和代码—论文不一致是高频返工源。
3. [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)及公开科学写作/审查实践提供 evidence-first、artifact manifest 和差异回归启发；本 skill 依据数模的预测/优化/仿真/决策任务重新定义验证类型。

实验注册不能证明模型真理或现实因果，只能把运行设置、输出、失败和主张范围变成可复核记录。
