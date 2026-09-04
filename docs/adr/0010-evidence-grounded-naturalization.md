# ADR 0010：证据约束的学术表达自然化

- 状态：accepted
- 日期：2026-09-04
- 适用版本：0.3.1

## 背景

0.3.0-rc2 冻结了三角色入口。写作链里仍有一部分“AI 味”判断来自经验清单（均匀三点式、长句、每段同节奏等）。公开项目 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone)（MIT）用对照语料推翻了多项流行判断，并强调白名单最小改写和作者风格优先。其语料不可核验，也不是数模论文，因此只借方法。

## 决策

1. 不新增 Skill，不复制对方 11 条规则或统计倍率，不输出 AI 分数或作者身份。
2. AI-pattern 信号拆成 evidence-backed / contextual / readability-only，并建立 negative-signal-registry。
3. Naturalizer 终稿精修默认 `signal-targeted`；`paragraph-rebuild` 仅在用户明确要求或结构层阅读问题时使用。
4. 风格基线优先序：用户指定 > 已确认章节 > 学科规范 > 通用规则；题意与证据仍最高。
5. `scan_language_signals.py` 只输出 `candidate`；preflight 视为 warning，不得阻断。

## 明确不做

新建 less-ai-tone Skill、训练检测器、按词频改写、把通用中文阈值硬套数模论文、把学术连接词改成口语。
