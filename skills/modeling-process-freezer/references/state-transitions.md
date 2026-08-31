# 状态转移与失效

## 状态语义

| 状态 | 含义 | 最低条件 |
| --- | --- | --- |
| working | 正在形成或修改 | 可有缺失和未知，不可称为已审查 |
| reviewable | 产物和索引齐备，等待专项审查/人工门 | 依赖可定位，未决问题已列出 |
| frozen | 指定范围和版本已由人确认 | manifest/hash 通过，核心决定有签核，阻断问题已处理或被明确接受 |
| blocked | 有问题阻止继续或冻结 | 记录阻断原因、证据和解锁动作；仍可保存快照 |
| superseded | 被后续快照取代 | 指向新快照，保留原 hash 和差异 |
| released | 完成最终预检并获得提交前签核 | 规则、论文、支撑、披露和身份/格式检查均通过；不等于实际上传 |

## 允许转移

~~~
working -> reviewable | blocked
reviewable -> frozen | blocked | working
frozen -> superseded | released
blocked -> working | reviewable
superseded -> (terminal; create a child snapshot)
released -> superseded   # 任何受影响变更都必须回退为新候选
~~~

状态回退不删除历史；新的快照写明回退原因和受影响 artifacts。没有父快照时，首个 working 快照可以为 parent_snapshot_id=null。

## 失效触发器

以下任一发生，就把相关快照标为 needs_recheck/superseded（若 schema 不支持该状态，则在 invalidated_by 记录并创建新快照）：

- 论文、代码、数据、图表或支撑材料 hash 变化；
- 题意/假设/模型/指标/结论或 AI 披露的人工决定变化；
- 规则 profile 的来源、版本、生效日期或字段变化；
- 术语定义、符号单位、主张证据或图表数据变化；
- 生成器、依赖、随机种子或运行环境变化到会影响结果；
- 自然化/结构重写触及受保护字段但没有回归；
- 发现来源范围越权、隐私泄露、版本冲突或未记录的外部输入。

## 签核范围

签核只对写明的 scope 生效。例如“确认语言修订快照”不能自动确认模型、实验和 AI 核心使用事件；“确认 PDF 排版”不能自动确认 PDF 中的事实。范围扩大必须重新签核。
