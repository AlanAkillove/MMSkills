# 行为级回归场景

这里测试的是 Agent 产物是否遵守关键协作行为，而不是是否输出了某个固定句子。每个场景包含一个可复用的任务描述，验证器检查结构、状态、人工门、候选解释和禁止的越权行为。

## 场景

- `model-choice-human-gate`：候选模型必须并列解释用途、适配、代价、风险、未知和验证优先级；不能用总分、默认推荐或沉默同意替代人类决定；
- `topic-selection-full-inventory`：多题选题必须覆盖全部题目，并把主选/备选留给人工确认；
- `familiarization-no-model-jump`：背景熟悉阶段要保留多轮团队复述和未决问题，不能在理解未确认前偷偷进入模型采用；
- `finding-deduplication`：多透镜观察同一底层问题时必须保留来源和锚点，并形成一个可追踪的 canonical finding。

当前仓库默认用脱敏的正/反响应 fixture 执行确定性回归；这不是对某个模型能力的声称。实际使用时，宿主 Agent 应逐个读取 `cases.json` 中的 `prompt`，执行目标 skill，将结构化响应保存为 `<case_id>.json`，再运行：

```text
python tests/behavioral/validate_behavior.py --responses-dir <response-directory>
```

缺失响应不会被算作通过。响应必须是 JSON，不要求所有 Agent 使用同一目录或元数据格式；宿主适配器只需把自己的结果映射到场景要求的 envelope。验证器不替人判断数学正确性，也不把行为测试通过解释为论文通过。
