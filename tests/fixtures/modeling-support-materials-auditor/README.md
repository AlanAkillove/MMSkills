# `modeling-support-materials-auditor` fixtures

这些脱敏片段测试支撑材料清单、静态安全、论文一致性、复现状态和匿名边界。

- `positive-static-manifest.md`：静态清单和 hash 完整；
- `positive-authorized-sandbox-run.md`：明确授权且隔离运行有记录；
- `negative-appendix-mismatch.md`：附录和压缩包不一致；
- `negative-unsafe-execution.md`：要求默认运行陌生脚本/宏；
- `negative-path-traversal.md`：压缩包路径穿越/异常嵌套；
- `negative-paper-support-mismatch.md`：论文代码数据图表版本冲突；
- `negative-cumcm-rule-copy.md`：规则 profile 不匹配；
- `negative-identity-leak.md`：匿名信息泄露；
- `negative-ai-disclosure-missing.md`：要求 AI 详情但文件缺失；
- `expected-behavior.md`：安全、状态、人工确认。
