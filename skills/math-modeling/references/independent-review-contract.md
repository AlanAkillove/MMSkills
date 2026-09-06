# Independent review contract

独立审阅是 Subagent 模式，不是新的公开 Skill。统一隔离原则，再按 review unit 换透镜。

## 隔离

- 新上下文；只给当前 artifact / review bundle 和必要原材料。
- 不给 producer rationale、投入时间、或“准备采用/已经很好”。
- 返回 finding / evidence / why it matters / alternative / recommended action。
- 不能自己改完后宣布问题已解决。
- `reviewed` 必须带这一版 `artifact_hash`；hash 变了则审阅作废。

## Review unit

默认一个承重单元一次 Subagent，而不是每个图、每个数字各开一次。

| unit | 典型成员 | 透镜 |
|---|---|---|
| question_bundle | 一问正文、相关结果、进正文的图 | 从题目到方法、证据、图表是否闭合 |
| model_bundle | 候选模型说明 | 是否答题、最强未验证假设、替代解释、验证能否证伪 |
| assumption_bundle | 高影响假设 | 更弱替代、失败会破坏什么 |
| manuscript_bundle | 摘要/结论或全文 | 跨章术语、主线、同构结构和图表风格 |

## 透镜问题（给 Subagent 的问题集，不是总分）

**model_critic**：是否真的回答题目？最强未验证假设是什么？有没有改题？哪一环最容易失效？验证能否区分碰巧拟合？有没有更简单的替代？哪些结论现在不能声称？

**result_interpretation**：这些数值能支持多强的结论？baseline 是否公平？是否只在一个划分上成立？有没有与预期矛盾的结果？能不能写“明显提高”？

**visual_reader**：五秒内能否识别读者任务？最先被注意的元素是否正确？标签/图例是否遮挡？是否其实该用表？caption 是否承担了图自己该表达的信息？

**question_closure**：读者能否从该问的题目要求一路跟到方法、结果、验证和图表？

**manuscript**：跨章术语是否一致？各问是否同构填空？摘要是否对上正文主线？
