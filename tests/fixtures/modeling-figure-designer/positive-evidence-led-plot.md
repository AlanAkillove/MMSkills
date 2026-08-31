# 正例：证据驱动的方案比较图

```yaml
figure_design:
  figure_id: FIG-07
  status: handed_off
  mode: plot
  figure_question: 在相同潮汐窗口和容量约束下，方案 B 相比基线 A 的等待时间变化是否稳定？
  reader_task: compare
  evidence_role: comparative
  claim_ids: [CLM-12]
  evidence_ids: [EVD-31, EVD-32]
  experiment_ids: [EXP-07]
  source_data_ids: [DATA-04]
  source_code_entry: plot/waiting_time_comparison.py
  input_manifest_hash: sha256:input-example
  transformations: [按方案分组, 保留重复实验点, 统一为分钟]
  chart_type: interval_dot_plot
  rejected_chart_types: [pie, 3d_bar]
  visual_system:
    target_physical_size: 0.85\textwidth x 6.2 cm
    palette_semantics: {baseline: neutral, candidate: focus}
    non_color_channels: [点形, 直接标签]
  export_formats: [svg, pdf, png]
  output_hashes: {svg: sha256:output-example}
  page_render_checked: true
  human_decision_id: DEC-19
  human_status: confirmed
```

图注解释区间含义和当前参数范围；正文引用 `FIG-07` 并限定比较边界。源文件包含 SVG，随后交给图表审计核对数字和单位。
