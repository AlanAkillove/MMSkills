# 跨宿主兼容性烟雾矩阵

本矩阵只记录适配所需的能力和验证动作，不把“仓库可以下载”写成“当前 Agent 已安装”。不同宿主的发现路径、插件机制、权限和脚本执行能力会随版本变化；真实安装仍需按 [跨 Agent 安装教程](../../docs/agent-skill-installation.md) 探测并记录结果。

适配器至少应验证：

1. 能否发现 `SKILL.md` 及其 frontmatter；
2. 是否保留 `references/`、`scripts/`、`schemas/`、`profiles/` 的依赖闭包和相对链接；
3. 是否能触发一个 skill 并产出结构化 artifact；
4. 是否保留人工门、未知状态和失败状态；
5. 若宿主不能执行脚本或读取历史会话，是否明确报告 `partial`/`blocked`，而不是伪造 `verified`。

矩阵中的 `fixture_only` 是仓库契约测试状态，不是对宿主当前版本的兼容性承诺。
