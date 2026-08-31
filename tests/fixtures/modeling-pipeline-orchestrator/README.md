# modeling-pipeline-orchestrator fixtures

这些是虚构状态文件，用于测试依赖路由，不代表真实项目状态。

- initial_state：规则 profile 已通过，题意入口和 AI 披露前置可被识别为 ready；
- multi_topic_state：规则 profile 已通过，但多题入口必须先运行 topic_selection，不能直接进入题意或模型阶段；
- blocked_state：题意解释被阻断，但不相关的披露阶段仍可独立显示为 ready；
- needs_human_state：orientation 已完成，但共同理解、正式题意和 AI 披露都待人工确认，没有任何阶段 ready；
- 三个状态均显式把已经选定的单题标为 topic_selection skipped，避免把单题入口误判为未完成的多题比较；
- invalid_state：包含未知 stage，必须拒绝生成计划。
