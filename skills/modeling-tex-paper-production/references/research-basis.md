# 研究依据与迁移边界

本技能参考官方赛事文件和公开开源 TeX 实践，但不把开源模板的默认样式当作赛事规范。

## 官方规则与模板实践

- CUMCM 官方《论文格式规范（2026 年修订稿）》：A4 与最小页边距、摘要首页、电子版去除承诺书/编号页、正文 30 页、附录和支撑材料、匿名与引用要求；未统一指定字号、字体、行距、颜色。来源：[mcm.edu.cn](https://www.mcm.edu.cn/html_cn/node/4cd596519c9eb9fbd866398f6df0caa3.html)。
- CUMCM 官方《人工智能工具使用规定（2026 年试行）》：声明位置、详情 PDF 字段和核心建模由队伍主导。来源：[mcm.edu.cn](https://www.mcm.edu.cn/html_cn/node/fef94648f2836ab6cc81586f4c38512b.html)。
- COMAP MCM/ICM 官方 instructions：Summary Sheet、目录、正文组织、页眉控制号、英文可读字号、匿名、页数和提交 PDF。来源：[contest.comap.com](https://www.contest.comap.com/undergraduate/contests/mcm/instructions.html)。
- COMAP 官方 AI Policy：透明披露、引用、核验和 AI report 的指导。来源：[Contest_AI_Policy.pdf](https://www.contest.comap.com/undergraduate/contests/mcm/flyer/Contest_AI_Policy.pdf)。
- MathorCup 官方公开历史格式页：第一页摘要、第二页目录、无页眉、中文和约 30 页等届次特定要求。来源：[mathorcup.org](https://www.mathorcup.org/detail/2414)。
- 中国研究生数学建模竞赛官方平台通知：必须使用当届官方模板、封皮和统一摘要页的实例。来源：[cpipc.acge.org.cn](https://cpipc.acge.org.cn/cw/contestNews/detail/4/2c90801b9914a68201994b1403512e96?page=1)。

## 开源实践

- [`latexstudio/CUMCMThesis`](https://github.com/latexstudio/CUMCMThesis)：将 CUMCM 版式集中到文档类，并明确 `withoutpreface`、`bwprint` 等选项；可借鉴结构化 class 思路，但不能把旧 class 的承诺书、编号页和字体路径复制给其他赛事。
- [`gbt7714-bibtex-style`](https://github.com/zepinglee/gbt7714-bibtex-style)：GB/T 7714-2015 BibTeX 样式和 LPPL 许可信息；可在许可、发行版和目标规范都确认后使用，不在本项目仓库无声明地复制 `.bst`。
- [`harveymuddcollege/icmmcm`](https://github.com/harveymuddcollege/icmmcm)：面向 MCM/ICM 的独立 class 与空白模板；可借鉴将控制号、Summary Sheet、正文和页码作为配置的思路，不替代 COMAP 当届文件。
- [`latexstudio-org/mcmthesis`](https://ctan.org/pkg/mcmthesis)：面向 MCM/ICM 的 CTAN 文档类实践；借鉴“随发行版管理依赖、提供文档和样例”的工程方式，不直接搬运代码或固定外观。

## 本项目的选择

本项目不随通用模板分发 `cumcmthesis.cls`、字体、Logo 或其他许可证/版本不明的第三方二进制资源，而采用 `ctexart` + 明确宏包依赖的中性骨架。这样用户可在官方模板、赛事专用 class 和中性模板之间作出可审计的选择；需要第三方 class 时，skill 要求记录来源、许可、版本和人工确认。

本技能的质量目标是“语义不变、页面可读、来源可追、规则可适配”，不是“更像某个获奖模板”、不是 AI 检测分数，也不是固定的竞赛获奖保证。
