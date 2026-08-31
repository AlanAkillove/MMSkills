# 设计依据与迁移边界

1. [全国大学生数学建模竞赛赛区评阅工作规范（2025 年修订稿）](https://www.mcm.edu.cn/html_cn/node/011a3fefdb4951a8cb595400f44ec3df.html)要求评阅统一标准、独立评阅，并对突出创新点与相似度/疑似抄袭线索单独查证和记录。本 skill 仅迁移“线索—证据—人工查证”的流程，不把赛区相似度阈值或处置结论推广到其他赛事。
2. 本项目[反同质化设计](../../../docs/anti-homogenization-design.md)把同质化拆为题目、建模、论证、术语和表达五层；本 skill 增加了成稿后的 anchor coverage，避免只做词频或句式检查。
3. 本项目的[差异化写前教练](../../modeling-distinctiveness-coach/SKILL.md)负责在写前记录真实取舍，本 skill 负责成稿后回查是否被擦平；[AI 模板化痕迹审查](../../modeling-ai-pattern-reviewer/SKILL.md)只提供可观察文本信号；[主张—证据审查](../../modeling-claim-evidence-audit/SKILL.md)负责主张强度和证据覆盖。
4. [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)的模块化、证据契约和一致性扫描提供工程启发；不照搬期刊原创性标准、版式或英文写作偏好。

本 skill 不能证明原创、不能判断 AI 来源、不能预测奖项，也不能让 Agent 为了不同而改变题意、模型或术语。没有足够材料时必须保持 `unknown`。
