# 最终预检契约

## Release manifest

```yaml
release_manifest:
  release_id: REL-0001
  target_competition: null
  target_year: null
  division: null
  region: null
  rules_profile_id: null
  paper:
    path: null
    sha256: null
    format: null
    size_bytes: null
  support:
    path: null
    sha256: null
    format: null
    size_bytes: null
  source_manifests: []
  ai_trace: null
  generated_at: null
  tools: []
  overall_status: draft
  human_signoff: pending
```

## Check result

```yaml
check:
  check_id: PRE-0001
  layer: identity_and_scope | paper_structure | problem_and_model | claim_and_evidence | terminology_and_reader | experiment_and_reproduction | figures_and_support | ai_disclosure
  rule_ids: []
  artifact_ids: []
  location: null
  status: pass | fail | unknown | not_applicable | blocked
  observation: null
  evidence_anchors: []
  severity: P0 | P1 | P2 | P3
  impact: null
  owner_or_handoff: null
  acceptance_test: null
  tool_version: null
  input_hashes: []
  output_hashes: []
  human_status: unreviewed | needs-human-confirmation | human-confirmed | rejected | unknown
  decision_id: null
```

## 状态语义

- `pass`：在声明的范围、版本和工具条件下完成检查且证据支持；
- `fail`：检查到不满足项；
- `unknown`：输入/证据/版本不够；
- `not_applicable`：规则 profile 明确说明不适用；
- `blocked`：权限、安全、规则或 P0/P1 阻断；
- `ready-for-human-submission`：机械/语义检查完成，但最终提交仍需人签核。

`unknown` 不得转换成 `pass`；没有运行检查也不能写“无问题”。
