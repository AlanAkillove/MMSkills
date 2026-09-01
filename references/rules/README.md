# Rules Profiles

规则适配器是按赛事和年份组织的参考资料。运行 skill 前，应先选择并核验 profile；没有匹配 profile 时，不得从相近赛事推断合规结论。

每个 profile 要记录：

- 官方来源、发布日期、访问日期和内容 hash；
- AI 可用、限制、禁止和未知范围；
- 声明文本、详情文件、提交位置和必填字段；
- 论文、附录、代码、支撑材料、文件大小和匿名要求；
- 规则冲突、地方附加要求和解释权；
- `draft/verified/conflict/stale/blocked` 状态以及下一次复核日期或复核触发条件。

当前已建立：

- [CUMCM 2026](cumcm-2026.yaml)：官方中文 AI 细则、参赛规则和论文格式规范快照；2026-09-01 已对照官网与本地 PDF，将参考文献列 AI、正文标注等记为 **not_required**（不是 prohibited）。因赛区附加通知与作者签核未齐，状态仍为 `draft`；
- [CUMCM 2026 说明](cumcm-2026.md)：面向阅读的规则解释。

统计建模、MathorCup、研究生数模和 COMAP 的材料目前作为调研来源，待取得并核验当届官方附件后再转为可执行 profile。
