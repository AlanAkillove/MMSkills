# 制作、渲染与交接

## 生产顺序

```text
设计简报
  -> 选图与故事板
  -> 数据/转换固定
  -> 绘图代码或可编辑结构图
  -> 矢量/预览导出
  -> 目标页面渲染
  -> 视觉自检
  -> 图表事实审计
  -> 正文阅读体验回归
  -> 人工确认与冻结
```

图表的 `source_data_ids`、`source_code_entry`、`input_manifest_hash` 和 `output_hashes` 随版本传递。重绘不覆盖旧输出；旧图若仍被正文引用，先标记 `superseded` 并更新交叉引用。

## 定量图生产清单

- 从结构化数据或实验输出读取，不从截图或复制粘贴的手工表格读取；
- 把筛选、排序、聚合、归一化、单位换算、插值和舍入写进代码/日志；
- 记录数据版本、代码版本、环境、随机种子、命令和输出 hash；
- 将基线、误差、缺失、不可行区、失败结果和范围按事实显示；
- 使用明确的颜色/线型/标记映射，图例和图注与术语账本一致；
- 保存可运行脚本和最小重现入口，不把手工图像编辑作为数字修改层。

## 结构图生产清单

- 先列节点、关系、输入、输出、方向、循环和决策点；
- 每个箭头有语义：数据流、控制流、约束、依赖或几何关系不能混用；
- 层级和布局由关系决定，避免所有节点等大、箭头交叉和装饰性图标；
- 优先保存 SVG/PDF、draw.io/Graphviz/Mermaid 或其他可编辑源；
- 图中出现的简称、变量和符号必须进入术语账本或图注；
- 如果结构尚未由人确认，状态只能是 `needs_human_confirmation`。

## 最小视觉自检

在目标页面/尺寸下记录：

```text
render_tool_and_version:
target_page_or_width:
font_check: pass | fail | unknown
label_and_unit_check: pass | fail | unknown
legend_and_encoding_check: pass | fail | unknown
grayscale_or_color_vision_check: pass | fail | not_applicable | unknown
crop_overlap_overflow: pass | fail | unknown
panel_roles_non_redundant: pass | fail | unknown
page_render_status: checked | unassessed
open_items: []
```

这一步只检查设计和渲染表现，不把 `pass` 解读成数据正确或主张成立。

## 下游路由

| 发现 | 路由 | 处理边界 |
|---|---|---|
| 数字、单位、筛选、来源或图注不一致 | `modeling-figure-table-auditor` | 回查数据/代码/主张，不以配色修复 |
| 图表不能支撑结论或暗示因果/最优 | `modeling-claim-evidence-audit` | 限缩主张或补验证，由人决定 |
| 图例、图注、术语和正文读起来费劲 | `modeling-reader-experience-auditor` / `modeling-terminology-auditor` | 优先删冗余、补定义、调整顺序 |
| 结构像通用模板，题目对象被抹平 | `modeling-anti-homogenization-auditor` | 回到题目锚点和真实决策，不用奇怪样式制造差异 |
| 页面裁切、字体、跨页或文件格式问题 | `modeling-final-preflight` | 按目标赛事 profile 和实际渲染件处理 |

## 不确定状态

- 没有源数据：`source_data_ids: []`，定量值为 `unknown`；
- 只有 PNG/JPG：可检查布局和文字，精确数据/转换/来源为 `unknown`；
- 没有目标页面渲染：`page_render_status: unassessed`；
- 颜色语义或关键标注未被人确认：`human_status: needs-confirmation`；
- 找不到生成代码：交付可视源，但把 `source_code_entry` 记为 `missing`，不能声称可复现。
