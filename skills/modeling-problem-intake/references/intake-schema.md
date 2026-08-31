# 题意解析字段契约

本文件是 `modeling-problem-intake` 的详细字段说明。只在需要建立或审查 `question_map.md` 时读取；不要把整份字段说明原样输出给最终论文读者。

## 证据状态

| 状态 | 含义 | 允许的表述 |
|---|---|---|
| `direct` | 题面文字、表格、公式或明确图注直接给出 | “题面明确说明……” |
| `visual` | 图上可直接观察的标签、线段、节点、箭头或相对布局 | “图中可见……；尚不能据此推出……” |
| `inferred` | 由一个或多个证据推断出的解释 | 必须列依据、替代解释和置信度 |
| `unknown` | 材料不足、未定义或无法确认 | 明确写“当前无法确定” |
| `conflict` | 不同材料、段落或图文之间不一致 | 并列记录来源，不擅自裁决 |
| `external` | 外部资料提供的背景或定义 | 不得覆盖题面；注明来源和适用范围 |

公共质量模型中的 `direct/inferred/unknown/external` 与本表兼容；`visual` 和 `conflict` 是题意解析为图示和冲突增加的细分状态。

## `question_map.md` 推荐结构

```markdown
# Question Map

## 0. Intake status
- status: draft | human-confirmed | blocked
- source_manifest: ...
- read_scope: ...
- missing_materials: ...

## 1. Neutral restatement
...

## 2. Evidence ledger
| evidence_id | location | excerpt_or_observation | status | polarity/quantifier/time/condition | modeling_impact | notes |

## 3. Entities and states
| entity_id | name_as_given | role | index/time/space | observable/state | evidence_ids |

## 4. Relations and structure
| relation_id | subject | relation | object | direction/condition | status | evidence_ids | alternatives |

## 5. Subquestion map
| question_id | task verb | object | input | expected output | explicit constraints/quantifiers | time scope | dependencies | evidence_ids |

## 6. Variables and parameters (candidate)
| symbol_candidate | meaning | type/unit/domain | index/time/space scope | observed or derived | source | confirmation |

## 7. Objectives and constraints (candidate)
| item_id | kind | statement | evidence_ids | status | scope | confirmation |

`kind` 至少区分 `requested_output`、`objective_candidate`、`constraint_candidate` 和 `evaluation_metric`。没有题面依据的候选项仍须保留为 `candidate`/`unknown`，不得伪装成 `direct`。

该表中的 `status: candidate` 表示“团队或 Agent 提出的待确认建模解释”，不是题面证据等级；只有在有人确认并有相应记录后，才可作为下游模型输入。`evidence_ids` 仍必须指向提出该候选的题面依据或明确说明缺口。

## 8. Boundary and counterexample checklist
...

## 9. Ambiguity/conflict queue
| issue_id | statement | alternatives | consequence | discriminating evidence | owner | status |

## 10. Problem-specific anchors
...

## 11. Human confirmation
...

## 12. Handoff
...
```

## 最小记录要求

- 每个主对象、关系、子问题、变量、参数、输出、目标候选、约束候选和评价指标至少有一个 `evidence_id`，或明确标为 `unknown`/`candidate` 并说明缺口；没有证据就不能留空后默认当作事实。
- 变量符号可以暂用 `x_candidate` 等占位符，避免在题意阶段过早引入带有模型含义的符号。
- “目标”与“约束”必须分别记录；若题面只说“分析影响”，不得直接写成最大化/最小化问题。
- 对题面中的单位和量纲保留原样，同时记录可能的换算需求；没有依据时不换算。
- 图示关系至少说明是文字明确、图中可见、推断还是未知；不要以“如图所示”替代实际关系说明。
- `status: human-confirmed` 只能在确认人、日期、确认范围和对应决策记录都留下后使用；“看起来合理”不构成确认。

## 人工确认记录

```markdown
| decision_id | confirmer | date | confirmed_scope | decision | evidence_ids | follow_up |
```

确认范围必须能落到对象、关系、子问题、目标/约束或边界等具体字段；只确认“整体没问题”不能升级所有字段的状态。

## 交接摘要

长题面或上下文压缩时，保留以下最小摘要：

```yaml
chunk_checkpoint:
  chunk_id: null
  source_range: null
  source_manifest_hash: null
  first_anchor: null
  last_anchor: null
  last_evidence_id: null
  processed_items: []
  confirmed_facts:
    - text: null
      evidence_ids: []
      status: direct
  candidate_inferences:
    - text: null
      evidence_ids: []
      status: inferred
      alternatives: []
  unresolved_ambiguities:
    - text: null
      evidence_ids: []
      status: unknown
      alternatives: []
  next_chunk: null
  forbidden_inferences: []
```

`source_manifest_hash` 不可得时写 `unknown`，不能编造 hash。

`last_evidence_id` 只是定位游标，不能作为事实来源的唯一记录；事实、推断和歧义必须在对应列表项中携带自己的 `evidence_ids`。
