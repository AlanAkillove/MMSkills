# 阶段依赖与返工影响

## 默认映射

| stage | skill | 必要前置 | 典型输出 | 人工门 |
| --- | --- | --- | --- | --- |
| rules_profile | modeling-rules-profile | 项目/赛事范围 | rules profile | 规则适用范围 |
| topic_selection | modeling-topic-selection | rules_profile | topic cards + comparison + selection brief | 主选/备选题目和比较依据 |
| literature_evidence | modeling-literature-evidence | topic_selection（orientation 模式）或 problem_intake（citation-audit 模式） | source register + orientation ledger（orientation 模式） | 来源阅读与迁移边界 |
| problem_familiarization | modeling-problem-familiarization | literature_evidence、topic_selection | background map + understanding checkpoint | 共同理解和未决边界 |
| problem_intake | modeling-problem-intake | problem_familiarization、topic_selection（单题须显式 skipped） | question map | 正式题意/问题分析 |
| assumption_ledger | modeling-assumption-ledger | problem_intake、problem_familiarization | assumption ledger | 关键假设 |
| data_audit | modeling-data-audit | problem_intake、problem_familiarization、数据入口 | data audit | 清洗/切分/授权 |
| model_architect | modeling-model-architect | problem_intake、problem_familiarization、assumption、data（适用时，须显式 skipped） | model registry + candidate cards/decision brief + understanding check | 模型/目标/约束、用户解释与人工决策支持 |
| experiment_validator | modeling-experiment-validator | model、data（适用时） | experiment registry | 实验与结论充分性 |
| paper_architect | modeling-paper-architect | question、model、experiment | paper blueprint | 结构与主张 |
| figure_design | modeling-figure-designer | paper/model/experiment/claim plan | design brief + source/render | 图表问题、图型、视觉系统和制作 |
| figure_table | modeling-figure-table-auditor | data/model/experiment/figure_design | figure registry | 图表事实 |
| claim_evidence | modeling-claim-evidence-audit | paper、model、experiment、sources | claim matrix | 主张强度 |
| terminology | modeling-terminology-auditor | question/model/paper | term ledger | 定义与符号 |
| draft | author/agent writing | paper_architect + relevant evidence | manuscript | 核心正文 |
| paper_review | modeling-paper-reviewer | draft + upstream artifacts | review report | 是否接受问题 |
| ai_pattern | modeling-ai-pattern-reviewer | draft | pattern report | 采用哪些建议 |
| anti_homogenization | modeling-anti-homogenization-auditor | draft + distinctiveness | distinctiveness audit | 题目特异性 |
| reader | modeling-reader-experience-auditor | rendered draft | reader audit | 是否可读 |
| naturalizer | modeling-paper-naturalizer | accepted review + locked ledgers | revised text/changelog | 修改边界 |
| support | modeling-support-materials-auditor | code/data/appendix + paper | support manifest | 支撑包 |
| ai_disclosure | modeling-ai-use-disclosure | authorized history + rules | disclosure PDF | 真实披露 |
| final_preflight | modeling-final-preflight | all relevant audits | release report | 最终提交 |
| process_freezer | modeling-process-freezer | final/preflight or checkpoint | snapshot/handoff | 冻结范围 |

## 可并行分支

选题比较必须先覆盖全场题目。选题后先以 orientation 模式建立背景/方法学习账本，再由题目熟悉 skill 组织多轮讲解与理解确认；理解确认后才运行正式 problem_intake，形成问题地图。之后 assumption_ledger 与 data_audit 在各自输入完整时可并行；figure_design 在 paper blueprint、模型和实验结果可用后运行，figure_table 在设计和证据输入形成后运行；claim_evidence、terminology 可与图表分支并行；paper_review 后的 ai_pattern、anti_homogenization、reader 可分别运行，再由作者决定自然化范围。并行不意味着共享文件可同时改写。

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
