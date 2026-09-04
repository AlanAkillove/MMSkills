# TeX 使用说明

仓库提供一份中性 TeX 骨架，用于组织已确认的论文内容，并按目标赛事配置做机械排版。它不是任何赛事的官方模板。

## 模板在哪里

入口在 [`templates/tex/`](../templates/tex/README.md)：

- `main.tex`：排版入口
- `body.tex`：正文，默认留空
- `references.bib`：空引用库
- `latexmkrc`：XeLaTeX 配置
- `tex-format-profile.example.yaml`：赛事格式记录示例
- `tex_build_manifest.example.yaml`：构建记录示例
- `tex_layout_audit.example.md`：版式抽查示例

专项技能是 [`modeling-tex-paper-production`](../skills/modeling-tex-paper-production/SKILL.md)。赛事差异见 [`format-profile-map.md`](../skills/modeling-tex-paper-production/references/format-profile-map.md)。CUMCM 附录清单示例见 `examples/cumcm-appendix.tex`。

## 怎么编译

复制整个 `templates/tex/` 到项目工作区后：

```text
latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
```

机械模板检查：

```text
python skills/modeling-tex-paper-production/scripts/check_tex_template.py templates/tex/main.tex
```

编译成功只说明 TeX 语法可处理，不说明模型、数据、引用、匿名或赛事提交已经合规。

## 哪些开关可用

```tex
\mmIncludeContentsfalse       % 要求目录的赛事才开启
\mmIncludeAIStatementfalse   % 规则与真实使用记录均确认后才开启
\mmIncludeCodeAppendixfalse  % 规则要求且篇幅允许时才开启
\mmShowHeaderfalse           % 规则要求控制号或页眉时才开启
\mmIncludeBibliographyfalse  % 有已核验且实际引用的来源后才开启
\mmIncludeAppendixfalse      % 需要附录内容时才开启
```

开关只改变机械排版。目录、页眉、AI 声明和页数是否合规，仍由目标赛事配置决定。

## 如何应用比赛配置

1. 先读取目标赛事、年份和官方模板；官方模板优先于本仓库骨架。
2. 用规则配置记录引擎、纸张、首页、目录、页眉、页数、附录、匿名和 AI 声明。
3. 再改 `main.tex` 开头的开关。不要把某一赛事的默认值复制给其他赛事。
4. 图表使用相对路径；不要把本机绝对路径写入源稿。

中性默认值是 A4、四边 2.5 cm、摘要先行、页脚页码、无目录和无页眉。这些默认值不等于赛事要求。

## 如何做 PDF 检查

```text
python skills/modeling-tex-paper-production/scripts/check_pdf_visual.py paper.pdf --paper a4
```

至少抽查摘要页、公式页、密集图表页、参考文献页和附录页。空白页、非预期纸张、本地路径和身份元数据由脚本报告。中文被抽成乱码时，以渲染检查为准，不要把抽取文本当成原文。
