# `modeling-assumption-ledger` fixtures

fixture 用于检查“假设是否可追溯、是否分解、是否越过人工确认”，不代表真实赛题。

- `positive-explicit-assumptions.md`：题面条件、团队简化和计算便利条件可以清楚区分。
- `positive-nonoptimization-boundary.md`：估计/比较题的假设不能偷偷引入优化或因果含义。
- `negative-silent-topic-change.md`：用方便计算的假设改变题意对象和时间范围，应阻断。
- `negative-unverified-independence.md`：自动补 i.i.d./正态/因果等统计前提，应标为待确认。
- `negative-code-paper-conflict.md`：代码默认值与论文描述冲突，应并列记录。
- `negative-unsupported-sensitivity.md`：没有运行敏感性实验却声称“结论稳健”，应标记证据缺失。
