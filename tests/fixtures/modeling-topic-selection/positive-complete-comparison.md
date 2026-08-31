# 正例：全量题目分项比较

题目 A、B、C 均已读取完整题面和附件，并分别建立 `topic_id` 与 `statement_snapshot_id`。每题卡片记录对象、子问、输入输出、背景学习负担、数据风险、验证入口和未知项。

比较表按 `problem_comprehension`、`background_load`、`data_readiness`、`validation_feasibility`、`team_fit` 和 `time_compute_cost` 分开记录，所有判断带有 `evidence_ids` 或 `unknown`。没有综合分数。

简报提出题目 B 作为主选候选、题目 A 作为备选，并记录最早核验任务、切换条件和待团队确认的 `decision_id`。尚未冻结模型或目标函数。
