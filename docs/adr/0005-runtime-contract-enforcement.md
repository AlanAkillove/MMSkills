# ADR 0005：让已冻结合同具有运行时效力

## 状态

已接受（运行时语义迭代）

## 背景

ADR 0004 把阶段注册表、共享 finding、运行档位和行为回归写入了仓库。随后的评审指出：这些合同当时主要是声明性的。`route_pipeline.py` 会打印 profile 路径，但不消费 `artifact_policy` / `review_policy`；`validate_state()` 浅于 `pipeline-state.schema.json`；finding 合并把锚点集合当作分组键；registry 中几乎每个阶段都叫 `human_gate: required`，与 contest profile 的压缩门清单冲突。

## 决策

1. 编排器构造 `canonical graph + run profile = effective_stage_policy`。canonical `depends_on` 不变；档位只把部分审查阶段标为 `selected` / `skipped-with-policy` / `not_selected`，并把产物投影写成 full 或 compact。
2. 路由入口先运行 `Draft202012Validator`，再检查 JSON Schema 难以表达的语义：`human-confirmed` 必须有 `decision_id`，`skipped` 必须有 reason，`current_stage` 和 stage 名必须属于 registry，state 中的 `depends_on` 不得与 registry 冲突。
3. finding 合并以 `canonical_issue_key` 为分组主键；锚点用于判断 duplicate/supplement/conflict。合并时 union 锚点和关联 ID；`open` 与 `resolved`、冲突的 `human_status` 不得被首条记录覆盖。
4. registry 增加 `gate_type = core_decision | review_checkpoint | none`。profile 只能压缩后两类，交叉测试要求每个 profile 的 `human_gates` 都能在 registry 中解析，且包含全部 `core_decision`。
5. 增加 Codex 行为 runner：`case → 可选宿主执行 → normalize envelope → validate → 保存 host/model/version/date/results`。CI 默认不调用真实宿主；缺失宿主记录为 `not_run`，不得算通过。Claude/Gemini 仍为 `fixture_only`。

## 后果

档位现在会改变 ready 集合和计划文本，因此测试必须覆盖 `contest-fast` 与 `research-full` 的差异。真实 Codex 运行结果默认留在本地 `tests/behavioral/results/runs/`，不作为 compatibility 已验证的证据。架构本身继续冻结，下一阶段应是脱敏真实项目上比较 `contest-standard` 与 `contest-fast` 的耗时、人工打断和返工量。
