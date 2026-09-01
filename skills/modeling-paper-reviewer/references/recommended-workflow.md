# 审稿角色的推荐工作流

本文件是按需读取的入口，详细透镜和字段以 [review-workflow.md](review-workflow.md) 为准。用户只要快速意见或针对某一透镜时，不要展开为全篇多透镜综合。

## 需要完整预审时的顺序

1. 固定版本/hash、范围和已读/未读材料。
2. 先读故事线，再回查题面、公式、数据和图表。
3. 各透镜独立产出后再去重；Major 数量由证据决定，不凑条数。
4. 意见只给可验证的下一步，不直接写替代段落。

## 需要落盘时的最低交付

`review_report.md`、`review_findings.jsonl`、`human_decision_queue.md`。JSONL 遵守仓库 `finding.schema.json`。
