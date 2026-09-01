# 运行档位

运行档位只压缩过程材料、审查透镜和协作强度，不取消题意、假设、模型、实验、结论、AI 披露和最终提交的 `core_decision` 人类决策门，也不把“更快”解释为“少做证据核验”。`review_checkpoint`（如 terminology、figure audit）可以由档位延后：Agent 可以继续，但最终采用前仍须人核对。用户没有指定档位时默认使用 `contest-standard`；需要完整复盘时再显式选择 `research-full`。编排器读取 YAML 和 `user_intent` 后生成 `effective_stage_policy`；canonical 硬依赖图不会被档位改写。

| profile | 默认协作强度 | 适用场景 | 主要压缩方式 |
| --- | --- | --- | --- |
| `research-full` | full | 有充足时间、需要完整研究记录或赛后复盘 | 各阶段独立产物、全部审查透镜、逐事件日志 |
| `contest-standard` | standard | 常规比赛周期，也是未指定档位时的平衡默认 | 共享状态优先、合并可复用检查表、按风险选择深度审查 |
| `contest-fast` | light | 时间紧或只需快速形成可审查初稿 | 一个续接包承载中间摘要、每类审查保留必要证据链、只压缩低风险文档颗粒度 |

三个档位都必须保留：全题目选题范围、背景/文献学习与理解确认、问题地图、关键假设、候选模型与人类取舍、数据/实验证据、主张边界、题目特异性、最终规则/格式检查、AI 使用真实记录和最终人类冻结。若压缩后无法追溯到原材料，应回退到更完整档位。
用户可感知的工作强度是 `working_depth = light | standard | full`；`collaboration_mode` 是兼容别名（`adaptive` 采用 profile 默认）。这些覆盖都不改变 `execution_requires`，也不取消核心采用门。
