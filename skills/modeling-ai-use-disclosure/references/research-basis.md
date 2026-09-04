# 研究与设计依据

本 skill 借鉴了规则原文、项目内历史会话协议、学术审稿/研究协作实践和开源 skill 的工程组织方式，但没有复制任何外部 skill 的提示词或赛事文本。

## 直接依据

- 中国大学生数学建模竞赛 2026 年 AI 使用规则：<https://www.mcm.edu.cn/html_cn/node/fef94648f2836ab6cc81586f4c38512b.html>（2026-09-01 再核验；此前 2025 试行规定已失效）
- 2025 年试行规定（仅作对照，不得执行）：<https://www.mcm.edu.cn/html_cn/node/eebcfb6dc37fd2de9603dc16026fdf01.html>
- 中国大学生数学建模竞赛 2026 年论文格式规范：<https://www.mcm.edu.cn/html_cn/node/4cd596519c9eb9fbd866398f6df0caa3.html>
- 项目内规则 profile：`../../../references/rules/cumcm-2026.yaml`
- 项目内历史会话读取协议：`../../../references/ai-use-history-protocol.md`
- 项目内规则到 PDF 的映射：`profile-to-pdf.md`

## 设计迁移

- 从开源学术 skill 借鉴“角色边界、渐进式读取、证据链、质量门和可复用 references”的组织方式；
- 从论文自然化和审稿 skill 借鉴“保护事实、把未知显式化、发现问题不直接替作者篡改”的人类控制原则；
- 结合数模赛事实际增加规则 profile、事件族去重、论文/代码/数据对账、匿名化、support archive 和 PDF 渲染 QA；
- 不把 AI 检测分数、所谓“降 AI 率”或模型自述当作使用历史证据；不对历史会话之外的内容作推断。

## 时效性

赛事规则、AI 工具版本和平台记录能力会变化。每次生成前重新验证 profile；本文件的链接只说明研究入口，不能替代当前赛事官方规则。
