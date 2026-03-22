# Backend Skeleton

这个目录当前不是飞书 MVP 的线上主实现。

当前定位：

- 未来独立后端 / 独立记录器 App 的适配层骨架
- 仓库内协议与命名参考实现
- 为后续迁移飞书真相层提供落点

当前不应把这里理解为：

- 线上主数据库实现
- 当前 OpenClaw 真实运行逻辑
- 当前飞书同步系统

## 当前建议关注

- `services/command_router.py`
  - 任务型 skill 路由参考
- `services/projection_flow.py`
  - 系统内置提交/投影流程参考
- `api/training.py`
  - 未来训练 API 草图
- `api/webhooks.py`
  - 未来事件接入草图

## 当前设计真相

请优先阅读：

- `docs/product/fitness-assistant-prd.md`
- `docs/product/training-agent-skill-design.md`
- `prompts/`
- `schemas/`
