# 设计依据与本地核验记录

1. [全国大学生数学建模竞赛人工智能工具使用规定（2026 年试行）](https://www.mcm.edu.cn/html_cn/node/fef94648f2836ab6cc81586f4c38512b.html)和 [2026 年参赛规则](https://www.mcm.edu.cn/html_cn/node/9d8e511fe7a1447b35f53a82c908e2e0.html)说明了 CUMCM 2026 的 AI、核心建模责任、竞赛保密和真实性边界；本 skill 只将它们固化为 CUMCM profile，不泛化到其他赛事。
2. 项目持有者提供的本地《全国大学生数学建模竞赛论文格式规范（2026 年修订稿）》副本已做文本抽取和前两页视觉核验：A4/页边距、纸质版页面结构、摘要页、正文 30 页、附录、电子版首页/文件大小、支撑材料 RAR/ZIP/20MB、文件列表和匿名信息等字段已记录在 `references/rules/cumcm-2026.yaml`；真实本地路径不写入公开仓库。生成规则 profile 时仍需检查官方最新链接和赛区附加要求。
3. [全国大学生数学建模竞赛赛区评阅工作规范（2025 年修订稿）](https://www.mcm.edu.cn/html_cn/node/011a3fefdb4951a8cb595400f44ec3df.html)要求统一评阅要点、独立评阅和对相似度/疑似抄袭线索单独记录；本 skill 借鉴来源和版本记录，不把评阅处置阈值变成通用规则。
4. 与本项目的[AI 披露设计](../../../docs/ai-disclosure-design.md)、[CUMCM 规则快照](../../../references/rules/cumcm-2026.md)、[项目 source register](../../../docs/research/source-register.md)衔接；任何 profile 的最终状态由目标赛事、适用范围和人工确认决定。

规则 profile 是可审计的工作资料，不是法律意见、官方解释或自动合规保证。
