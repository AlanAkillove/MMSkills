# 多轮理解 checkpoint

```text
topic_id:
status: partial | needs_human | blocked | human-confirmed
last_round_id:
last_evidence_id:
last_source_id:
```

## 轮次记录

### `round_id`

```text
date:
focus:
materials_read:
```

#### Agent 本轮说明

（标出题面锚点、来源锚点和不确定项。）

#### 团队复述或问题

（记录原意，不用“已理解”代替。）

#### 证据核对与差异

| 项目 | 团队说法 | 原材料/来源 | 状态 | 是否影响后续 |
|---|---|---|---|---|
|  |  |  |  |  |

#### 纠正与新未知

- 纠正：
- 新未知：
- 受影响 artifact：
- 下一轮问题：

## 完成确认

```text
confirmed_scope:
confirmed_by:
date:
decision_id:
```

确认只覆盖背景、对象关系、子问、术语/单位和文献边界；正式假设、模型、实验和结论仍需后续人工门。
