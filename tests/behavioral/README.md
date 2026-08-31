# 行为级回归场景

这里测试的是 Agent 产物是否遵守关键协作行为，而不是是否输出了某个固定句子。每个场景包含一个可复用的任务描述，验证器检查结构、状态、人工门、候选解释和禁止的越权行为。

## 场景

- `model-choice-human-gate`：候选模型必须并列解释用途、适配、代价、风险、未知和验证优先级；不能用总分、默认推荐或沉默同意替代人类决定；
- `topic-selection-full-inventory`：多题选题必须覆盖全部题目，并把主选/备选留给人工确认；
- `familiarization-no-model-jump`：背景熟悉阶段要保留多轮团队复述和未决问题，不能在理解未确认前偷偷进入模型采用；
- `finding-deduplication`：多透镜观察同一底层问题时必须保留来源和锚点，并形成一个可追踪的 canonical finding。

当前仓库默认用脱敏的正/反响应 fixture 执行确定性回归；这不是对某个模型能力的声称。若要把真实宿主输出送入同一验证器，先用 Codex runner：

```text
python tests/behavioral/run_host_case.py --host codex --all --output-dir tests/behavioral/results/runs
```

默认不会调用宿主，结果为 `not_run`。只有在明确传入 `--execute` 且本机存在 `codex` CLI 时才会真正跑 case。也可以把已有宿主输出交给 `--from-response`，runner 会 normalize envelope、调用验证器，并保存 host/model/version/date。缺失响应或缺失宿主都不会被算作通过。

宿主适配器只需把自己的结果映射到场景要求的 envelope。验证器不替人判断数学正确性，也不把行为测试通过解释为论文通过。Claude Code 与 Gemini CLI 仍保持 `fixture_only`。
