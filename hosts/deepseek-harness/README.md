# DeepSeek Harness 薄适配

这是可选宿主适配（`native-adapter`），不是第二条架构。Codex / 标准 `skills/` 仍是源文件。DSH 只需要能发现 `SKILL.md` 并解析相对链接。

不要把 DSH 专用 frontmatter、工具名或 Workbench API 写回 `skills/`。

## 何时使用

当前会话跑在 DeepSeek Harness，且它从某个目录扫描 skill 文件系统时。平时用 Codex 不必生成适配目录。

## 怎么装

在仓库根目录：

```text
python hosts/deepseek-harness/sync_adapter.py --target .agents
```

它会把 `skills/` 以及 `references/`、`schemas/`、`templates/`、`profiles/`、`docs/` 镜像到目标目录，并写入 `source-manifest.yaml`。相对链接（`../../schemas`、`../modeling-literature-evidence/...`）保持原样，不改写 SKILL 正文。

`.agents/` 是派生产物，已列入 `.gitignore`。回滚：删掉该目录。上游 `skills/` 不会被修改。

## 运行约定

适配器会镜像整个 `skills/` 树，以便 specialist 的相对链接仍然有效。`source-manifest.yaml` 的 `default_entry` 是 `math-modeling`，但这**不是** Harness 级强制：适配器本身不能阻止宿主把全部 specialist 列给模型。若 DSH 会把 28 个 Skill 都暴露给模型，顶层认知复杂度仍需在会话里遵守“只加载 math-modeling + 一个角色”。copied ≠ discovered/activated/verified。

脚本按上游仓库根目录执行，例如：

```text
python skills/modeling-tex-paper-production/scripts/check_pdf_visual.py paper.pdf
```

不要把这些命令改写成适配器内部路径后再写回源 skill。

缺 DSH 宿主时，兼容性状态是 `optional` / `not_run`，不阻挡 Codex 发布。

安装时仍按 [跨 Agent 安装教程](../../docs/agent-skill-installation.md) 报告 copied / discovered / activated / verified；镜像存在不等于已经激活。
