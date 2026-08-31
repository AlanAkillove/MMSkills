# Templates

模板用于让不同会话和不同 Agent 之间传递结构化状态。模板是起点，不是替代人工判断的默认答案。

当前包含：

- `project_profile.yaml`：项目与赛事上下文；
- `rules_profile.yaml`：目标赛事规则、来源、日期和适用范围；
- `topic_cards.md`：一场比赛的全题目卡片、工作负担、团队匹配和风险；
- `topic_selection_brief.md`：多题分项比较、主选/备选讨论和人工选题门；
- `assumption_ledger.md`：假设、理由、影响、验证与确认状态；
- `problem_background_map.md`：选定题目的现实背景、对象关系、测量数据和任务语义；
- `literature_orientation_ledger.md`：背景/方法文献的思想卡片、可迁移和不可迁移边界；
- `understanding_checkpoint.md`：多轮说明、团队复述、纠正和理解确认；
- `familiarization_open_questions.md`：题目熟悉阶段的未决问题和解锁条件；
- `decision_log.md`：人类做出的关键选择；
- `claim_evidence_matrix.csv`：主张—证据—边界映射；
- `terminology_ledger.md`：术语、定义、首次出现、替换和禁用候选；
- `experiment_registry.jsonl`：实验、参数、数据版本、结果和复现入口；
- `model_candidate_cards.md`：逐候选模型的通俗用途、分项评估、代价、风险、未知和理解校验；
- `model_decision_brief.md`：候选并列比较、验证优先级和人类确认问题；
- `figure_design_brief.md`：图表问题、证据角色、选图理由、视觉系统和人工确认项；
- `figure_storyboard.md`：多面板证据角色、视觉顺序、正文承接和删留决定；
- `figure_design_manifest.yaml`：图表来源、转换、面板、导出、版本和交接状态；
- `ai_use_event.yaml`：单条 AI 使用事件的结构化记录；字段、枚举和证据等级见 `skills/modeling-ai-use-disclosure/references/event-schema.md`。
- `finding_record.json`：跨审稿/审计角色共享的 finding 起始记录；机器字段以 `schemas/finding.schema.json` 为准。
- `tex/`：中性数学建模论文 TeX 骨架、赛事 profile 示例和 XeLaTeX 构建说明。
