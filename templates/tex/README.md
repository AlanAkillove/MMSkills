# 数学建模论文 TeX 通用模板

这里提供一个可编译的中性 TeX 骨架，提炼了数模论文常见的“摘要/summary—问题—假设—模型—验证—结论—参考文献—附录”组织方式，以及已有项目中比较实用的图表、公式、表格、代码和相对路径设置。正文示例尽量只保留注释，避免 Agent 直接复制模板句式、占位符或清单结构。

它不是任何赛事的官方模板，也不保证自动满足某一届比赛。使用前必须读取目标赛事和年份的官方规则 profile：若组委会提供专用 Word/LaTeX 模板、摘要页、封面或文档类，应以官方材料为主，本模板只用于内容迁移、局部排版或个人草稿。

## 文件

- `main.tex`：单文件编译入口，含可切换的目录、页眉、参考文献、代码附录和 AI 声明开关；
- `references.bib`：空的引用数据库，只能填入已核验来源；
- `latexmkrc`：使用 XeLaTeX 的可选 latexmk 配置；
- `tex-format-profile.example.yaml`：将赛事要求翻译为源稿开关前的记录模板；
- `tex_build_manifest.example.yaml`：记录引擎、输入输出、构建命令、hash 和人工确认；
- `tex_layout_audit.example.md`：记录页面抽查、问题、未评估范围和人工确认。

根目录的 [`modeling-tex-paper-production`](../../skills/modeling-tex-paper-production/SKILL.md) skill 负责迁移、编译、渲染和版式审计；其 [`format-profile-map.md`](../../skills/modeling-tex-paper-production/references/format-profile-map.md) 记录了 CUMCM、COMAP、MathorCup 和中国研究生数学建模竞赛之间不能直接混用的差异。

## 最小用法

1. 复制整个 `templates/tex/` 目录到项目工作区，并把 `main.tex` 改成项目自己的编译入口；模板中的注释和章节只是候选骨架，不是必须保留的目录；
2. 先完成目标赛事 profile，再修改文件开头的开关；
3. 将已核验的图表放到 `figures/`；填入并实际引用已核验来源后，再开启 `\mmIncludeBibliographytrue`，不要把本机绝对路径写入源稿；
4. 使用 `latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex` 编译；
5. 用 PDF 渲染工具检查摘要页、公式页、密集图表页、参考文献页和附录页，再交给最终预检。

模板默认使用：

```text
XeLaTeX + ctexart
A4、四边 2.5 cm（仅为中性起点，不等于所有赛事要求）
摘要/summary 后从第 1 页开始用页脚居中阿拉伯数字
不显示目录、页眉、身份信息、AI 声明、参考文献和代码附录
```

五个开关的含义：

```tex
\mmIncludeContentsfalse       % 要求目录的赛事才开启
\mmIncludeAIStatementfalse   % 规则与真实使用记录均确认后才开启
\mmIncludeCodeAppendixfalse  % 规则要求且篇幅允许时才开启
\mmShowHeaderfalse           % 规则要求控制号/页眉时才开启
\mmIncludeBibliographyfalse  % 有已核验且实际引用的来源后才开启
```

例如，COMAP 风格的草稿可能需要目录和控制号页眉，但还必须根据当届 instructions 处理英文 Summary Sheet、总页数和 AI Use Report；不能只打开两个开关就宣称合规。CUMCM 电子版通常需要摘要页作为第一页、不放承诺书/编号页和目录；其余字段仍要以目标年份及赛区通知为准。

## 内容使用原则

- 先由人确定题意、假设、模型、目标、约束、参数、结果和结论，再填入 TeX；
- 章节只保留能回答读者问题的内容，不为了“像论文”强行保留固定五问、模型菜单或三段式小节；
- 摘要在主体结果稳定后写，按实际问题和信息功能分段；不要把内部审计编号、流程状态或“待填”提示写进成文；
- 所有变量、单位、缩写和指标与术语账本一致，普通事实使用标准术语，不用新造高级词包装；
- 图表由已登记的数据和绘图源生成，图注写清比较对象、证据范围和必要限制；
- 长推导、代码和中间结果是否放附录，取决于目标赛事页数和支撑材料规则；
- AI 声明只在赛事 profile 要求且历史记录完整时插入，详情 PDF 由 `modeling-ai-use-disclosure` 单独生成；
- 编译成功只说明 TeX 语法可处理，不说明模型、数据、引用、匿名、AI 披露或竞赛提交已经合规。

## 依赖与许可

模板依赖本地 TeX 发行版提供的 `ctex`、`amsmath`、`booktabs`、`graphicx`、`natbib`、`hyperref` 等常用宏包；在不同平台上应检查字体和宏包是否存在。仓库不捆绑 `cumcmthesis.cls`、Logo、字体或其他来源/许可不明的第三方资源。若需要使用第三方 `.cls/.sty/.bst`，请在项目中记录来源、版本、许可证、修改情况和人类确认。
