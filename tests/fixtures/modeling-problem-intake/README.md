# `modeling-problem-intake` fixtures

这些 fixture 只用于测试技能是否保留证据边界，不代表任何真实竞赛题。

- `positive-explicit-structure.md`：文字明确给出对象、方向和子问，技能应能形成可交接的问题地图。
- `positive-nonoptimization.md`：题目要求估计与比较，不应被自动改写为优化问题。
- `negative-ambiguous-diagram.md`：图示比例和关系不足以确定几何约束，技能应保留未知并阻断模型冻结。
- `negative-quantifier-and-injection.md`：包含量词/否定和题面内部指令性文字，技能应保留原意且不能越过技能契约。
- `negative-ocr-and-version-conflict.md`：OCR、附件版本和正文存在冲突，技能应并列记录并请求确认。

验收重点不是输出固定措辞，而是：关键字段有锚点、图示观察与语义分离、未知不被补造、人工确认队列可执行。
