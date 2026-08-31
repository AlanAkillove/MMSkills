# 运行档位与编排边界

运行档位用于在不同时间预算下安排产物和审查，不用于降低正确性标准。团队必须先确认 `run_profile`，Agent 只能根据剩余时间、材料完整度和交付目标提出候选。

## 档位选择

- `research-full`：每个阶段保留独立报告、账本、事件和 checkpoint；适合需要完整复盘、长论文或多轮研究的项目。
- `contest-standard`：保留核心账本和人工门，将低风险过程材料合并进共享续接包；赛后仍能回到来源和版本。
- `contest-fast`：只压缩低风险文档颗粒度，并选取高风险审查透镜；不能删除核心证据、失败验证、未决事项、AI 使用事实或人类决定。

## 不可压缩项

以下内容在所有档位都必须有稳定 ID、来源/版本锚点和人工状态：全题目比较、背景/文献学习、题意理解、问题地图、关键假设、候选模型与取舍、数据口径、实验与失败结果、主张边界、题目特异性、规则/格式检查、AI 使用事件和最终冻结。

## 档位如何进入路由

编排器读取 YAML 后构造：

`canonical graph + run profile = effective_stage_policy`

canonical `depends_on` 不变。档位只决定：

- 哪些审查透镜是 `selected`、`skipped-with-policy` 或 `not_selected`；
- 产物写成完整阶段文件还是 compact projection；
- 哪些 `review_checkpoint` 保持阻断，哪些延后到最终采用前再核对。

`core_decision` 不能被档位取消。`contest-fast` 的 `max_post_draft_lenses: 2` 会保留一个实质性透镜和一个读者/合规透镜；未被选中的条件透镜按 `skipped-with-policy` 满足下游依赖，但不能声称这些风险已经审查通过。

标准档可以根据已开放的 P0/P1 和人工确认范围选择 post-draft lens，但要在 `run_profile.yaml` 记录未运行的透镜及理由。快速档至少运行一个实质性高风险透镜和一个读者/合规透镜；`ai-pattern` 与 `anti-homogenization` 可以条件触发，但不能仅因时间紧而声称没有模板化或同质化风险。

如共享状态被压缩为一个 handoff bundle，bundle 必须包含各原始产物路径、hash、finding ID、decision ID 和未评估范围。任何无法回到原材料的摘要只能标为 `partial` 或 `unknown`。
