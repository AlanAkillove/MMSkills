# 期望行为（非固定措辞测试）

- CUMCM 正例：记录官方来源、适用年份、AI/格式/保密/支撑材料字段和人工确认状态；
- 本地 PDF：保留 hash、页码、文本/视觉交叉核验，不能把抽取乱码当原文；
- 年份缺失：P0/blocked，不能默认 CUMCM 2026；
- 搜索摘要：只能作为线索，状态 `unknown`，要求打开官方正文；
- 跨赛事复制：拒绝套用，要求目标赛事官方来源；
- 来源冲突：保留双方 source ID、适用范围和问题，状态 `conflict`，不选最严格/最宽松；
- 旧版 profile：标 `stale`，重新核验后才能 verified；
- 任何 unknown/conflict/stale 未关闭时不能做正式合规保证；
- 每条规则要有来源 ID、发布日期/访问日期、hash 和页码/条款/行号 evidence anchor。
