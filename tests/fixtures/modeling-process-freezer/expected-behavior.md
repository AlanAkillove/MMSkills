# Expected behavior

1. working/reviewable/blocked 可以保存快照，但只有符合签核门才能标为 frozen/released。
2. 文件改动、规则/术语/证据/决定变化后，旧快照必须失效并创建新快照，不能保留旧 hash。
3. manifest 路径必须是根目录内的相对 POSIX 路径；默认不纳入 .git、缓存、临时物和 raw 会话。
4. hash 证明字节一致，不证明数学正确、实验充分或赛事合规。
5. handoff 先给状态、证据路径、未决问题和下一步；摘要不能替代原始材料。
