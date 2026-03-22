# 健身训练 Agent Backlog

> 更新：2026-03-22  
> 原则：仓库文档优先，飞书/OpenClaw 后台配置随后对齐

## Now

| ID | 任务 | 入口 | 验收标准 | 状态 |
|---|---|---|---|---|
| N1 | 统一产品与架构文档真相 | `docs/product/fitness-assistant-prd.md`, `docs/ARCHITECTURE_SIMPLE.md`, `docs/fitness-system-architecture.md`, `docs/GITHUB_README.md` | 全部采用飞书 MVP + 可迁移训练内核口径 | done |
| N2 | 重写训练 skill 设计稿 | `docs/product/training-agent-skill-design.md` | 包含 9 个 skills、核心对象、图片导入约束 | done |
| N3 | 新增 router 与 skill prompts | `prompts/**` | router + 9 个 skill prompt 文件存在，内容独立 | done |
| N4 | 新增 schema 资产 | `schemas/**` | 核心对象与 skill I/O schema 可读可复用 | done |
| N5 | 新增 fixtures 资产 | `fixtures/**` | 至少包含真实对话样例、mock sessions、mock sets、图片导入候选 | done |
| N6 | 重定位 backend 骨架 | `fitness-assistant/backend/**` | README、router、API 文件明确为未来适配层/参考实现 | done |
| N7 | 线上配置对齐审计 | 飞书 / OpenClaw 后台 | 列出仓库与线上配置差异清单 | todo |
| N8 | Skill 与提交投影层分离 | `docs/product/training-agent-skill-design.md`, `schemas/skill-io.md`, `docs/reference/feishu-mapping.md` | 明确主真相表、投影表、系统内置提交流程 | done |
| N9 | 补批量导入能力设计 | `prompts/skills/bulk_ingest_workout.md`, `fixtures/bulk_ingest_candidates.json` | 新增 `bulk_ingest_workout` prompt 和批量导入 fixture | done |
| N10 | 补系统提交/投影参考骨架 | `fitness-assistant/backend/services/projection_flow.py` | 存在 commit / projection / pending_sync 参考流程 | done |
| N11 | 输出 OpenClaw 更新执行文档 | `docs/product/openclaw-update-playbook.md` | 能直接指导后台按仓库定义更新 router / skills / 映射规则 | done |

## Next

| ID | 任务 | 入口 | 验收标准 | 状态 |
|---|---|---|---|---|
| X1 | 实现 `start_session` 真实配置 | OpenClaw skill 配置 | 能创建/更新 active session | todo |
| X2 | 实现 `log_set` 真实配置 | OpenClaw skill 配置 | 文本记录能稳定落到 set 级对象 | todo |
| X3 | 实现 `amend_set` 真实配置 | OpenClaw skill 配置 | 修改/删除一组可精确命中 | todo |
| X4 | 图片导入确认流程 | 飞书卡片 + skill | 图片不能直接入库，必须确认 | todo |
| X5 | `swap_exercise` / `suggest_next_set` | OpenClaw skills | 能基于约束和历史给训练中调整 | todo |
| X6 | 按执行文档更新 OpenClaw 后台 | `docs/product/openclaw-update-playbook.md` | Router 和 4 个核心 skill 与仓库定义一致 | todo |

## Later

| ID | 任务 | 入口 | 验收标准 | 状态 |
|---|---|---|---|---|
| L1 | 飞书日历映射 | 飞书日历 | session 级训练安排可同步 | todo |
| L2 | Session summary 文档输出 | 飞书文档 | 每次训练结束能生成短复盘 | todo |
| L3 | 训练周边决策 skills 完整化 | `pre_workout_decision`, `conditioning_protocol_adjust` | 高饥饿场景和有氧协议场景可稳定运行 | todo |
| L4 | 独立记录器 App 内核梳理 | docs / schema | 形成 App 可复用的接口与状态机 | todo |
| L5 | 后端主库迁移评估 | `fitness-assistant/backend/` | 明确从飞书真相层迁出条件 | todo |
