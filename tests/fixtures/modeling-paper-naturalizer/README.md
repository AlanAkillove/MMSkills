# `modeling-paper-naturalizer` fixtures

这些 fixture 用于检查保真修稿边界，不代表真实论文。

- `positive-conservative-method.md`：方法段落应保留公式变量、条件和步骤，只修复句法。
- `positive-topic-specific-results.md`：结果段可自然化，但保留数字、范围和图表证据。
- `negative-template-introduction.md`：空泛背景与段末套话应压缩为题目具体信息。
- `negative-meaning-drift.md`：改写不得把相关变因果、把候选最好变最优。
- `negative-protected-latex.md`：LaTeX 命令、引用键、标签和公式不可被破坏。
- `negative-missing-evidence.md`：证据缺口应报告，不得用自然句子填补。
- `negative-terminology-drift.md`：不得为了自然改写而轮换术语或变更单位。
- `negative-redundant-defensive-statements.md`：删除或合并无新信息的自我免责，但不能凭空补出适用范围。
- `positive-required-limitation.md`：有证据边界的局限必须保留。
