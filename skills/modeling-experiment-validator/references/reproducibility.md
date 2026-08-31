# 复现与输出核对

## 复现 manifest

```yaml
reproduction:
  paper_version: null
  code_version_hash: null
  data_hashes: []
  environment: null
  dependencies: []
  command: null
  working_directory: null
  seed: null
  expected_outputs: []
  actual_outputs: []
  output_hashes: []
  run_at: null
  run_status: success | partial | failed | not_run | unknown
  mismatch: null
```

## 核对顺序

1. 代码入口和依赖是否存在；
2. 输入数据/配置/模型版本是否与论文和图表一致；
3. 命令、随机种子、资源和切分是否记录；
4. 论文数字/单位/图表是否能由输出定位；
5. 重跑差异是随机、环境、版本还是论文错误；
6. 所有失败和不一致是否进入 audit，而不是只保留成功日志。

无法运行时可做静态检查，但状态为 `not_run/unknown`；不能以“代码看起来能跑”标为 verified。
