# Templates

模板用于让不同会话和不同 Agent 之间传递结构化状态。模板是起点，不是替代人工判断的默认答案。

当前包含：

- `project_profile.yaml`：项目与赛事上下文；
- `rules_profile.yaml`：目标赛事规则、来源、日期和适用范围；
- `assumption_ledger.md`：假设、理由、影响、验证与确认状态；
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
