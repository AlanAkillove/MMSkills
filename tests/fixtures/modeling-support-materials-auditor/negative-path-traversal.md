# 脱敏反例：压缩包路径风险

ZIP 中包含 `../../AppData/result.csv`、绝对路径 `C:\Users\name\secret.txt`、符号链接和高压缩比嵌套包。Agent 准备直接解压到项目目录覆盖同名文件。
