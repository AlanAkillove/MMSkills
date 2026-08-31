# Skills

这里存放可被 Agent 调用的专项技能。每个目录应只承担一个可辨认的职责，避免把研究、写作、审稿、披露和格式处理揉成无法测试的超长提示词。

## 命名约定

使用小写 kebab-case，例如：

```text
modeling-problem-intake
modeling-claim-evidence-audit
modeling-paper-naturalizer
modeling-ai-use-disclosure
```

每个 skill 的 `SKILL.md` 是入口；详细词表、规则矩阵、长样例和脚本按需放在同目录下。

## 已实现

- [`modeling-problem-intake`](modeling-problem-intake/)：将题面整理为带证据锚点的问题地图，专门处理图示/几何关系、边界条件、歧义和长题面续接。
- [`modeling-assumption-ledger`](modeling-assumption-ledger/)：登记题面条件、团队假设、推导条件和计算便利条件，追踪影响、边界、验证与人工确认。
- [`modeling-claim-evidence-audit`](modeling-claim-evidence-audit/)：逐项核对论文主张、证据类型、范围和措辞强度，分离补证据与限缩主张。
- [`modeling-terminology-auditor`](modeling-terminology-auditor/)：维护概念—术语—符号—单位映射，识别同义漂移和高级感包装。
- [`modeling-ai-pattern-reviewer`](modeling-ai-pattern-reviewer/)：定位可观察的论文模板化信号和防御性声明簇，保留合理规范并禁止 AI 来源归因。
- [`modeling-paper-naturalizer`](modeling-paper-naturalizer/)：在锁定数字、公式、术语、主张和证据后，做保真、最小化的中文表达自然化、声明去重和差异回归。
- [`modeling-paper-reviewer`](modeling-paper-reviewer/)：以证据化预审角色检查题意、模型、数据实验、主张、阅读体验和赛事边界，不替作者改稿或做来源归因。
- [`modeling-distinctiveness-coach`](modeling-distinctiveness-coach/)：在写前从题目锚点、团队决策和验证证据中保存真实差异，阻断强行复杂化和生造创新。
- [`modeling-anti-homogenization-auditor`](modeling-anti-homogenization-auditor/)：成稿后逐层回查题目特异性、模型路径、证据故事、术语贡献和图表表达是否被模板抹平。
- [`modeling-reader-experience-auditor`](modeling-reader-experience-auditor/)：沿快速评阅、技术复核和非本专业阅读三条路径检查导航、信息顺序、图表和注意力负担。
- [`modeling-rules-profile`](modeling-rules-profile/)：将指定赛事/年份规则转为带来源、有效期、冲突状态和人工确认门的 profile。
- [`modeling-data-audit`](modeling-data-audit/)：审计数据来源、口径、单位、质量、切分泄漏、授权和可复现性。
- [`modeling-model-architect`](modeling-model-architect/)：先建立可解释基线，再登记候选模型的适配、复杂度、验证和团队取舍。
- [`modeling-experiment-validator`](modeling-experiment-validator/)：登记基线、对照、敏感性、边界、不确定性和复现实验，防止只报最好结果。
- [`modeling-literature-evidence`](modeling-literature-evidence/)：围绕题意、方法、数据和主张建立来源清单与可核查证据链，阻断搜索摘要和虚构引用。
- [`modeling-paper-architect`](modeling-paper-architect/)：将题目、证据和主张组织为章节/段落契约，避免固定目录与清单式拼接。
- [`modeling-figure-designer`](modeling-figure-designer/)：从读者任务、证据角色和题目特征出发设计并制作可读、可复现、适合正文排版的图表与模型结构图。
- [`modeling-figure-table-auditor`](modeling-figure-table-auditor/)：逐图/表核对证据角色、数据/单位/来源、正文主张、版本和渲染可读性。
- [`modeling-support-materials-auditor`](modeling-support-materials-auditor/)：安全核对附录/压缩包、代码/数据、匿名信息和论文一致性，默认不执行陌生代码。
- [`modeling-final-preflight`](modeling-final-preflight/)：汇总规则与各专项证据状态，按 P0/P1 阻断高风险提交项并保留人工签核。
- [`modeling-ai-use-disclosure`](modeling-ai-use-disclosure/)：从明确授权的会话/日志抽取 AI 使用事件，核对规则与人工控制，并生成可验证的 AI 使用详情 PDF。
- [`modeling-process-freezer`](modeling-process-freezer/)：用 append-only 快照、SHA-256、状态谱系和人工签核保存长会话与改稿过程。
- [`modeling-pipeline-orchestrator`](modeling-pipeline-orchestrator/)：按阶段依赖、证据状态和人工门生成全流程运行计划，不替人作核心决定。

## 最低契约

- 描述应能区分“何时调用”和“何时不要调用”；
- 指明输入材料、读取顺序、输出文件和失败/不确定状态；
- 重要结论必须带证据锚点；
- 不得越过人类决策门替用户决定核心模型、核心假设或最终结论；
- 长材料必须支持分块、摘要、状态文件和续接；
- 涉及规则的 skill 必须使用赛事/年份适配器。
