# MathModelingSkills

面向数学建模竞赛与研究型建模任务的人机协作 Skills 工作台。

[![quality](https://github.com/AlanAkillove/MMSkills/actions/workflows/quality.yml/badge.svg)](https://github.com/AlanAkillove/MMSkills/actions/workflows/quality.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![version](https://img.shields.io/badge/version-0.3.1-blue)

## 项目简介

MMSkills 将建模工作划分为 **Modeler、Computationalist 和 Writer** 三类角色，根据当前任务按需加载 specialist skills。项目强调 problem-first 的模型设计、文献与领域机理辅助建模、可复核的计算结果，以及保持作者术语和表达习惯的论文写作。

它不是自动完成整场比赛的流水线。Agent 可以主动检索、推导、实现、试算和起草，而题意解释、关键假设、模型采用、结果冻结与最终提交仍由用户决定。

当前默认入口是 `math-modeling`。对话先落到三个角色；二十多个 specialist 仍然保留，只在当前任务需要时加载。

## 核心设计

| 原则 | 含义 |
|---|---|
| Problem first | 先理解对象、机理、约束、数据和任务，再形成候选模型，不从算法名称开始选型 |
| Human-led judgment | Agent 可以探索、比较、实现和起草；模型采用、关键假设、结果冻结和提交由用户确认 |
| Progressive disclosure | 默认只加载当前角色和必要 specialist，不预加载完整工作流 |
| Evidence before prose | 文献、代码、实验结果和术语先形成可核查依据，再进入正式论文 |
| Tools for mechanical checks | 引用、结果 freshness、图表、TeX/PDF 等确定性问题尽量交给工具检查 |
| Author-aware writing | 建模阶段建立术语，写作阶段检查 drift；自然化不以 AI 检测分数为目标，也不用换词制造差异 |

MMSkills 采用开放建模与确定性工具相结合的设计。角色用于划分任务边界；specialist skills 根据当前意图按需加载，不构成强制执行顺序。仅靠提示词约束无法保证结果可靠，因此可确定的检查应尽量交给工具完成。

## 三角色工作方式

| 角色 | 负责的问题 | 常见任务 |
|---|---|---|
| Modeler / 建模手 | 题意、领域机理、文献、假设、术语、模型构思 | 理解结构、调研相关工作、比较模型 |
| Computationalist / 编程手 | 数据、实现、实验、数值核验、图表、结果来源 | 数据处理、求解、敏感性分析、生成研究图 |
| Writer / 论文手 | 论文结构、正文、引用、术语一致性、审稿与排版 | 写摘要、修改章节、术语审查、终稿预检 |

角色只是任务边界，不是阶段流水线。用户可以从任意角色开始，也可以随当前问题切换。

完整赛程初始化、跨会话恢复和提交前全检才需要编排器。日常对话不预加载工作流，也不因为调用了某个 skill 就生成过程账本。

## 快速开始

安装完成后，不需要记住 specialist 名称，直接描述当前任务：

- `先帮我弄懂这个微通道结构。`
- `根据这些论文继续讨论问题三的模型。`
- `跑一下参数敏感性分析。`
- `检查图 8 的设计和标注。`
- `继续精修论文 5.3 节。`

MMSkills 会先判断当前任务属于哪个角色，再按需读取 specialist。普通局部任务不会启动完整 pipeline，也不会因为调用 Skill 自动生成过程账本。

仓库地址：[`https://github.com/AlanAkillove/MMSkills`](https://github.com/AlanAkillove/MMSkills)

让 Agent 接入本项目前，先读[跨 Agent 安装教程与安装提示词](docs/agent-skill-installation.md)。不同宿主的 skill 目录、插件和项目指令并不通用；能 clone 仓库，不等于当前应用已经发现、启用或验证了这些技能。提示词可以直接复制：

```text
请将 https://github.com/AlanAkillove/MMSkills.git 接入当前 Agent；先判断你当前支持的 skill、插件或项目指令规范，再按教程选择适配方式并报告 copied、discovered、activated、verified 状态。不要把 Codex 的目录格式当成通用标准，也不要自动运行脚本或替我决定数学建模的核心内容。
```

## 主要能力

| 能力 | 说明 |
|---|---|
| 统一入口 | `math-modeling` 按当前意图路由到三角色，再加载必要 specialist |
| 题意与模型 | 从题目结构、领域机理和文献证据形成候选模型；不建设用于发现的算法知识库 |
| 文献证据 | 发现与核验分开；文献服务模型综合，而不是提供可套用的方法模板 |
| 计算与结果 | 用 snapshot 和 run summary 记录来源与 freshness，便于发现过期数字 |
| 术语治理 | 建模阶段建立术语表，写作阶段做 drift 检查，避免终稿才统一用词 |
| 写作与自然化 | 终稿精修默认按可定位信号做最小修改；作者风格优先于通用去模板规则 |
| 机械 QA | citation 对照、图表几何、TeX/PDF 预检接入终检；不确定项标为未评估 |
| 赛事规则 | 规则按赛事、年份、来源和核验日期登记；未核验前标为未知 |

数模论文的差异应来自题目特征、模型取舍和实际证据，而不是术语包装或无必要的复杂化。完整技能列表见 [技能目录](docs/skill-catalog.md)。

## 项目状态

当前版本：**0.3.1**

0.3 系列已经完成三角色入口、渐进加载、术语治理、结果 snapshot、基础 citation / figure / PDF QA，以及证据约束的学术自然化。

目前仍在进行真实 Agent 行为回放。现有 CI 主要验证代码和契约，不能替代实际 Codex / DeepSeek Harness 会话中的模型级评估。

仍在推进的工作包括：

- test1 与 26A 等真实项目回放；
- 联网文献 discovery 与原始来源 verification 的进一步衔接；
- 不同宿主下 progressive disclosure 的实际行为验证。

完整实施记录见 [Implementation Roadmap](docs/implementation-roadmap.md)。

## 仓库结构

```text
skills/       三角色入口与 specialist skills
docs/         架构、ADR、质量模型与研究说明
schemas/      共享状态、证据和决策契约
templates/    TeX、术语表、披露等模板
profiles/     工作深度与赛事规则 profiles
hosts/        可选 Agent 宿主适配
tests/        契约测试、工具测试与脱敏 fixtures
```

更细的地图在 [技能目录](docs/skill-catalog.md) 和 [架构说明](docs/architecture.md)。三角色工作台的取舍见 [ADR 0009](docs/adr/0009-role-oriented-workbench.md)；自然化收口见 [ADR 0010](docs/adr/0010-evidence-grounded-naturalization.md)。

## 文档

| 文档 | 内容 |
|---|---|
| [Architecture](docs/architecture.md) | 角色边界、入口与产物关系 |
| [Skill catalog](docs/skill-catalog.md) | specialist 目录与优先级 |
| [Quality model](docs/quality-model.md) | 质量维度与验收口径 |
| [Implementation roadmap](docs/implementation-roadmap.md) | 版本历史与未完成项 |
| [Agent installation](docs/agent-skill-installation.md) | 跨宿主安装与验证 |
| [ADR 0009](docs/adr/0009-role-oriented-workbench.md) | 三角色工作台 |
| [ADR 0010](docs/adr/0010-evidence-grounded-naturalization.md) | 证据约束的学术自然化 |

## 致谢

MMSkills 的设计过程中研究并参考了多个优秀的开源数学建模与 Agent 项目。这些项目在角色划分、渐进加载、证据检索、结果复现、图表质量控制、人机协作边界和写作自然化等方面提供了重要启发。

MMSkills 并不是这些项目的 fork，也没有照搬它们的完整工作流。我们根据自己的数学建模实践重新选择、组合和实现相关思路。

| 项目 | 对 MMSkills 的主要启发 |
|---|---|
| [XiaoMaColtAI/math-modeling-skill](https://github.com/XiaoMaColtAI/math-modeling-skill) | Modeler / Programmer / Writer 的角色化入口、渐进加载、工具化实践，以及建模阶段提前建立术语表 |
| [jihe520/MathModelAgent](https://github.com/jihe520/MathModelAgent) | 成果文件质量检查、论文/PDF 终检和完整建模项目的工程组织方式 |
| [RealSeaberry/AutoMCM-Pro](https://github.com/RealSeaberry/AutoMCM-Pro) | 代码结果自检、数值 sanity check 和可复现结果管理 |
| [sweetcornna/mathodology](https://github.com/sweetcornna/mathodology) | 文献 discovery 与 verification 分离、来源核验、证据追踪与研究型检索 |
| [BZDmathclub/bzd-math-modeling-skills](https://github.com/BZDmathclub/bzd-math-modeling-skills) | 根据当前赛题形成评审关注点，而不是用固定评分模板审查所有论文 |
| [hrdZhu/modelviz-skill](https://github.com/hrdZhu/modelviz-skill) | 图表服务于具体 claim、技术 QA 与视觉 QA 分离，以及可复现绘图 |
| [zhnnky329/MathModeling-skills](https://github.com/zhnnky329/MathModeling-skills) | human-led workflow、model feasibility probe、结果 freeze、轻量运行记录和事件驱动产物 |
| [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) | 证据约束的语言自然化、负面信号、最小修改以及作者风格优先 |

感谢这些项目公开其设计、代码和研究过程。若后续直接复用第三方代码或文档，MMSkills 会在对应文件中保留原项目要求的许可证和版权声明。

## 贡献

请先看 [CONTRIBUTING.md](CONTRIBUTING.md)。涉及竞赛规则、AI 使用或隐私的改动，需要同时留下来源、适用范围、人工确认点和脱敏测试；规则只有核验之后才能写进对应赛事 profile。

本地最小检查：

```text
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m compileall -q skills tests
```

TeX 模板另跑 `python skills/modeling-tex-paper-production/scripts/check_tex_template.py templates/tex/main.tex`；本机有 TeX 时再编译并检查 PDF。

## 许可证

MIT License，见 [LICENSE](LICENSE)。若以后引入许可条件不同的第三方内容，会在对应文件和 `docs/research/` 里单独标明。
