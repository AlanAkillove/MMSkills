# 阻断与签核

## 总体状态规则

```text
若存在 P0/P1 fail 或 blocked -> overall_status=blocked
否则若存在 unknown/conflict/stale 或未完成人工确认 -> needs-human-signoff
否则若机械/专项检查完成但未签核 -> ready-for-human-submission
签核后固定全部输入/输出 hash -> frozen
```

`frozen` 只表示团队冻结该版本；不表示组委会接受、奖项资格或内容绝对正确。

## 签核事项

团队至少确认：

1. 目标赛事/版本/profile 与附加规则；
2. 题意、关键假设、模型取舍、数据处理和实验解释；
3. 主张、数字、公式、图表、引用、局限和支撑材料；
4. AI 使用事实、详情、声明、人工修改/核验和未知项；
5. 身份/隐私/版权、代码执行范围、风险接受和最终文件；
6. 签核人、日期、范围、决定 ID 和版本/hash。

## 风险接受

对 P2/P3 可以记录 `accepted-risk`，但必须写理由、影响、确认人和 decision ID；P0/P1 不能用风险接受伪装成通过。任何冻结后修改生成新 release，不覆盖旧 manifest。
