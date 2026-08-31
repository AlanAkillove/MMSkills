# rules profile 字段契约

## 来源

```yaml
source:
  source_id: SRC-0001
  title: null
  url_or_path: null
  authority: official_organizing_committee | official_region | school_notice | user_provided | publisher | community | unknown
  published_at: null
  effective_from: null
  effective_to: null
  accessed_at: null
  content_hash: null
  language: zh-CN
  completeness: complete | partial | unknown
  evidence_anchors: []
  limitations: null
```

`content_hash` 建议 SHA-256；网页更新时保留旧 hash 和访问日期，不覆盖历史证据。

## 规则

```yaml
rule:
  rule_id: RULE-0001
  category: paper | support_materials | ai | confidentiality | submission | ethics | other
  title: null
  requirement: null
  condition: null
  exceptions: []
  applies_to: [paper]
  status: confirmed | unknown | conflict | stale | not_stated
  certainty: high | medium | low
  source_ids: [SRC-0001]
  evidence_anchors:
    - locator: page 2 / Article 10
      excerpt_or_summary: null
  verification_action: null
  human_question: null
  decision_id: null
```

`requirement` 应尽量接近可检查的自然语言；`condition` 和 `exceptions` 不能被省略。`certainty` 描述证据可靠程度，`status` 描述当前适用状态，二者不能混用。

## 人工确认

```yaml
human_confirmation:
  required: true
  status: pending | confirmed
  person: null
  date: null
  scope: null
  decision_id: null
```

`verified` profile 必须有确认人、日期、范围和决定 ID；`draft/conflict/stale/blocked` profile 可以保留待确认状态，但不能被下游当作正式合规通过。

## 规则 profile 顶层状态

- `draft`：已抽取但未完成来源/适用范围确认；
- `verified`：目标范围、官方来源、有效期和人工确认均完成，且无未解决 P0/P1；
- `conflict`：存在未解决的官方/附加规则或版本冲突；
- `stale`：来源可能已过期，尚未重新核验；
- `blocked`：关键来源不可读、目标不明或存在保密/权限阻断。

## 变更记录

```text
change_id | profile_version | parent_version | field_path | before | after
source_ids | reason | effective_date | downstream_impact | human_status | decision_id
```
