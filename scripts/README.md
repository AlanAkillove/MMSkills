# Scripts

脚本只承担可重复、可验证的机械工作，例如：

- 检查技能目录和 frontmatter；
- 将结构化 AI 使用事件渲染为 Markdown/PDF；
- 校验披露报告中的未知字段、来源锚点和人工确认状态；
- 统计论文结构、术语一致性、图表引用和支撑材料清单；
- 检查最终 TeX/Markdown 的成文清洁风险，例如草稿/占位符、内部编号、过程性话语、重复防御性声明、摘要密度、交叉引用和列表密度；
- 从阶段注册表和运行档位生成 `effective_stage_policy` 与保守运行计划，并按 `canonical_issue_key` 合并跨透镜 finding；
- 运行行为级回归场景的结构化响应验证，以及 Codex 宿主 runner（缺失宿主不得算通过）；
- 对 PDF 做文本提取、页数/纸张/空白页、元数据泄露和可选光栅抽查（`skills/modeling-tex-paper-production/scripts/check_pdf_visual.py`）；
- 为 DeepSeek Harness 生成可选 `native-adapter` 镜像（`hosts/deepseek-harness/sync_adapter.py`），不改写源 skill。

脚本不应偷偷修改论文内容，也不应把模型判断包装成确定性事实。
