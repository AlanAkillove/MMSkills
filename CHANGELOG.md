# Changelog

本文件记录可复用技能和共享契约的变化。

## [Unreleased]

### Added

- 初始化开源项目骨架；
- 建立全流程数模技能的总架构、反同质化设计、质量模型和分板块调研计划；
- 建立 AI 使用详情披露的规则适配与证据追踪设计草案。
- 增加跨审稿、自然化和阅读体验技能共用的防御性声明处理协议，并补充正反例契约测试。
- 完成首个生产级技能 `modeling-problem-intake` 的入口、图示/几何读取协议、字段契约、长题面 checkpoint 和脱敏正反例。
- 完成第二个生产级技能 `modeling-assumption-ledger` 的入口、假设字段契约、影响/验证指南、长材料 checkpoint 和脱敏正反例，并完成契约验证。
- 完成第三个生产级技能 `modeling-claim-evidence-audit` 的入口、主张矩阵 schema、强度校准表、证据审查工作流和脱敏正反例，并完成契约验证。
- 完成第四个生产级技能 `modeling-terminology-auditor` 的入口、术语账本 schema、保留/回退判据、跨产物一致性检查、共享模板和脱敏正反例，并完成契约验证。
- 完成第五个生产级技能 `modeling-ai-pattern-reviewer` 的入口、五层信号分类、模板化审查协议、研究依据和脱敏正反例，并完成契约验证。
- 完成第六个生产级技能 `modeling-paper-naturalizer` 的入口、修订保真契约、自然化模式、受保护语法、研究依据和脱敏正反例，并完成契约验证。
- 完成第七个生产级技能 `modeling-paper-reviewer` 的入口、六个数模审查透镜、finding 契约、独立审查工作流、研究依据和脱敏正反例，并完成契约验证。
- 完成第八个生产级技能 `modeling-distinctiveness-coach` 的入口、题目锚点—路径账本、强行创新护栏、研究依据和脱敏正反例，并完成契约验证。
- 完成第九个生产级技能 `modeling-anti-homogenization-auditor` 的入口、五层题目特异性覆盖审计、相似性授权防护、研究依据和脱敏正反例，并完成契约验证。
- 完成第十个生产级技能 `modeling-reader-experience-auditor` 的入口、三条读者路径、视觉/导航检查、研究依据和脱敏正反例，并完成契约验证。
- 完成第十一个生产级技能 `modeling-rules-profile` 的入口、规则来源/版本 schema、冲突与新鲜度处理、本地格式 PDF 核验依据和脱敏正反例，并完成契约验证。
- 完成第十二个生产级技能 `modeling-data-audit` 的入口、数据 manifest/字典契约、质量与缺失处理、时间/实体泄漏审计和脱敏正反例，并完成契约验证。
- 完成第十三个生产级技能 `modeling-model-architect` 的入口、基线优先模型注册、适配/复杂度比较、验证准备度和脱敏正反例，并完成契约验证。
- 完成第十四个生产级技能 `modeling-experiment-validator` 的入口、实验注册、验证矩阵、公平比较、不确定性/敏感性、复现契约和脱敏正反例，并完成契约验证。
- 完成第十五个生产级技能 `modeling-paper-architect` 的入口、章节/段落契约、论证映射、篇幅与图表计划和脱敏正反例，并完成契约验证。
- 完成第十六个生产级技能 `modeling-figure-table-auditor` 的入口、图表证据契约、数据/主张/单位核对、视觉检查和脱敏正反例，并完成契约验证。
- 完成第十七个生产级技能 `modeling-support-materials-auditor` 的入口、支撑 manifest、压缩包与执行安全、论文一致性和脱敏正反例，并完成契约验证。
- 完成第十八个生产级技能 `modeling-final-preflight` 的入口、八层提交前检查目录、状态/阻断/签核契约和脱敏正反例，并完成契约验证。
- 完成第十九个生产级技能 `modeling-literature-evidence` 的入口、来源/主张证据契约、检索与版本核验、引用安全边界和脱敏正反例，并完成契约验证。
- 完成第二十个生产级技能 `modeling-ai-use-disclosure` 的入口、会话授权与事件 schema、隐私/对账/规则映射、草稿与最终版 PDF 生成校验及渲染检查。
- 完成第二十一个生产级技能 `modeling-process-freezer` 的入口、状态谱系、SHA-256 manifest、上下文交接、冻结签核和哈希失效测试，并完成契约验证。
- 完成第二十二个生产级技能 `modeling-pipeline-orchestrator` 的入口、全流程依赖图、返工影响矩阵、人工门、只读路由脚本和未知状态失败测试，并完成契约验证。
- 完成第二十三个生产级技能 `modeling-figure-designer` 的入口、图表设计契约、选图规则、视觉系统、制作/交接流程、开源实践依据和脱敏正反例，并完成契约验证。
- 增强 `modeling-model-architect` 的用户决策支持：为候选模型增加通俗用途、分项评估、证据/未知、验证优先级、候选卡片和决策简报，并用理解确认门阻止总分、单一推荐和沉默同意替代人类决策。
- 增加跨 Agent 安装教程与可复制安装提示词：先探测宿主能力，再在原生标准目录、宿主适配器、插件/扩展、项目 instructions、单条提示词和阻断状态之间选择；补充依赖闭包、权限、安全、验证、manifest、升级与回滚要求。
- 将安装教程和 README 安装入口切换为公开仓库 `https://github.com/AlanAkillove/MMSkills`，补充 Git 获取源代码与项目级短安装提示词，同时保留跨宿主适配边界。
- 修正通用规则模板和 CUMCM 2026 profile 的 0.2 schema 对齐、YAML 引号与保守 `draft` 状态；补充编排器无 ready 阶段的安全动作测试。
- 增加开发依赖清单和 GitHub Actions 质量工作流，覆盖契约测试、YAML 解析、Python 编译和披露 PDF 草稿校验。
- 发布产物已移除本机磁盘路径和 Windows 用户名，并将命令统一为跨平台占位符。

### Pending

- 扩充 CUMCM 以外的赛事规则 profile，并在实际比赛前重新核验时效性；
- 持续用脱敏真实项目验证各 skill 的串联、返工影响和保守人工门；
- 评估本地日志采集/脱敏工具及 PDF/Word/LaTeX 交付验证工具是否需要独立拆分；
- 完成开源发布前的依赖、许可证、敏感信息和文档核对。
