# PRD Policy（需求文档规则）

> 适用于：PRD、需求设计、功能规格类文档
> 本仓库推荐放置：`docs/product/**`

---

## Must（必须）

### 1) PRD 最小字段（独立开发者版）

PRD 必须包含：
- 背景与目标（含非目标）
- 目标用户与核心场景
- 需求范围与边界（Scope / Out of scope）
- 方案概要与关键流程（信息架构/交互步骤）
- 验收标准（可测试、可观察）
- 风险与未决问题（含验证计划）
- 任务 checklist（每条可执行、可验收）

### 2) Checklist 规则

- **ZH**：每条任务必须：
  - 可执行（有明确改动对象/入口）
  - 可验证（有可观察结果或命令/页面路径）
  - 有状态（`todo / doing / done / blocked` 之一）
- **EN**：Tasks must be executable, verifiable, and status-tracked.

### 3) 进入开发的质量门槛（自检）

必须满足：
- 目标/范围/验收明确
- 关键流程已描述（至少 1 条主流程）
- 风险已识别（可先作为未决项）
- 与现有架构/分层冲突已评估
- checklist 已建立

不满足则退回补齐，不进入开发。

### 4) 更新触发

- **ZH**：范围/验收/关键流程变化必须更新 PRD，并同步调整 checklist（不另起漂移文档）。
- **EN**：When scope/acceptance/flows change, update PRD + checklist.

---

## Should（建议）

- **ZH**：用"默认值 + 可选增强"写方案，先把 MVP 交付闭环跑通。
- **EN**：Prefer MVP-first with defaults.

- **ZH**：对关键指标写口径（例如：移动端首屏内容长度、详情页点击率、索引页收录/CTR）。
- **EN**：Define metric definitions when relevant.

---

## Avoid（避免 / 禁止）

- **ZH**：避免抽象任务（如"优化体验/提升 SEO"）；必须写到"改哪块、怎么验收"。
- **EN**：Avoid vague tasks; make them testable.

---

## Acceptance（验收 / Self-check）

- **ZH/EN**：PRD 能在 2 分钟内回答：
  - 要解决什么问题？目标是什么？
  - 做哪些、不做哪些？
  - 用户怎么走完整流程？
  - 做完怎么验收？
  - 有哪些风险/未决项？
  - 下一步任务是什么、状态是什么？
