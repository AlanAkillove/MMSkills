# 反例：理解未确认就跳到模型

团队还没有说明图中对象关系，`understanding_checkpoint` 为 `partial`；Agent 却根据一篇论文直接确定采用某优化模型，补写目标函数并开始运行代码。
