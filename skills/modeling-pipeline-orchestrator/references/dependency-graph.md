# 阶段依赖与返工影响

三层依赖以 [`schemas/stage-registry.json`](../../../schemas/stage-registry.json) 为准。下表是阅读索引：`execution_requires` 才阻断当前任务；`adoption_requires` 只在 adopt/freeze/submit 前生效；`recommended_after` 不阻断明确要求的探索或续写。

## 默认映射

| stage | skill | 执行前置 | 采用前置 | 软建议 | 人工边界 |
| --- | --- | --- | --- | --- | --- |
| rules_profile | modeling-rules-profile | 无 | 无 | 无 | 规则适用范围（查看即可，冻结 profile 需确认） |
| topic_selection | modeling-topic-selection | 无 | 无 | rules_profile | 正式选定主选/备选 |
| literature_evidence | modeling-literature-evidence | 无 | 无 | topic_selection | 未核验来源不得写成已采用证据 |
| problem_familiarization | modeling-problem-familiarization | 无 | topic_selection | literature_evidence、topic_selection | 把理解标为已确认 |
| problem_intake | modeling-problem-intake | 无 | topic_selection | familiarization、literature | 冻结题意解释 |
| distinctiveness_coach | modeling-distinctiveness-coach | 无 | 无 | intake、familiarization | 题目锚点是质量建议 |
| assumption_ledger | modeling-assumption-ledger | 无 | problem_intake | familiarization | 写入采用集 |
| data_audit | modeling-data-audit | 无 | 无 | problem_intake | 查看缺失是 explore；删异常/改切分才是 adopt |
| model_architect | modeling-model-architect | 无 | problem_intake | familiarization、distinctiveness、assumption、data_audit、literature | 比较候选可探索；冻结核心模型需确认 |
| experiment_validator | modeling-experiment-validator | 无 | model_architect | data_audit | 把结果写进结论前需已采用模型 |
| paper_architect | modeling-paper-architect | 无 | 无 | intake、model、experiment | 蓝图不是正文章节模板 |
| figure_design | modeling-figure-designer | 无 | 无 | paper_architect、experiment | 图表问题与制作 |
| figure_table | modeling-figure-table-auditor | 无 | 无 | experiment、figure_design | 图表事实 |
| claim_evidence | modeling-claim-evidence-audit | 无 | 无 | paper_architect、experiment | 主张强度 |
| terminology | modeling-terminology-auditor | 无 | 无 | paper_architect | 定义与符号 |
| draft | modeling-paper-writer | 无 | 无 | paper_architect、experiment、figure、claim、terminology | 有题面/分析/旧稿即可写暂定稿 |
| paper_review | modeling-paper-reviewer | draft | 无 | 无 | 是否接受问题 |
| ai_pattern | modeling-ai-pattern-reviewer | draft | 无 | 无 | 采用哪些建议 |
| anti_homogenization | modeling-anti-homogenization-auditor | draft | 无 | distinctiveness_coach | 题目特异性 |
| reader | modeling-reader-experience-auditor | draft | 无 | 无 | 是否可读 |
| naturalizer | modeling-paper-naturalizer | draft | 无 | paper_review、ai_pattern、anti_homogenization、reader | 修改边界 |
| support | modeling-support-materials-auditor | draft | 无 | figure_table | 支撑包 |
| ai_disclosure | modeling-ai-use-disclosure | 无 | rules_profile | rules_profile | 真实披露 |
| final_preflight | modeling-final-preflight | draft | ai_disclosure | 审查与支撑相关阶段 | 最终提交 |
| process_freezer | modeling-process-freezer | final_preflight | final_preflight | 无 | 冻结范围 |

## 可并行分支

选题比较通常覆盖全场题目，但已有选题或用户只要求解释时可以直接推进相关范围。文献 orientation、题目熟悉和问题地图可以按用户当前问题裁剪，不因推荐顺序而阻断探索。`model_architect` 在用户要求比较模型时只要有题面或问题描述即可探索；正式采用仍需要题意范围。paper_architect 和 modeling-paper-writer 可以先形成结构/正文草稿。并行不意味着共享文件可同时改写；共同 finding 必须按 finding-protocol 合并。

## 返工影响矩阵

| 变化源 | 至少重新路由 |
| --- | --- |
| 选题/团队资源/比赛范围 | topic_selection → literature_evidence → problem_familiarization → problem_intake → assumption/model → experiment → paper/claim |
| 背景/文献理解 | literature_evidence → problem_familiarization → problem_intake → assumption/model → experiment → paper/claim |
| 题意/对象/边界 | problem_familiarization → problem_intake → assumption → model → experiment → paper/claim |
| 假设/目标/约束 | assumption → model → experiment → claim → paper |
| 数据/清洗/切分 | data → model → experiment → figure-design → figure-audit → claim → support |
| 模型/指标/参数 | model → experiment → figure-design → figure-audit → claim → paper → review |
| 结构/术语/正文 | paper/terminology → reader → AI-pattern → naturalizer → claim |
| 图表/代码/附录 | figure-design/figure-audit/support → reader → claim → final_preflight |
| 规则/AI 使用记录 | rules_profile → ai_disclosure → support → final_preflight |

该矩阵是保守下界；具体影响以 artifact 依赖和 process-freezer manifest 为准。探索性讨论不必等整条返工链跑完，但 adopt/freeze/submit 前应核对受影响的采用前置。
