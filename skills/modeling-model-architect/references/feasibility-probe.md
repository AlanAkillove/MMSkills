# 模型可行性探测

正式大编码前，用很小的成本证伪明显算不了的方案。Probe 不是评分，也不是选型菜单。

## 原则

- 只检查当前候选真正可能失败的地方，不套通用百分制。
- 失败只说明“现在不宜投入实现”，不自动改成更复杂的算法。
- 没有有意义的对照时，不要为了探测而编造 baseline。
- 探测记录可丢弃；只有影响采用决定时才留盘。

## 按问题族选择检查（示例，不是必填清单）

物理/工程：方程是否闭合、量纲是否一致、边界是否足够、参数能否取得或可辨识、极限情形是否荒谬、计算规模能否在比赛时间内承受。

优化/决策：约束是否可能可行、变量规模、目标是否退化、求解器时间预算。

统计/学习：样本量、目标是否可得、泄漏、划分、输出是否退化。

## 记录字段

```text
candidate_id
family: physics | optimization | stats_ml | other
checks[]: name, result (pass|fail|unknown), note
verdict: feasible_to_try | not_now | unknown
```

禁止 `overall_score`、`award_probability` 或把探测写成模型排名。
