# 共享机器可读契约

本目录是跨 skill、跨 Agent 传递状态的机器可读契约。Markdown 模板用于人阅读和讨论，JSON Schema 用于约束结构；两者不应各自发展出互相冲突的字段。

当前核心契约：

- `stage-registry.json`：全流程唯一阶段注册表；编排器脚本从这里读取阶段顺序、硬依赖、`recommended_after` 软建议、`gate_type` 和审查透镜映射；
- `stage-registry.schema.json`：阶段注册表自身的结构契约；
- `pipeline-state.schema.json`：项目状态与续接状态；路由入口先用它做 Draft 2020-12 校验，再做跨字段语义检查；
- `finding.schema.json`：审稿、术语、图表、阅读体验、AI 模板化和反同质化发现的共同 envelope；
- `evidence.schema.json`、`decision.schema.json`：证据与人类决策的最小记录；
- `model.schema.json`、`experiment.schema.json`：候选模型和实验记录；
- `ai-use-event.schema.json`：AI 使用事件记录，与赛事披露呈现分离。
- `run-profile.schema.json`：运行档位 YAML 的共同字段契约。镜头名受枚举约束；human gate/review gate 是否属于注册表由交叉测试检查，因为 JSON Schema 不能动态引用 registry。

阶段注册表中的 `depends_on` 是真正会影响 ready 的硬依赖；`recommended_after` 只是推荐先后，不应阻断用户明确要求的解释、探索、续写或局部修稿。`core_decision` 的人工确认在最终采用/定稿/冻结前仍然不可省略，`review_checkpoint` 默认是可延后的核对点。

这些 schema 不替代人工确认，也不把结构合法误认为数学正确。修改字段时应同步更新对应 skill、模板、fixtures、ADR 和变更记录；对既有字段做破坏性修改必须提供迁移说明。
