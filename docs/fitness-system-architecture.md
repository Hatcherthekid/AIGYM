# 健身训练系统架构说明（当前 MVP / 未来适配）

> 更新：2026-03-22

## 当前运行时架构

```
用户（飞书）
  -> OpenClaw
  -> router
  -> task skills
  -> 飞书多维表 / 日历 / 文档
```

当前没有独立后端主库。飞书多维表是运行时结构化真相层，但它只是 MVP 期间的承载方式。

## 未来目标架构

```
训练记录器 App / 飞书
  -> 共用训练内核
  -> 独立后端与主库
```

## 当前必须稳定的对象

- Session
- Set
- Exercise
- Constraint
- SessionSummary
- SourceArtifact

## 当前必须稳定的技能协议

- `start_session`
- `log_set`
- `amend_set`
- `swap_exercise`
- `suggest_next_set`
- `end_session`
- `query_context`
- `pre_workout_decision`
- `conditioning_protocol_adjust`

## 后端骨架的当前定位

`fitness-assistant/backend/` 不是线上主逻辑，而是未来 App / 后端迁移时的适配层参考实现。

它当前承担三种作用：

- 保留概念层目录与命名
- 为未来 API / 数据模型提供参考
- 作为仓库内协议草图，而不是生产真相
