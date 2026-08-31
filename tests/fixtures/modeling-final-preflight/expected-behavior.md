# 期望行为（非固定措辞测试）

- 待签核正例：overall_status=`needs-human-signoff`，不是合规保证；
- 冻结正例：P0/P1 清零、P2/P3 有风险接受、输入/输出 hash 和签核齐全才可 `frozen`；
- 过期 profile：`blocked` 或 `unknown`，不能 ready；
- 主张 P1：整体 `blocked`，不能用格式通过抵消；
- 无渲染件：视觉检查 `unknown/unassessed`，不能写页面通过；
- AI 披露：缺版本/采纳/核验/人工确认时阻断，不能从成品反推；
- 支撑身份：P0/P1，按规则阻断并只报告最小必要信息；
- 版本冲突：整体 `blocked`，保留各 hash，不选择更好看的版本；
- 不输出通过率、AI 率、原创度、获奖概率或官方合规保证。
