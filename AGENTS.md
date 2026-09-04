# MathModelingSkills Maintainer Guide

## 工作范围

这是一个数学建模竞赛全流程 skill 仓库。新增内容要优先解决可复现的真实问题，并能在题意、模型、数据、论文和提交材料之间建立证据链。

## 强制边界

- 核心题意解释、关键假设、模型取舍、数据处理、结果结论和最终提交由人类确认；
- 规则必须带赛事、年份、来源和核验日期，并写在使用该规则的 profile 或 skill 内；
- 不以规避 AI 检测器为功能目标，不输出作者身份结论；
- 不猜测缺失的模型版本、时间、prompt、回复、人工修改或采纳情况；
- 不提交真实私人会话、未公开赛题、队伍身份和未授权数据；
- 不为了差异化而强行引入复杂模型、生造术语或改变事实。

## 公开仓库面

`main` 只保留运行本体、用户文档和正常开源维护设施。下列内容不得提交到公开仓库：

- 临时设计计划、scratch notes、Cursor/Codex 工作备忘；
- 内部调研日志、开发过程中的研究总账；
- 历史用户项目归纳、私人会话分析；
- 已被当前架构取代的设计草案。

Development scratch notes, private research logs, project-specific findings, and temporary planning documents must not be committed to the public repository. 把它们放在已被忽略的 `.dev-notes/`、`.local-research/` 或 `scratch/`。

## 实现约定

- 每个 skill 以一个短 `SKILL.md` 为入口，长资料按需放在 `references/`；
- 共享状态优先使用 `templates/` 中的 schema，不在各 skill 内重复定义同一字段；
- 机械、可确定的检查写脚本；判断性结论必须保留证据位置、置信度和人工确认状态；
- 长文和长会话采用分块索引、状态摘要和可续接 checkpoint；
- 修改论文时锁定数字、公式、引用、代码和结论，生成前后对照与变更日志；
- 生成 PDF 后做结构化字段/可行时的文本提取、文件属性、敏感信息和视觉版式检查；若字体编码导致文本抽取不可靠，必须明确记录并以渲染检查为准；
- 证据跟着使用它的功能走，不维护“开发时看过什么”的中央登记。

## 提交前检查

1. 若用户可见接口、安装方式或质量标准变化，更新对应 README / `docs/` 用户文档；
2. 更新 `CHANGELOG.md`；
3. 为正常输入和失败/未知输入添加脱敏 fixtures；
4. 运行项目脚本和产物检查（含 `pytest`）；
5. 核对规则来源仍写在对应 profile 或 skill 内；
6. 在变更记录中说明人工确认点和剩余风险。

不要为了“留下设计痕迹”新增 ADR、研究计划和来源总账。架构理由写进 `docs/architecture.md`；实际复用第三方代码或文档时，用文件头和 `THIRD_PARTY_NOTICES.md` 履行许可证义务。
