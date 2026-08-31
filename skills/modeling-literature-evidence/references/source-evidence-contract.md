# 来源与证据契约

## 来源记录

`source_register.csv` 每行一个来源，建议字段：

| 字段 | 说明 |
| --- | --- |
| `source_id` | 稳定 ID，不能因引用格式修改而变化 |
| `source_type` | `official_rule`、`official_statistic`、`dataset_doc`、`primary_study`、`method_paper`、`benchmark`、`review`、`software_doc`、`background`、`secondary` |
| `bibliographic_identity` | 作者/机构、标题、年份、期刊/会议、版本等可核验身份 |
| `locator` | DOI、官方 URL、文件路径或数据集标识；不能只写搜索结果 URL |
| `authority` | `official`、`primary`、`peer_reviewed`、`maintainer`、`secondary`、`unknown` |
| `publication_status` | `published`、`preprint`、`official_notice`、`dataset_release`、`archived`、`unknown` |
| `version` | 版本/发布日期/生效日期；未知写 `unknown` |
| `accessed_at` | 实际打开/读取日期 |
| `content_hash` | 可行时记录内容 hash；网页变化时至少保留快照说明 |
| `read_status` | `candidate`、`opened`、`read_relevant_part`、`verified`、`summary_only`、`unavailable`、`conflict` |
| `evidence_locator` | 页码、章节、表/公式/段落或稳定锚点 |
| `evidence_summary` | 对当前问题的最小事实摘要，不冒充逐字引文 |
| `scope_and_limits` | 样本、地区、时间、方法假设、不能外推之处 |
| `human_verified` | `yes`、`no`、`pending` |
| `notes` | 排除理由、冲突、许可和隐私说明 |

## 主张—来源关系

`citation_evidence_matrix.csv` 每行一个原子关系：

```text
claim_id,source_id,relation,evidence_locator,source_says,source_does_not_say,
scope_match,citation_location,citation_status,human_verified,conflict_id,notes
```

`relation` 使用：

- `direct_support`：来源在其自身范围内直接支持主张；
- `context_only`：只提供背景或定义，不支持主张的数值/因果结论；
- `method_precedent`：说明某方法曾被使用，不证明本题一定适用；
- `dataset_provenance`：说明数据来源/口径，不证明分析结论；
- `contradicts`：来源与主张冲突，需要处理；
- `no_support`：已读取但不能支持，不能留作装饰引用；
- `unknown`：未能读到或定位不足。

## 证据等级

- `E3`：打开了原始来源并有稳定定位，内容和范围可核对；
- `E2`：可信发布者的可访问摘要/版本记录，支持有限字段；
- `E1`：二手引用、论文成品或间接线索，只能提示核查方向；
- `E0`：模型记忆、搜索摘要、用户口述或未经核实的候选。

只有 E3 才适合直接支撑关键事实；E2–E0 必须保留限制和人工确认状态。
