# 长题面与跨会话续接

当题面、附件或历史会话过长时，目标是保留可复核的结构，不是生成越来越短但失去来源的摘要。

## 分块原则

- 优先按题面章节、子问题、表格和图示边界分块；不要在一个关系或公式中间截断。
- 每块记录 `chunk_id`、原材料路径、页码/段落范围、首尾锚点和已读取附件。
- 先抽取证据，再写局部总结；总结中的每条关键事实都回指 `evidence_id`。
- 同一概念跨块出现时沿用 ID，不要因换块重命名造成术语漂移。

## 每块完成后的 checkpoint

```yaml
chunk_checkpoint:
  chunk_id: Q-03
  source_range: "page 2, subsection B"
  source_manifest_hash: null
  first_anchor: null
  last_anchor: null
  evidence_ids: [T-08, FIG-02-LABEL]
  processed_items: []
  confirmed_facts:
    - text: "..."
      evidence_ids: [T-08]
      status: direct
  candidate_inferences:
    - text: "..."
      evidence_ids: [T-08]
      status: inferred
      alternatives: ["..."]
  unresolved_ambiguities:
    - text: "..."
      evidence_ids: [FIG-02-LABEL]
      status: unknown
      alternatives: ["..."]
  entities_added: []
  relations_added: []
  subquestions_affected: []
  next_chunk: Q-04
  human_confirmation_needed: true
```

这里的 `confirmed_facts` 指“已被原材料直接支持的事实”，不等于 Research Chair 的最终人工确认；人工确认仍须记录在 `question_map.md` 的人工确认表。不要用 `confirmed_facts` 存放未经来源支持的推断；如果来源范围不完整，状态应为 `partial` 或 `blocked`。

## 恢复顺序

1. 读取总交接块和最近 checkpoint；
2. 检查输入文件版本/hash 是否变化；
3. 重新打开最后一个锚点附近的原文，而不是只相信摘要；
4. 检查已有实体、关系和术语 ID，防止重复或改名；
5. 从 `next_chunk` 继续，并在结束时追加 checkpoint；
6. 若无法恢复来源，保留已有证据但将受影响字段降为 `unknown`，不要补写。

## 什么时候停止

出现以下任一情况就停止继续推断并交给人工：

- 同一关系有两个无法排除的解释；
- 图示/附件缺失且会改变模型边界；
- 题目动词和输出形式无法确定；
- 版本变化导致已有锚点失效；
- 上下文不足以区分原文、摘要和模型建议。
