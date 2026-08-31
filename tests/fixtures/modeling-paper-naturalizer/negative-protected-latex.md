# 脱敏反例：受保护的 LaTeX

```latex
由式 \ref{eq:flow} 可得，$x_i\ge 0$。见图 \ref{fig:network}，相关数据来自 \cite{smith2024}。
\begin{equation}\label{eq:flow}
  \sum_i x_i = Q
\end{equation}
```

自然化只能修改命令外的人类可读文字，不能改动命令、标签、引用键和公式。
