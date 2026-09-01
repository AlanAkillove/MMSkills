# 图表设计的推荐工作流

本文件是按需读取的详细协议，不是每轮必须执行的 SOP。用户只要修一张已有图或导出问题时，先处理该局部。

## 工作模式

`brief`、`plot`、`redesign`、`assemble`、`diagram`、`handoff`。

## 需要完整制作时的顺序

1. 写图表契约：读者任务、主张、数据和正文位置。
2. 按变量关系选图，并记录不选相邻候选的理由。
3. 多面板只保留互补角色，避免重复同一结果。
4. 在目标页面尺寸上设置字体、线宽、颜色语义和灰度通道。
5. 代码优先生成，定量图保留脚本和输入。
6. 插入正文或按目标尺寸渲染后再检查可读性。

## 需要落盘时的最低交付

`figure_design_brief.md`、`figure_storyboard.md`、`figure_design_manifest.yaml`，以及 `plot/`、`source/`、`render/`。数据事实交给 `modeling-figure-table-auditor`。
