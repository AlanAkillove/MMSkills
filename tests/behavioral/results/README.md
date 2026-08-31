# Behavioral host results

真实宿主运行记录默认写到 `runs/`，不提交公开仓库。文件应包含 `host`、`model`、`model_version`、`run_at`、`status` 和 validator 问题；`not_run` 与 `error` 不能改写成 pass。

这些结果不等于 compatibility matrix 已验证。矩阵在没有稳定的脱敏真实运行前保持 `fixture_only`。
