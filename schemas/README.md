# 共享机器可读契约

本目录是跨 skill、跨 Agent 传递状态的机器可读契约。Markdown 模板用于人阅读和讨论，JSON Schema 用于约束结构；两者不应各自发展出互相冲突的字段。

当前核心契约：

- `stage-registry.json`：全流程唯一阶段注册表；编排器脚本从这里读取阶段顺序、依赖和人工门；
- `stage-registry.schema.json`：阶段注册表自身的结构契约；
- `pipeline-state.schema.json`：项目状态与续接状态；
- `finding.schema.json`：审稿、术语、图表、阅读体验、AI 模板化和反同质化发现的共同 envelope；
- `evidence.schema.json`、`decision.schema.json`：证据与人类决策的最小记录；
- `model.schema.json`、`experiment.schema.json`：候选模型和实验记录；
- `ai-use-event.schema.json`：AI 使用事件记录，与赛事披露呈现分离。
- `run-profile.schema.json`：运行档位 YAML 的共同字段契约。

这些 schema 不替代人工确认，也不把结构合法误认为数学正确。修改字段时应同步更新对应 skill、模板、fixtures、ADR 和变更记录；对既有字段做破坏性修改必须提供迁移说明。
