# 术语账本字段契约

## 推荐结构

```markdown
# Terminology Ledger

## 0. Scope
- status: draft | needs-human-confirmation | human-confirmed | blocked
- paper/project version: ...
- source_manifest/hash: ...
- unread_materials: ...

## 1. Concept register
| concept_id | canonical_term | language | definition | source/evidence_ids | term_status | first_definition | occurrences | related_symbol | unit | scope |

## 2. Variants and conflicts
| variant | concept_id | location | relation | allowed_scope | action | notes |

## 3. Symbol/unit register
| symbol | concept_id | meaning | type/domain | unit/dimension | locations | conflict |

## 4. High-commitment terms
| term | claim_or_concept | promised_property | required_evidence | evidence_ids | verdict | action |

## 5. Human decisions
| decision_id | confirmer | date | confirmed_scope | decision | evidence_ids | follow_up |

## 6. Handoff
...
```

## 字段规则

- `concept_id` 是稳定概念身份；术语变更不应导致概念重编号；
- `canonical_term` 是当前建议规范名，不等于人类已确认；`term_status` 至少使用 `standard`、`project-defined`、`candidate`、`alias`、`deprecated`、`unknown`、`conflict`；
- `definition` 要说明对象、范围和必要条件，不能只写一个同义词；
- `source/evidence_ids` 指向题面、标准/文献、数据字典、模型、代码、图表或人工决定；没有依据就写 `unknown`；
- `allowed_scope` 用来说明别名只在某语言、历史版本、代码接口或不同层级中可用；
- `unit/dimension` 未知时明确写未知，不得从词语或图形外观猜测；
- `first_definition` 和 `occurrences` 应能定位页码/段落/代码/图表；只给“全文”不足以复核；
- 同一概念可以有一个规范名和有限别名，但不能用“每段换一个词”制造表达变化。

## 新术语的最低审查表

```text
term_candidate:
  unique_referent: yes | no | unknown
  standard_term_checked: yes | no | unknown
  operational_definition: yes | no | unknown
  technical_function: yes | no | unknown
  reuse_value: yes | no | unknown
  evidence_or_human_decision: yes | no | unknown
  keep_status: candidate | keep | replace | blocked
```

任何一项为 `no` 的普通命名优先回退标准表达；高承诺词还要通过 [term-decision-rubric.md](term-decision-rubric.md)。
