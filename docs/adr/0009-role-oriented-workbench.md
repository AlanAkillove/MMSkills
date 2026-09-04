# ADR 0009：三角色工作台与渐进加载

- 状态：accepted
- 日期：2026-09-04
- 适用版本：0.3.0-rc2

## 背景

0.2.2 把动作门做到了运行时，但用户和 Agent 仍首先面对二十多个 specialist。社区仓库（XiaoMa 三角色入口、zhnnky 的 human-led skills、Mathodology 的 discovery≠verification）说明：值得借鉴的是认知入口、渐进加载和机械工具，而不是固定门禁、算法目录或数量 KPI。

使用者明确拒绝把算法知识库当作模型发现入口：物理/工程题应先理解对象与机理、再查领域文献，而不是从优化/预测/评价标签里挑选方法。

## 决策

1. 新增极薄的 `math-modeling` 统一入口。默认只路由到 Modeler / Computationalist / Writer。现有 specialist 保留，不合并、不删除。
2. 普通交互不经过 `modeling-pipeline-orchestrator`，不预加载 stage registry 或 process-freezer。编排器只用于完整赛程初始化、跨会话恢复、full audit、提交诊断。
3. Progressive disclosure 四层：Router → Role → Specialist → Reference/Tool。Never preload the workflow.
4. 建模遵循 problem-first、literature-guided。不建设用于模型发现的算法知识库；不问“选哪个算法名”。文献不足时可以提出 provisional candidate，但必须标明 literature-backed 与 model-knowledge-derived。
5. 术语在建模阶段建立 `terminology_table.md`；`modeling-terminology-auditor` 分为 `establish` 与 `audit`。写作阶段只做 drift regression。
6. 能由脚本确定的检查写成工具。本轮加入 results snapshot、run_summary、figure placement、本地 citation 对照、PDF 机械页面 QA，以及终检胶水；联网检索仍后续补齐。DeepSeek Harness 只作为可选 native-adapter，不进入主架构。
7. 事件驱动留痕：不因为 skill 被调用而创建文件。Action gate 沿用 0.2.2。
8. 0.3.0 不以 pytest 通过宣称实践成功；真实 Agent 回放仍是发布门。

## 明确不做

算法百科、model dictionary、固定候选/图数量、强制 baseline、G1–G6 普通流水线、每轮实验报告、自动国奖打分、四段式摘要、固定正文章节。

## 后果

- “继续问题三”只加载当前角色与必要 specialist；
- “比较几个模型”走 Modeler + model-architect，不打开算法目录；
- “hydraulic diameter 全文统一”才更新术语表；解释 Re 定义不落盘。
