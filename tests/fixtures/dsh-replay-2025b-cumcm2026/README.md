# Sanitized regression from a 2025 CUMCM-B replay written under 2026 rules

This fixture encodes observable failure modes from a live DeepSeek Harness run.
It is not the original session, PDF, or team manuscript. Do not treat numbers
or citations as scientific results.

Expected mechanical findings under `cumcm-natural-cn` + `cumcm-2026`:

- wrong-rules-year-page-limit (`<= 20` while official limit is 30)
- english-abstract-forbidden
- boxed-equation
- unordered-list-forbidden
- orphan-bibliography (`\\bibitem` without `\\cite`)
- coverage-short when `--pdf-pages 11`
- problem-restatement-section (`\\section{问题重述}`)
