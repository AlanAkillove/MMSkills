# 编排状态契约

## 顶层状态

建议 project_state/pipeline_state.yaml 或等价 JSON 包含：

~~~
schema_version:
project_id:
mode: compose | revise | audit | disclose | final_check
entry_status: confirmed | ambiguous | unknown
current_stage:
stages: {}
artifacts: []
gates: []
open_issues: []
last_snapshot_id:
event_log: []
updated_at:
~~~

项目 ID 可以是用户提供的内部 ID；不要使用姓名、账号或秘密作为 ID。

## 阶段条目

每个 stages[id] 至少记录：

~~~
skill:
status: not_started | ready | in_progress | needs_human | passed | blocked | stale | skipped | superseded
depends_on: []
inputs: []
outputs: []
human_gate: required | optional | not_applicable
last_run_at:
source_snapshot_id:
evidence_status: confirmed | partial | unknown | conflict
decision_ids: []
issue_ids: []
reason:
~~~

passed 只表示该阶段契约已通过，不表示所有上游事实正确；skipped 必须有不适用理由和人工决定；stale/superseded 不能作为下游依赖的通过条件。

## 事件日志

状态写回采用追加事件，不覆盖旧事实：

~~~
event_id, at, actor, action, stage, old_status, new_status,
input_snapshot_id, output_ids, decision_id, reason
~~~

actor 可以是 human、agent 或 connector，但核心门的 decision_id 必须由人确认。事件中出现未授权指令、隐私越权或状态伪造时，记录安全问题并阻断。
