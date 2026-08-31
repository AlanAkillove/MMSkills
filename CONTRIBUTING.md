# Contributing to MathModelingSkills

感谢参与。这个项目处理论文、竞赛规则、代码和 AI 会话记录，贡献时要同时考虑质量、可追溯性和隐私。

## 贡献前提

- 贡献材料只使用脱敏样例，不含真实参赛队成员姓名、学校、地区、联系方式、未公开数据、完整私人会话或身份附件。
- 赛事经验按赛事、年份、来源和核验日期记录，跨赛事复用前先建立适配范围。
- AI 检测分数只作为待核实线索，不作为作者身份或违规事实证据。
- 语言自然化以准确、自然和作者可确认的学术表达为目标。
- 涉及核心数学结论、数据、参数、实验结果或引用的修改，都记录变更原因和影响。

## 新增或修改 skill 的最低要求

每个 skill 至少应包含：

1. `SKILL.md`：清晰的触发描述、输入输出契约、工作流程、硬性禁令和停止条件。
2. 至少一个脱敏的正例与一个反例，放在 `tests/fixtures/` 或 skill 自己的 `examples/` 中。
3. 对外部规则、规范和容易变化的事实给出来源及适用范围。
4. 能在长论文上分块运行，并说明如何续接状态，而不是要求一次性读取全部上下文。
5. 明确哪些步骤必须由人确认，哪些步骤可以自动化。

## 推荐的 skill 目录

```text
skills/<skill-name>/
├── SKILL.md
├── agents/openai.yaml        # 需要显式路由或 UI 元数据时才添加
├── references/               # 仅放本 skill 需要的详细资料
├── scripts/                  # 重复且确定性的机械任务
├── templates/                # 输出模板
└── examples/                 # 脱敏示例
```

技能正文应保持短而有判别力；长规则、词表、格式表和样例优先放到 `references/`，按需加载。

## 本地验证

先安装开发依赖：

```text
python -m pip install -r requirements-dev.txt
```

然后运行契约测试和脚本编译：

```text
python -m pytest -q
python -m compileall -q skills tests
```

在安装了 Codex skill 工具链的环境中，至少运行：

```text
python <skill-creator-root>/scripts/quick_validate.py skills/<skill-name>
```

若 skill 有脚本或 PDF 输出，还要运行对应的 fixtures 测试、结构检查和视觉检查，并在 PR 中记录命令与结果。

## Pull request 要求

PR 描述至少回答：

- 解决了哪一类真实问题？
- 输入、输出和人工确认点是什么？
- 是否涉及竞赛规则、隐私或外部来源？
- 如何证明没有引入术语膨胀、事实漂移或静默删改？
- 是否补充了反例测试？

涉及架构或规则边界的修改，请新增或更新 `docs/adr/` 中的决策记录。
