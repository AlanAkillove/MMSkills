# MathModelingSkills

面向数学建模竞赛与相关技术报告的全流程 Agent 技能库。

本项目将 Agent 定位为数学建模团队的协作工具：人类负责核心建模判断与最终提交，Agent 负责问题理解、资料核验、数据审计、候选方案整理、实验记录、论文写作辅助、审稿式检查、语言自然化、格式预检和 AI 使用披露，并把这些工作组织成可追踪、可复核、可移交的流程。流程是辅助层，不是每轮对话必须完成的审批表。

> 当前状态：0.2.2 把动作门做到运行时，并继续瘦身高频写作 skill。`blocking` 跟随当前动作；正式采用要有 human-confirmed decision；默认 TeX 附录也退出通用模板。仓库 CI 仍是 fixture/contract tests，第一次真实 Agent 的 test1 重放尚未完成，不能把 pytest 通过写成实践项目已经成功。

## 0.2 的协作原则

用户当前目标优先于推荐阶段图。`execution_requires` 才是开始当前任务的硬依赖；`adoption_requires` 只在正式采用、冻结或提交前生效；`recommended_after` 只是建议先后。Agent 可以在核心内容尚未最终确认时给出候选、解释和暂定草稿，但不能把它们写成已采用的模型、结论或最终提交稿。

用户可感知的工作强度是 `working_depth = light | standard | full`。默认先在对话中推进问题；只有跨会话、用户要求留痕、完整审计或最终交付时才落盘账本。

项目内部账本、finding/decision ID、状态和待确认项属于追踪层；最终论文属于成文层。交付前必须运行成文清洁检查，清除草稿标记、占位符、内部编号和无功能的过程性话语，同时保留真正影响结论范围的限制和合规信息。

## 设计原则

1. **人类敲板**：题意解释、关键假设、模型取舍、参数口径、实验结论和最终提交均必须有明确的人类确认点。
2. **证据先于表述**：论文中的每个重要结论都要能回到数据、公式、实验、图表或可靠文献。
3. **术语克制**：只保留有必要、可定义、可复用的术语；拒绝为了制造“高级感”而给普通事实重新命名。
4. **阅读体验优先**：先保证读者能沿着“问题—方法—证据—结论”顺畅阅读，再做句式和词汇层面的润色。
5. **反同质化**：不把“换几个词”当作原创性。优先从题目特征、建模路径、证据组织、图表设计和作者决策中保留差异，同时拒绝为求独特而强行复杂化。
6. **自然化服务于表达质量**：去模板化和去 AI 味儿以清晰、准确、符合作者意图的学术表达为验收标准，不使用检测器结果作为目标。
7. **规则按赛事适配**：AI 使用、页数、附录、支撑材料和格式要求均依据目标赛事最新官方规则处理，单一赛事条款只在其适用范围内生效。
8. **过程可追溯**：尽可能记录输入、输出、采纳情况、人工改动、验证方式和决策归属；无法确定的字段必须明确标为未知。
9. **人类可决策**：复杂候选先用分层说明降低理解负担，再把适配、代价、风险、未知和验证路径交给人判断；不以总分、默认推荐或沉默同意替代人工决定。

## 全流程蓝图

```text
题目与规则接收
  -> 规则画像与合规边界
  -> 全部题目盘点与选题分析
  -> 人类确认主选/备选题目
  -> 背景/文献学习与多轮理解确认
  -> 题意拆解与问题地图
  -> 写前差异化路径与题目锚点登记
  -> 数据/资料审计
  -> 基线与候选模型
  -> 人类模型决策门
  -> 实现、实验与验证
  -> 论文结构、图表设计与论证链
  -> 论文正文写作与成文清洁
  -> 同质化/术语/证据/阅读体验审查
  -> 自然化修稿与二次核对
  -> AI 使用记录整理与披露 PDF
  -> 格式、支撑材料与提交预检
  -> 人类最终冻结
```

## 目录

```text
skills/       可被 Agent 调用的专项技能；每个技能独立目录、独立 SKILL.md
references/   共享规则、检查表、术语与证据规范
templates/    项目状态、日志、报告和披露材料模板
schemas/      跨 skill 的机器可读状态、证据、决策、finding、模型和实验契约
profiles/     research-full、contest-standard、contest-fast 运行档位
scripts/      确定性辅助脚本，例如结构检查、日志转换、PDF 生成与验证
tests/        技能契约测试、反例和脱敏 fixtures
docs/         架构、研究记录、决策记录与质量模型
tmp/          本地临时文件，不纳入版本控制
```

## 技能族

### 研究与建模前

