# 技能目录与优先级

这是当前技能目录和优先级记录。优先级依据“对后续返工的影响 × 可跨论文复用性 × 可测试性”确定。反同质化不是最后的装饰检查，而是从题意拆解和模型选择阶段开始的横切能力。

当前进度：0.3.1 做证据约束的学术表达自然化，不改三角色架构。脱敏真实项目回放仍是 0.3 实践门。

## P0：先做最小闭环

| 候选 skill | 作用 | 关键产物 |
|---|---|---|
| `math-modeling` | 按当前意图路由到建模手/编程手/论文手 | 本轮 loaded specialists（通常不落盘） |
| `modeling-pipeline-orchestrator` | 完整赛程、恢复、full audit、提交诊断 | `pipeline_state.yaml` |
| `modeling-topic-selection` | 比较全场题目并形成主选/备选人工决策 | `topic_cards.md` + `topic_selection_brief.md` |
| `modeling-problem-familiarization` | 分轮学习题目背景、对象关系与文献边界 | `problem_background_map.md` + `understanding_checkpoint.md` |
| `modeling-problem-intake` | 把题面拆成任务、变量、目标、约束和歧义 | `question_map.md` |
| `modeling-assumption-ledger` | 登记假设、理由、影响、验证与确认状态 | `assumption_ledger.md` |
| `modeling-claim-evidence-audit` | 绑定主张、证据、边界和验证入口 | `claim_evidence_matrix.csv` |
| `modeling-paper-reviewer` | 以证据化审稿角色发现题意、模型、证据、阅读和合规问题 | `review_report.md` + `review_findings.jsonl` |
| `modeling-paper-naturalizer` | 在保留含义和证据的前提下自然化表达 | `revised_text.md` + changelog |
| `modeling-final-preflight` | 提交前汇总格式、引用、图表、身份、支撑和 AI 披露状态 | `preflight_report.md` + release manifest |

## P1：解决高频返工和论文同质化

| 候选 skill | 作用 | 关键产物 |
|---|---|---|
| `modeling-rules-profile` | 把赛事要求转为有来源、有效期和冲突状态的规则 profile | `rules_profile.yaml` + source register |
| `modeling-data-audit` | 检查数据口径、泄漏、缺失、异常和可复现性 | `data_audit.md` |
| `modeling-model-architect` | 组织基线、候选模型、通俗分项评估、理解校验、取舍和人类决策 | `model_registry.md` + candidate cards/decision brief |
| `modeling-experiment-validator` | 记录实验、比较、敏感性、不确定性和稳健性 | `experiment_registry.jsonl` + reproduction manifest |
| `modeling-figure-designer` | 从题目、证据和读者任务设计并制作论文图表、模型图和多面板图 | `figure_design_brief.md` + source/render + manifest |
| `modeling-distinctiveness-coach` | 写前保留题目特征和真实取舍，阻断强行创新 | `distinctiveness_ledger.md` |
| `modeling-terminology-auditor` | 建模阶段建立术语表，成稿后只做 drift audit | `terminology_table.md` |
| `modeling-anti-homogenization-auditor` | 审核题目特征、建模路径、证据组织和表达是否被模板抹平 | `distinctiveness_audit.md` |
| `modeling-ai-pattern-reviewer` | 识别模板化痕迹并给出证据化重写建议 | `ai_pattern_report.md` |
| `modeling-reader-experience-auditor` | 以不同读者路径检查逻辑、导航、视觉和信息负担 | `reader_audit.md` |
| `modeling-ai-use-disclosure` | 从会话/日志整理赛事适配的 AI 使用详情 PDF | `AI工具使用详情.pdf` |
| `modeling-literature-evidence` | orientation / modeling-synthesis / citation-audit：发现与核验分开，文献服务模型综合而不是模板 | `source_register.csv` + orientation/synthesis notes |
| `modeling-process-freezer` | 冻结阶段快照、hash、谱系和人工签核 | `freeze_manifest.json` + `handoff.md` |
| `modeling-tex-paper-production` | 按赛事 profile 生成、迁移、编译、渲染和审计 TeX 论文 | `main.tex` + `tex_build_manifest.yaml` + `tex_layout_audit.md` |

## P2：扩展完整工程链

- 主要数模赛事规则适配器
- 本地日志采集和脱敏工具
- Word 交付验证与 PDF 正文/附录分段计数工具

## 不建议单独做成 skill 的功能

- 单纯的同义词替换；
- 没有证据的“AI 率评分”；
- 只按词频判定作者身份；
- 与具体赛事无关的万能格式清单；
- 把所有写作问题塞进一个超长 prompt；
- 为了与他人不同而无证据地改用复杂模型或新造术语。
