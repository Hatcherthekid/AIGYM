# 健身训练 Agent 迭代日志

> 更新：2026-03-22

## Iteration 0：文档初建 ✅

### Goal
- 建立 PRD、架构文档、Backlog、决策记录

### Done
- 初始产品文档完成
- 后端骨架初始化

### Verification
- `docs/product/` 下核心文档存在

### Next
- 收敛真实 MVP 架构

---

## Iteration 1：从“飞书机器人”收敛为“训练内核 + 飞书 MVP” 🔄

### Goal
1. 统一仓库里的架构与产品真相
2. 明确训练内核、skill 边界和图片导入约束
3. 重定位后端骨架

### Done
- 重写 PRD 与架构文档为统一口径
- 重写训练 skill 设计稿
- 将仓库定义为唯一设计真相
- 新增 `prompts/` 与 9 个 skill prompt
- 新增 `schemas/` 与 `fixtures/`
- 重定位 backend 骨架为未来适配层
- 将用户层 skill 与系统提交/投影流程分开
- 新增 `bulk_ingest_workout` 能力设计
- 新增 OpenClaw 更新执行手册，作为线上配置对齐入口

### Verification
- PRD / 架构文档 / README 对 source of truth 的叙述一致
- 训练 skill 设计稿中包含 10 个正式 skills（含 `bulk_ingest_workout`）
- `prompts/skills/` 下存在 9 个 skill prompt
- `schemas/` 与 `fixtures/` 目录存在且有基础资产
- `backend/README.md`、`api/training.py`、`api/webhooks.py`、`services/command_router.py` 已改为未来适配层口径
- `skill-io.md` 和 `feishu-mapping.md` 已写明主真相表 vs 投影表约束
- `openclaw-update-playbook.md` 已写明更新顺序、读取文件优先级、OpenClaw 配置边界

### Not done
- 线上飞书/OpenClaw 配置尚未审计
- `database.py` / `models/training.py` / `main.py` 仍保留旧骨架命名，后续可继续清理

### Next
1. 做线上飞书/OpenClaw 配置对齐审计
2. 按执行手册把 `start_session / log_set / amend_set / bulk_ingest_workout` 先映射到真实运行配置
3. 继续清理 backend 剩余旧命名与说明