- 多题全量盘点、分项选题比较与人工选题门
- 题意解析与问题地图
- 题目背景、对象关系、术语和文献边界的分轮熟悉
- 规则画像与赛事合规
- 文献/公开资料检索与证据卡片
- 数据字典、数据质量与口径审计
- 建模假设登记与候选模型比较

### 实现与验证

- 可复现实验注册
- 模型诊断、敏感性分析与稳健性检查
- 论文图表设计、制作与多面板编排
- 结果—图表—结论一致性审计
- 代码、数据、支撑材料和运行环境预检

### 论文写作与审修

- 数模论文结构与论证链构建
- 以用户意图为先的论文正文、摘要和分节写作
- 反同质化设计与作者决策保真
- 术语规范与术语账本
- 审稿角色的实质问题审查
- AI 模板化痕迹识别（只报告可观察信号和证据边界）
- 中文学术表达自然化
- 阅读体验与信息架构审查
- 最终格式和提交预检
- TeX 源稿生产、赛事版式适配、编译和 PDF 页面预检

### 过程与披露

- 会话/本地日志归档与证据抽取
- AI 工具使用详情整理
- 面向具体赛事的披露 PDF 生成
- 人类确认、版本冻结与交付清单

## Agent 安装

本项目地址：[`https://github.com/AlanAkillove/MMSkills`](https://github.com/AlanAkillove/MMSkills)

如果要让 Agent 安装或接入本项目，请先阅读[跨 Agent 安装教程与安装提示词](docs/agent-skill-installation.md)。教程中的提示词可以直接复制给当前 Agent：

```text
请将 https://github.com/AlanAkillove/MMSkills.git 接入当前 Agent；先判断你当前支持的 skill、插件或项目指令规范，再按教程选择适配方式并报告 copied、discovered、activated、verified 状态。不要把 Codex 的目录格式当成通用标准，也不要自动运行脚本或替我决定数学建模的核心内容。
```

Agent 应先根据自身宿主能力选择项目级、用户级、会话级或仅提示词方式；不能因为仓库地址可访问就声称技能已经被当前应用发现、启用或验证。

## 当前工作方式

本项目按“总设计 → 分板块调研 → 契约冻结 → 技能实现 → fixtures 测试 → 行为级回归 → 脱敏真实项目只读回归 → 发布准备”的顺序推进。0.2.0 本轮重点是让阶段注册表、运行档位和 schema 真正支持意图优先，同时把论文成文清洁纳入最终预检。规则实现目前以 CUMCM 为首个具体适配对象，其他赛事必须另建并核验 profile，不能从 CUMCM 自动推断。

详见：

- [总架构](docs/architecture.md)
- [分板块调研计划](docs/research-plan.md)
- [技能目录与优先级](docs/skill-catalog.md)
- [分板块细化设计](docs/block-design.md)
- [实施路线图](docs/implementation-roadmap.md)
- [AI 使用披露设计草案](docs/ai-disclosure-design.md)
- [反同质化设计草案](docs/anti-homogenization-design.md)
- [质量模型与问题分类](docs/quality-model.md)
- [共享机器契约与阶段注册表](schemas/README.md)
- [运行档位](profiles/README.md)
- [行为级回归场景](tests/behavioral/README.md)
- [跨宿主兼容性烟雾矩阵](tests/compatibility/README.md)
- [跨 Agent 安装教程与安装提示词](docs/agent-skill-installation.md)
- [TeX 模板设计与赛事排版调研](docs/tex-template-design.md)
- [TeX 通用模板](templates/tex/README.md)
- [0.2.0 意图优先与软硬边界 ADR](docs/adr/0006-intent-first-adaptive-workflow.md)

## 贡献与使用

请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。涉及竞赛规则、AI 使用或隐私的变更，需要同时更新来源、适用范围、人工确认点和测试 fixtures；规则条目只有在完成人工核验后，才能写入对应赛事 profile。

本地最小验证：`python -m pip install -r requirements-dev.txt`，然后运行 `python -m pytest -q` 和 `python -m compileall -q skills tests`。TeX 还需运行 `python skills/modeling-tex-paper-production/scripts/check_tex_template.py templates/tex/main.tex`，在本地 TeX 环境可用时编译并渲染 PDF；AI 详情 PDF 还需按对应 skill 的 fixtures 命令做结构和视觉检查。

如果要直接让 Agent 安装本项目，请先使用[跨 Agent 安装教程与安装提示词](docs/agent-skill-installation.md)。教程要求 Agent 先判断当前应用支持的 skill、插件或项目指令规范，再选择适配方式；不默认把 Codex 的目录和元数据当成所有 Agent 的通用格式。

## 许可证

本项目暂采用 MIT License，见 [LICENSE](LICENSE)。若后续引入具有不同许可条件的第三方内容，将在对应文件和 `docs/research/` 中单独标明来源与许可。
