# 术语 establish / audit 工作流

本文件按需读取。不要每轮重建全文账本。

## establish（建模手）

从题面、文献和模型对象收集概念。表格只有两张：概念与术语、符号与单位。只记录会造成概念漂移的 aliases，不禁止所有近义表达。

用户说“以后全文统一叫 hydraulic diameter”才写入 canonical 名。

## audit（论文手）

输入：`terminology_table.md`（或兼容的 `terminology_ledger.md`）+ 当前稿。

检查：未登记新术语、canonical 被换成包装词、高承诺词突然出现、中英对应改变、符号/单位漂移。不在 audit 中重新决定规范名。

## 机械检查

`scripts/check_terminology_drift.py` 只能抓住表中已登记的 ambiguous/deprecated 别名，以及一小类未登记的包装词模式。文采和概念是否同一仍需人看。
