# Iteration & Solo PM Rules（迭代日志与个人项目管理）

> 适用于：个人迭代记录、Roadmap、Backlog、决策记录（ADR-lite）
> 目标：用最小的"项目管理"成本，换取可复盘与低返工

---

## Must（必须）

### 1) 每次迭代必须有"迭代日志"（Iteration Log）

- **ZH**：每次迭代（不管大小）都写一个最小日志条目，包含：
  - **Goal**：本次要达成的目标（1–3 条）
  - **Done**：完成了什么（要能指向代码/页面/数据产物）
  - **Not done**：没做完的点 + 原因（1–3 条即可）
  - **Verification**：怎么验证（命令/页面路径 + 预期结果）
  - **Next**：下一步（1–3 条）
- **EN**：Every iteration must record goal, done/not-done, verification, and next steps.

### 2) Backlog 必须"可执行 + 可验收"（Actionable & Verifiable）

- **ZH**：Backlog 的每一项必须能回答：
  - 做完是什么样（验收条件）
  - 入口在哪（页面/脚本/文件路径）
- **EN**：Each backlog item must have acceptance and an entrypoint.

### 3) 重要决策必须留痕（ADR-lite）

- **ZH**：当你做出会影响长期维护/成本的决策时，至少记录一条：
  - 问题（Problem）
  - 选择（Decision）
  - 理由（Rationale）
  - 代价（Trade-offs）
- **EN**：Record problem/decision/rationale/trade-offs for major decisions.

---

## Should（建议）

- **ZH**：Roadmap 用 3–8 个"主题"（Themes）即可，按 `Now / Next / Later` 三段；不要写到任务粒度。
- **EN**：Keep roadmap theme-based (Now/Next/Later); avoid task-level detail.

- **ZH**：每次迭代结束，做一次 2 分钟复盘：保留 1 条"这次学到了什么/下次避免什么"。
- **EN**：Add one short retrospective note per iteration.

---

## Avoid（避免 / 禁止）

- **ZH**：不要引入团队仪式（Sprint 计划会、评审会、站会模板）来写给自己看；你需要的是"可执行清单 + 可复盘记录"。
- **EN**：Avoid team ceremony; optimize for execution and review.

- **ZH**：不要把迭代日志写成流水账；聚焦"目标-结果-验证-下一步"。
- **EN**：Avoid diary-style logs; focus on outcomes and verification.

---

## Acceptance（验收 / Self-check）

- **ZH/EN**：
  - 迭代日志条目包含 Goal/Done/Verification/Next
  - Backlog 条目具备验收条件与入口
  - 关键决策有 ADR-lite 记录（Problem/Decision/Rationale/Trade-offs）
