# 设计依据与迁移边界

1. CUMCM 公开格式规范要求论文附录列出支撑材料，支撑材料应包含支撑模型/结果/结论的必要材料和大篇幅中间图表；本 skill 将图表—数据—代码—论文的溯源与一致性作为审计接口，不把具体文件大小/版式直接泛化。
2. 本项目[阅读体验审计](../../modeling-reader-experience-auditor/SKILL.md)、[实验验证](../../modeling-experiment-validator/SKILL.md)、[数据审计](../../modeling-data-audit/SKILL.md)和[主张—证据审查](../../modeling-claim-evidence-audit/SKILL.md)共同指出图表脱节、单位/数字漂移、只报最好结果和读者无法定位主张是高频问题。
3. [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) 的“图表先建立结论—证据契约”和输出一致性扫描提供工程启发；不照搬 Nature 视觉规范或期刊版式。

图表审计不能从像素证明数据真实，也不能用视觉美观替代模型/实验/证据验证。无渲染件时视觉状态必须为 `unassessed`。
