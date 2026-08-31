# 人工门、冲突和交接

## 必停门

编排器至少在以下节点把任务置为 needs_human：

1. 题面对象和子问题解释；
2. 关键假设、目标函数、约束、指标；
3. 数据清洗、异常处理、样本切分、外部来源采纳；
4. 模型候选取舍和实验设计；
5. 题目特异性/差异化路径；
6. 主要主张、结果解释、结论和局限；
7. 审稿意见是否采纳以及自然化修改范围；
8. AI 使用详情的真实程度、隐私、规则分类和最终签核；
9. 最终预检、身份信息隔离、提交文件和 release snapshot。

用户未回复、agent 自述“应该没问题”或文件存在，均不能替代确认。

## 冲突合并

多个 reviewer 或专项 skill 发现同一底层问题时，保留原始 finding ID、合并后的 issue ID、支持证据、不同解释和作者决定。不要为了减少问题数量而丢弃冲突；不要将互盲 reviewer 的报告在其独立冻结前互相暴露。

## 续接格式

每个 handoff 至少写：

~~~
Current stage:
Snapshot:
Passed:
Needs human:
Blocked/stale:
Evidence to open:
Next action:
Do not:
Acceptance condition:
~~~

handoff 只传递最小必要上下文；原文和原始数据仍在 artifact 路径中。下一 agent 先验证 snapshot/hash 和 scope，再继续任务。

## 失败策略

- 入口不明：输出两个候选及最小共同前置，不替用户选；
- 依赖缺失：标 blocked，列出具体 artifact 和解锁动作；
- 上游变更：标 stale，按影响矩阵回归；
- 规则冲突：停止合规结论，等待目标赛事官方解释；
- 权限/隐私问题：停止读取越权材料，报告 blocked/privacy；
- 上下文截断：不重构“记忆中的论文”，先从冻结材料重建索引。
