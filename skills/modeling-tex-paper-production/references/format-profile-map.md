# 赛事格式 profile 与 TeX 开关映射

本文件只记录当前调研得到的适配思路，不替代目标赛事当届官方文件。所有字段应带 `required`、`forbidden`、`recommended` 或 `unknown` 状态和来源锚点；无法确定时不自动选择。

## 共同字段

| 字段 | 需要先确认的事实 | TeX 中的影响 |
|---|---|---|
| `engine` | XeLaTeX、LuaLaTeX、官方 Word 模板或其他 | 选择编译器和字体方案；不把 `latexmk -pdf` 当成 XeLaTeX |
| `paper_size` / `margins` | A4、Letter、最小页边距或模板固定尺寸 | `geometry` 只在规则允许自行设置时使用 |
| `first_page` | 摘要/summary、封面、承诺书或专用摘要页 | `\maketitle`、`abstract`、专用页面和页码起点 |
| `table_of_contents` | 必须、允许还是禁止 | 控制 `\tableofcontents`，不以“读者体验”覆盖明文禁令 |
| `page_numbering` | 位置、起点、是否带总页数 | `fancyhdr`/`plain` 页脚或页眉；按官方示例设置 |
| `header` | 是否要控制号、队号、短标题或明确禁止页眉 | 默认无页眉；只有 profile 明确要求时开启 |
| `main_text_limit` | 正文上限还是整份 solution 上限，附录是否计入 | 在构建清单里按规则分段计数，不用缩字号作弊 |
| `appendix_and_code` | 附录是否无限、代码必须进论文还是另交 | 决定 `\appendix`、`\lstinputlisting` 和支撑材料清单 |
| `identity` | 哪些页面可出现队号/学校/成员信息 | 统一扫描 PDF、源稿、图片元数据和支撑包 |
| `language` | 中文、英文或官方双语要求 | 选择 `ctexart`/英文类、术语账本和参考文献样式 |
| `ai_disclosure` | 是否要声明、引用、局部标注和详情 PDF | 在参考文献前插入最小声明；详情按单独 artifact 生成 |
| `citation_style` | 编号、作者-年份、脚注、官方模板格式 | 选择 `.bst`/biblatex/手工环境，但禁止编造条目 |

## 已调研赛事的适用边界

### 全国大学生数学建模竞赛（CUMCM）

以官方 2026 年格式规范和 AI 使用规定为例：纸质版是 A4、上下左右至少 2.5 cm，承诺书/编号专用页/摘要页有专门顺序；电子论文不放承诺书和编号专用页，首页为摘要页；正文不超过 30 页、不设目录，附录页数不限；电子论文为单独 PDF 或 Word，建议 PDF，大小不超过 20 MB；支撑材料另行压缩，文件列表放入附录并保持匿名。字号、字体、行距和颜色在规范中没有统一指定，赛区可以另行要求。

2026 年 AI 试行规定要求在参考文献前设置二选一的 AI 工具使用声明；使用过 AI 的作品还要在支撑材料提交 `AI工具使用详情.pdf`，说明工具、用途/环节、主要提示方式与过程、采纳/人工修改/核验情况。它不要求把一份通用的“AI 边界宣言”塞进正文，也不允许用模板替代真实记录。

因此，CUMCM 电子论文可将通用模板的开关理解为：

```text
first_page = abstract
table_of_contents = forbidden
header = usually_forbidden
footer_page_number = centered_arabic_from_abstract
main_text_limit = 30 pages (definition must be confirmed at submission)
appendix = included in paper, page count not limited by this rule
identity = forbidden in abstract/body/appendix/support package
ai_statement = before_references_if_required_by_current_profile
```

这只是适配示意。纸质版封面、编号页和电子版裁剪不能由通用模板自动替用户生成或合并。

### COMAP MCM/ICM

COMAP 的官方 2027 instructions 要求英文、可读字号至少 12 pt、PDF、首页为 Summary Sheet、每页顶端包含 team control number 与页码，并要求匿名；官方问题文件和说明还会规定 Summary Sheet、目录、完整解答、memo/letter、参考文献和 AI Use Report 的组成。当前 instructions 还规定 25 页总限制，但不同当届页面对 AI report 是否计入有专门措辞，必须以当届 instructions、problem statement 和 AI policy 共同核对。

COMAP 同时提供官方 LaTeX Summary Sheet；本项目只借鉴“首面摘要、顶部控制号、英文可读性和信息顺序”，不复制官方 class 或固定内容。

```text
first_page = summary_sheet
table_of_contents = required_in_current_instructions
header = control_number_and_page_number_required
language = English
identity = names/institution forbidden, control number allowed
page_limit = current instructions; confirm whether appendix/AI report is included
ai_report = follow current COMAP AI policy and problem-specific instructions
```

### MathorCup 高校数学建模挑战赛（公开历史规则对照）

官方公开的第十三届格式说明要求：题目、摘要和关键词在第一页，第二页为目录，正文从目录后开始编号；不得有页眉，不得出现身份/学校信息；中文写作，正文约 30 页、附录不限；引用需在正文和参考文献中标注；程序等按当届要求放入附录/支撑材料。该页面是历史届次材料，不能直接当作 2026 或未来届次规则。

```text
first_page = title_abstract_keywords
table_of_contents = required_in_that_edition
header = forbidden_in_that_edition
footer_page_number = centered_arabic_from_body
language = Chinese
page_limit = historical "about 30" guidance; confirm current edition
```

### 中国研究生数学建模竞赛（公开历史通知对照）

官方平台公开的第二十二届通知要求按组委会论文模板编写，首页为不可删除的封皮，第二页起为摘要和正文；封皮外页面不得出现单位、姓名、队伍编号等信息，摘要不超过两页。它说明了“官方专用模板优先”的重要性：此类任务不应把中性 `ctexart` 模板直接作为提交稿。

## 通用模板开关

仓库 `templates/tex/main.tex` 提供以下默认开关，仅是源稿层的起点：

```tex
\mmIncludeContentsfalse       % COMAP/其他要求目录时再开启
\mmIncludeAIStatementfalse   % 只有 profile 与事件记录支持时开启
\mmIncludeCodeAppendixfalse  % 只有赛事明确要求且篇幅允许时开启
\mmShowHeaderfalse           % 只有 profile 要求控制号/页眉时开启
\mmIncludeBibliographyfalse  % 有已核验且实际引用的来源后才开启
```

变更开关前要在 profile 和 `decision_log.md` 中写明依据。不要通过 `\fontsize`、负间距、透明文字、不可见身份字段或压缩图片元数据绕过规则。

## 来源

- CUMCM 官方格式规范：[mcm.edu.cn](https://www.mcm.edu.cn/html_cn/node/4cd596519c9eb9fbd866398f6df0caa3.html)；
- CUMCM 官方 AI 规定：[mcm.edu.cn](https://www.mcm.edu.cn/html_cn/node/fef94648f2836ab6cc81586f4c38512b.html)；
- COMAP 官方 instructions：[contest.comap.com](https://www.contest.comap.com/undergraduate/contests/mcm/instructions.html)；
- COMAP 官方 AI policy：[Contest_AI_Policy.pdf](https://www.contest.comap.com/undergraduate/contests/mcm/flyer/Contest_AI_Policy.pdf)；
- MathorCup 官方历史格式页面：[mathorcup.org](https://www.mathorcup.org/detail/2414)；
- 中国研究生数学建模竞赛官方平台通知：[cpipc.acge.org.cn](https://cpipc.acge.org.cn/cw/contestNews/detail/4/2c90801b9914a68201994b1403512e96?page=1)。
