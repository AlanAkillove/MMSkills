# modeling-process-freezer fixtures

这些文本描述虚构项目状态，只验证快照和续接规则。哈希脚本测试会在临时目录中创建文件，不读取或覆盖真实项目材料。

- positive-freeze：有父谱系、人工决定和文件 hash 的阶段冻结；
- negative-unsigned-freeze：没有人工签核却声称 frozen；
- negative-stale-hash：文件修改后仍沿用旧 hash；
- negative-unsafe-path：manifest 用绝对路径或 .. 指向项目外；
- negative-state-regression：把 frozen 直接覆盖成 working，未保留新快照和差异。
