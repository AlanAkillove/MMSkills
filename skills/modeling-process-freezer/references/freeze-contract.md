# 快照冻结契约

## Manifest 最小结构

~~~
{
  "schema_version": "0.1",
  "snapshot_id": "SNAP-...",
  "parent_snapshot_id": null,
  "project_root": "...",
  "state": "working",
  "purpose": "context_checkpoint | human_gate | revision_baseline | release_candidate",
  "created_at": "...",
  "rules_profile": {"profile_id": "...", "content_hash": "...", "status": "verified"},
  "files": [],
  "artifact_status": [],
  "decision_ids": [],
  "claim_ids": [],
  "open_issue_ids": [],
  "human_confirmation": {"status": "pending"}
}
~~~

上例的字段是接口示意；实际值必须来自项目。project_root 可在内部记录，但 handoff/公开报告尽量使用相对路径和脱敏 ID。

## 文件条目

每个 files[] 条目至少有：

~~~
path, kind, bytes, sha256, status, sensitivity, source_or_generator, last_checked_at
~~~

path 必须是项目根目录内的相对 POSIX 路径，禁止盘符、UNC 路径和 ..；status 使用 present、missing、changed、unreadable、excluded。临时渲染图可以在审计记录中出现，但不应被误标为 release artifact。

## 关联字段

- artifact_status：artifact ID、路径、用途、当前状态、上游依赖、下游消费者、是否需回归；
- decision_ids：题意/假设/模型/数据/实验/结论/披露的人工决定；
- claim_ids：受本快照保护的主张和证据矩阵版本；
- open_issue_ids：阻断、待确认、可延后问题；
- invalidated_by：该快照因哪些文件/规则/决定变化而失效；
- human_confirmation：人、角色、日期、决定 ID、范围、状态和备注。

## 状态不等价

有 manifest 不等于冻结；hash 稳定不等于数学正确；人工签核不等于赛事合规；released 不等于已经上传。状态只能表达当前流程证据，不能扩大成质量保证或提交授权。
