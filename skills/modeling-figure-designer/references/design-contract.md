# 图表设计契约

设计契约回答“这张图为什么存在、读者要看什么、它如何由证据生成”。它是设计阶段的输入/输出接口；完成后应合并到共享的 `figure_table_registry.md`，再由图表审计技能独立核对事实。

## 最小字段

```yaml
figure_design:
  figure_id: FIG-0001
  status: brief | planned | rendering | needs_human_confirmation | handed_off | superseded
  mode: brief | plot | redesign | assemble | diagram | handoff
  title: null
  figure_question: null
  reader_task: compare | locate_trend | inspect_distribution | inspect_relationship | inspect_boundary | follow_process | verify_result | other
  evidence_role: descriptive | comparative | trend | relationship | distribution | sensitivity | feasibility | process | schematic | result_table
  placement: diagnostic | comparison | paper | appendix
  used_in_manuscript: false
  question_ids: []
  claim_ids: []
  evidence_ids: []
  experiment_ids: []
  model_ids: []
  paper_location: null
  source_data_ids: []
  source_code_entry: null
  input_manifest_hash: null
  transformations: []
  chart_type: null
  rejected_chart_types: []
  panel_plan:
    - panel_id: A
      role: null
      input_ids: []
      encoding: null
      reader_observation: null
      caption_link: null
  visual_system:
    target_physical_size: null
    aspect_ratio: null
    palette_semantics: {}
    non_color_channels: []
    typography: null
    grid_and_axes: null
  annotations: []
  export_formats: [svg, pdf, png]
  source_files: []
  render_files: []
  output_hashes: {}
  page_render_checked: false
  unresolved_items: []
  human_decision_id: null
  human_status: unreviewed | needs-confirmation | confirmed | rejected | unknown
```

## 设计检查

- `figure_question` 必须是读者问题，不写成“展示结果”或“美化页面”；
- `evidence_role`、`chart_type` 和每个面板的 `role` 必须互相匹配；
- `claim_ids` 只登记已有主张，不在设计过程中凭空生成结论；
- `transformations` 记录筛选、聚合、排序、归一化、单位转换和舍入；
- `palette_semantics` 说明颜色代表什么，不能把颜色名当作语义；
- `page_render_checked: false` 时，页面可读性只能记为 `unassessed`；
- `human_status: confirmed` 必须能回到 `decision_log.md` 的 `human_decision_id`。

## 与图表审计的交接

设计者交给 `modeling-figure-table-auditor` 的最小包为：

```text
figure_id + input_manifest_hash + output_hashes
figure_question + evidence_role + claim_ids/evidence_ids/experiment_ids
source_data_ids + source_code_entry + transformations
panel_plan + target_physical_size + page_render_checked
unresolved_items + human_decision_id
```

设计完成不代表数据正确、主张成立或页面通过。审计报告中的 `data_mismatch`、`unsupported_claim`、`missing_source` 和 `readability` 必须分别处理，不能只改样式后标记通过。
