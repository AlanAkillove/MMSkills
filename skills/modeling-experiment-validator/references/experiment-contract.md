# 实验注册契约

## 实验条目

```yaml
experiment:
  experiment_id: EXP-0001
  experiment_family: EXP-FAM-0001
  type: baseline_comparison | holdout_or_cross_validation | feasibility_or_constraint | sensitivity | robustness | ablation | uncertainty_or_repetition | edge_case | reproduction
  question: null
  claim_ids: []
  risk_ids: []
  model_ids: []
  baseline_ids: []
  data_ids: []
  code_entry: null
  environment: null
  version_hash: null
  split_protocol: null
  parameters: {}
  random_seed: null
  repetitions: null
  metric_definition: null
  units: null
  planned_outputs: []
  output_files: []
  output_hashes: []
  result_status: planned
  failure_or_limit: null
  uncertainty: null
  interpretation: null
  supported_scope: null
  validation_status: unverified
  human_status: unreviewed
  decision_id: null
```

## 结果状态

- `planned`：已登记问题和设置，未运行；
- `running`：正在执行；
- `success`：按设置完成并输出可读取结果；
- `partial`：部分输出或部分重复完成；
- `failed`：运行失败、不可行、超时或数值不稳定；
- `not_run`：因资源/权限/人工决定未运行；
- `conflict`：输入、日志、论文或输出版本不一致。

`validation_status=verified` 只表示在已声明范围内设置、输出、代码/数据版本和主张映射通过核对，不表示模型正确、普适或最优。

## 结果与解释分离

结果字段写原始观测、指标、误差、区间和输出定位；解释字段写对主张的支持范围、替代解释、局限和需要人工决定的内容。不可由结果直接推出的机制、因果和最优性不能写入解释。
