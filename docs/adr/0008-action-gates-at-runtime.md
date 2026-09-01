# ADR 0008：动作门落到运行时

- 状态：accepted
- 日期：2026-09-01
- 适用版本：0.2.2
- 修订：ADR 0007 的运行时补全，不改变“skills 是辅助知识”的方向

## 背景

0.2.1 把依赖拆成三层，并把确认描述为动作门，但 registry 仍只有 `human_gate` / `gate_type`。运行时只要 stage 是 `core_decision`，`blocking` 就始终为真；`adoption_requires` 只认 `passed/skipped`。计划里的 Safe next action 还会强制读取 process-freezer manifest。结果是：探索仍可能被写成“先停下来等确认”，而删除异常一类的 adopt 又没有机器规则拦住。

## 决策

1. Registry 增加 `default_action_gates` 和可选的每阶段 `action_gates` overlay。`blocking` 等于当前 `user_intent.action` 的 gate 是否为 `required`。
2. `execution_satisfied()` 保持 `passed/skipped` 或政策跳过；`adoption_satisfied()` 对 `adopt=required` 或 `core_decision` 前置额外要求 `human-confirmed` 和 `decision_id`。
3. `data_audit` 虽是 review checkpoint，其 `adopt`/`freeze`/`submit` 为 required，防止未确认的异常删除或切分变更进入后续采用。
4. Safe next action 按 `working_depth`、入口类型和用户意图生成。light/local turn 直接继续当前任务，不强制打开 freezer manifest。
5. 规范义务字段使用 `required | prohibited | not_required | unspecified`。CUMCM 2026 对参考文献列 AI、正文标注、参考文献后未使用声明和全文交互日志记为 `not_required`，不是 `prohibited`。
6. 默认 TeX 附录改为开关；复现/支撑材料章节移到 example。高频写作 skill 继续瘦身，SOP 放入 `references/recommended-workflow.md`。

## 未在本版完成的验证

脱敏 regex 回归不能证明真实 Agent 写得更好。第一次 live 回放协议见 `tests/fixtures/paper-regression/replay-protocol.md`；完成前不得把 0.2.2 宣传为“test1 已重跑成功”。

## 后果

- 用户说“比较几个模型”时，`model_architect.blocking` 为 false，Safe next action 是 continue the requested task；
- 要把模型写成已采用，需要题意范围且 `problem_intake` 已有 human-confirmed decision；
- 删除异常并让后续模型采用时，计划会把 `data_audit` 标为当前动作的 required gate。
