# modeling-pipeline-orchestrator fixtures

这些是虚构状态文件，用于测试依赖路由，不代表真实项目状态。

- initial_state：规则 profile 已通过，题意入口和 AI 披露前置可被识别为 ready；
- blocked_state：题意解释被阻断，但不相关的披露阶段仍可独立显示为 ready；
- needs_human_state：题意和 AI 披露都待人工确认，没有任何阶段 ready；
- invalid_state：包含未知 stage，必须拒绝生成计划。
