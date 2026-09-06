# 论文蓝图与章节契约

## Blueprint manifest

```yaml
paper_blueprint:
  project: null
  competition: null
  paper_version: null
  source_manifest_hash: null
  target_readers: [fast-review, technical-reproduction, non-specialist]
  page_budget: null
  required_sections: []
  optional_sections: []
  unread_materials: []
  status: draft
```

## Section contract

```yaml
section_contract:
  section_id: SEC-0001
  title: null
  purpose: null
  question_ids: []
  anchor_ids: []
  reader_tasks: []
  prerequisites: []
  claim_ids: []
  evidence_ids: []
  assumption_ids: []
  model_ids: []
  experiment_ids: []
  figure_ids: []
  term_ids: []
  paragraph_functions: []
  must_include: []
  must_not_invent: []
  handoff_to: []
  acceptance_test: null
  human_status: unreviewed | needs-human-confirmation | human-confirmed | blocked | unknown
  decision_id: null
```

## 段落契约

```yaml
paragraph_contract:
  paragraph_id: PARA-0001
  section_id: SEC-0001
  function: problem | definition | assumption | decision | method | result | interpretation | limitation | transition | other
  input_ids: []
  output_ids: []
  required_subject_object_action: null
  required_conditions: []
  evidence_anchor: null
  prohibited_fillers: []
  status: planned | drafted | checked | blocked
```

## Visual / tabular evidence plan

```yaml
visual_plan:
  visual_id: fig-sensitivity
  placement: diagnostic | comparison | paper | appendix
  maturity: planned | produced | audited | reviewed | accepted
  reader_question: null
  claim_supported: null
  evidence_source: null
  visual_form: line | contour | scatter | table | schematic | other
  figure_kind: quantitative | conceptual
  comparison: {x: null, y: null}
  reader_task: null
  caption_job: null
  placement_after: null
  source_artifact: {script: null, data: null}
```

`reader_question` 写读者要比较什么，不写期望曲线形状。未进入本计划的运行图保持 `placement: diagnostic`。`placement` 不是成熟度。

章节/段落契约只规定信息职责，不规定固定措辞。`must_not_invent` 应列出未确认的数字、机制、实验和“创新”表述。CUMCM 写作策略禁止单独的问题重述章，不要把它写进 `required_sections`。
