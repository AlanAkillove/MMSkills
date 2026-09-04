# 设计依据与迁移边界

1. 用户提供的 CUMCM 2026 格式规范规定论文与支撑材料分开提交，附录列出文件列表，支撑材料至少包括必要可运行源代码、必要自主查阅数据和大篇幅中间图表，并限制匿名信息与文件大小；本 skill 仅通过 rules profile 读取这些条件。
2. CUMCM 2026 AI 规定要求使用 AI 时提交 `AI工具使用详情.pdf`，但具体适用规则仍由 [rules profile](../../modeling-rules-profile/SKILL.md) 和目标年份/赛区决定。
3. 本项目[实验验证](../../modeling-experiment-validator/SKILL.md)、[图表审计](../../modeling-figure-table-auditor/SKILL.md)、[数据审计](../../modeling-data-audit/SKILL.md)和[AI 披露](../../modeling-ai-use-disclosure/SKILL.md)提供代码/数据/图表/论文的证据链接口；本 skill 只检查交付包和安全，不替代内部验证。

支撑材料审计不能保证代码无漏洞、数据有权利或模型正确；默认静态检查，不执行陌生内容。
