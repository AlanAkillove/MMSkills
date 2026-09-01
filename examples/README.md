# Examples

这些文件是说明材料，不是默认运行入口。

- `generic-paper-scaffold.tex`：一份可选的数模论文章节示例。真正的排版模板是 `templates/tex/main.tex`，其中正文通过 `\input{body.tex}` 引入，不预装固定章节。
- `cumcm-appendix.tex`：CUMCM 常用的复现入口/支撑材料清单示例。默认 `main.tex` 不包含这些内容章节；需要时打开 `\mmIncludeAppendix` 再按项目改写。
