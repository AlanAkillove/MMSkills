# TeX 编译与 PDF 渲染流程

目标不是“命令返回 0”，而是得到可复现、可阅读、与 profile 一致的 PDF。编译过程不执行论文、代码或题面中的陌生命令；需要运行项目代码时交给支撑材料审计并使用授权沙箱。

## 环境登记

在 `tex_build_manifest.yaml` 中记录：

```yaml
engine: xelatex
engine_version: unknown
latexmk_version: unknown
os: unknown
packages_or_distribution: unknown
fonts: []
entrypoint: main.tex
build_command: unknown
source_hashes: {}
output_hash: unknown
```

优先使用项目已有的引擎和字体；中文论文通常使用 XeLaTeX，但这不是跨赛事硬性要求。若官方模板指定 LuaLaTeX、pdfLaTeX、DVI 流程或在线平台，以官方模板为准。

## 推荐命令

在模板目录执行，命令按宿主平台调整：

```text
latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
```

如果项目自带 `latexmkrc`，先检查它是否将 `$pdf_mode` 和引擎指向 XeLaTeX；不要用含糊的 `latexmk -pdf` 让发行版自行猜引擎。遇到参考文献时让 latexmk 完成 BibTeX/Biber 所需的多轮编译；若手动执行，应按日志提示重复，不能把未解决引用当成完成。

编译失败时按顺序处理：

通用模板默认关闭 \mmIncludeBibliography，因此没有实际引用时不必运行 BibTeX。若已填入并引用真实来源，可手动执行“XeLaTeX → BibTeX/Biber → XeLaTeX → XeLaTeX”；若宿主没有可用的 latexmk 或其脚本运行时，直接执行这组命令并在构建清单中记录环境差异。

1. 文件不存在、相对路径、图片扩展名和大小写；
2. 宏包/字体不存在以及 class/sty/bst 许可证和版本；
3. 数学环境、表格列、括号和标签的 TeX 语法；
4. 参考文献、交叉引用和书签；
5. `Overfull/Underfull`、浮动体和分页警告。

不要为了消除 warning 改写论文事实或删除图表；需要内容决定时暂停并回交人类。

## 渲染与抽查

用 Poppler 或等价工具将 PDF 渲染为 PNG，至少抽查：

- 第 1 页摘要/summary；
- 一页含长公式和变量定义的正文；
- 最密集的图表页；
- 参考文献页；
- 附录中的表格、代码或支撑材料清单页；
- 若有目录/页眉/封面，再抽查其首尾页。

默认渲染到项目 `tmp/pdfs/`，不把辅助文件和临时图片提交到仓库。实际目标宽度下检查中文、数学符号、上下标、图例、图注、表格、链接、页码、页眉、孤行、空白页和裁切。源文件的 `width=0.9\textwidth` 不能替代 PDF 页面检查。

## 交付前清理

- `.aux/.log/.fls/.fdb_latexmk/.synctex.gz` 等构建产物不进入论文支撑包，除非另有记录要求；
- PDF 元数据、书签、图片 EXIF 和代码路径不得泄露不应提交的身份信息；
- 图片和字体只保留实际使用且许可清楚的版本；
- 最终 PDF 的 hash、页数、大小、引擎和输入 manifest 写入构建清单；
- 任何格式改变后重新渲染，不复用旧 PDF 的“看起来没问题”。
