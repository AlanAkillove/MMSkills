# 调研依据与迁移边界

访问日期：2026-08-31。以下资料用于提炼图表设计和工程 QA 原则，不等同于赛事规则，也不要求项目安装对应仓库。

| 来源 | 借鉴点 | 数模化改造 |
|---|---|---|
| [Yuan1z0825/nature-skills — nature-figure](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-figure) | 先写 figure contract；区分图表结论、证据层级、面板角色、源数据和可编辑输出；生成后再做一致性检查 | 不照搬 Nature 期刊版式、英文偏好或固定尺寸；加入题意锚点、模型/实验注册、中文标签、竞赛正文嵌入和人工确认 |
| [SciencePlots](https://github.com/garrettj403/SciencePlots) | 将样式参数分层管理；提供论文尺寸和色板参考；鼓励可复用的绘图配置 | 样式库是可选实现细节，不是审美标准；不允许用统一 style 覆盖不同证据角色或题目特征 |
| [academic-figure-patterns](https://github.com/taoge946/academic-figure-patterns) | 先考虑“展示什么、如何组织比较、标注怎样引导读者”，并提供误差、基线、排序和区间等叙事模式 | 将“内容先于样式”落实为数模的题面—模型—实验—主张链；注释数量按读者任务决定，不机械套用样例 |
| [figure-gate](https://github.com/narenp12/figure-gate) | 把色觉安全、构图和实际字号等问题转成失败明确的机械化 gate，并用失败测试和边界案例验证 | 本技能只做设计阶段自检；数据/数值/主张仍交给图表审计，避免把视觉 gate 当作科学正确性评分器 |
| [CMasher](https://github.com/1313e/CMasher) | 感知均匀和色觉友好的连续色带优于随意的彩虹色带 | 只借鉴色带选择原则；按数据语义选择顺序/发散/循环映射，不把色带库作为强依赖 |
| [Matplotlib colormap guide](https://matplotlib.org/stable/users/explain/colors/colormaps.html) 与 [seaborn color palettes](https://seaborn.pydata.org/tutorial/color_palettes.html) | 连续数据、发散数据和分类数据需要不同色彩语义；亮度/感知变化影响读数 | 将色彩检查与灰度、色觉差异、中文印刷和正文尺寸一起验证，禁止只凭屏幕观感 |
| [matplotlib_for_papers](https://github.com/jbmouret/matplotlib_for_papers) | 先确定尺寸/纵横比；控制字号、线宽和空白；删掉没有信息功能的图形元素 | 迁移到 A4/竞赛正文和中文字体；不追求“一种风格适用于全部图表” |

## 本技能的结论

1. 图表应从读者任务和证据角色出发，样式后置；
2. 美观首先是可读、可解释、可嵌入和可复核，其次才是风格偏好；
3. 图表设计需要反同质化检查，但差异来自题目和证据，不来自稀奇配色或生造术语；
4. 视觉 gate 能发现渲染缺陷，不能证明数据、模型和结论正确；
5. 任何模板、样式库和生成式图像都必须服从题意、数据和人工确认。
