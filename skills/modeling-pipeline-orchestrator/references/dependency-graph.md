# 阶段依赖与返工影响

## 默认映射

| stage | skill | 硬前置 | 软建议/典型输出 | 人工边界 |
| --- | --- | --- | --- | --- |
| rules_profile | modeling-rules-profile | 项目/赛事范围 | rules profile | 规则适用范围 |
| topic_selection | modeling-topic-selection | 无（规则核验为推荐前置） | `recommended_after: rules_profile`；topic cards + comparison + selection brief | 主选/备选题目和比较依据 |
| literature_evidence | modeling-literature-evidence | topic_selection（orientation 模式）或 problem_intake（citation-audit 模式） | source register + orientation ledger（orientation 模式） | 来源阅读与迁移边界 |
| problem_familiarization | modeling-problem-familiarization | literature_evidence、topic_selection | background map + understanding checkpoint | 共同理解和未决边界 |
| problem_intake | modeling-problem-intake | problem_familiarization、topic_selection（单题须显式 skipped） | question map | 正式题意/问题分析 |
| distinctiveness_coach | modeling-distinctiveness-coach | problem_intake、problem_familiarization | distinctiveness ledger | 题目锚点和差异化路径 |
| assumption_ledger | modeling-assumption-ledger | problem_intake、problem_familiarization | assumption ledger | 关键假设 |
| data_audit | modeling-data-audit | problem_intake、problem_familiarization、数据入口 | data audit | 清洗/切分/授权 |
| model_architect | modeling-model-architect | problem_intake、problem_familiarization、distinctiveness_coach、assumption、data（适用时，须显式 skipped） | model registry + candidate cards/decision brief + understanding check | 模型/目标/约束、用户解释与人工决策支持 |
| experiment_validator | modeling-experiment-validator | model、data（适用时） | experiment registry | 实验与结论充分性 |
| paper_architect | modeling-paper-architect | question、model、experiment | paper blueprint | 结构与主张 |
| figure_design | modeling-figure-designer | paper/model/experiment/claim plan | design brief + source/render | 图表问题、图型、视觉系统和制作 |
| figure_table | modeling-figure-table-auditor | data/model/experiment/figure_design | figure registry | 图表事实 |
| claim_evidence | modeling-claim-evidence-audit | paper、model、experiment、sources | claim matrix | 主张强度 |
| terminology | modeling-terminology-auditor | question/model/paper | term ledger | 定义与符号 |
| draft | modeling-paper-writer | 无（需由 skill 自行标记材料缺口） | `recommended_after: paper_architect, experiment_validator, figure_design, figure_table, claim_evidence, terminology`；clean manuscript | 有题面/分析/旧稿即可形成暂定稿，最终采用仍由人确认 |
| paper_review | modeling-paper-reviewer | draft + upstream artifacts | review report | 是否接受问题 |
| ai_pattern | modeling-ai-pattern-reviewer | draft | pattern report | 采用哪些建议 |
| anti_homogenization | modeling-anti-homogenization-auditor | draft + distinctiveness | distinctiveness audit | 题目特异性 |
| reader | modeling-reader-experience-auditor | rendered draft | reader audit | 是否可读 |
| naturalizer | modeling-paper-naturalizer | draft | `recommended_after: paper_review, ai_pattern, anti_homogenization, reader`；revised text/changelog | 修改边界 |
| support | modeling-support-materials-auditor | draft | `recommended_after: figure_table`；support manifest | 支撑包 |
| ai_disclosure | modeling-ai-use-disclosure | authorized history + rules | disclosure PDF | 真实披露 |
| final_preflight | modeling-final-preflight | all relevant audits | release report | 最终提交 |
| process_freezer | modeling-process-freezer | final/preflight or checkpoint | snapshot/handoff | 冻结范围 |

## 可并行分支

选题比较通常覆盖全场题目，但已有选题或用户只要求解释时可以直接推进相关范围。选题后可用 orientation 模式建立背景/方法学习账本，再由题目熟悉 skill 组织多轮讲解与理解确认；理解确认后再采用正式 problem_intake 结果。问题地图之后可运行 distinctiveness_coach 保存题目锚点，再由 assumption_ledger 与 data_audit 在各自输入完整时并行；model_architect 读取可用的差异化信息后形成候选模型。paper_architect 和 modeling-paper-writer 可以先形成结构/正文草稿，figure、claim、terminology、reader 和 AI pattern 等审查按用户目标和风险安排。并行不意味着共享文件可同时改写；共同 finding 必须按 finding-protocol 合并。

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

该矩阵是保守下界；具体影响以 artifact 依赖和 process-freezer manifest 为准。
