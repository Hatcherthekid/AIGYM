# 健身训练 Agent 当前架构（飞书 MVP）

> 更新：2026-03-22  
> 本文件描述当前真实架构，而不是未来完整系统。

## 一句话

`飞书 = 运行壳，OpenClaw = 对话与路由层，模型 = Kimi/GPT 可替换层，飞书多维表 = 当前运行时结构化真相层。`

## 当前层级

### 1. 用户层

- 飞书对话
- 飞书卡片
- 飞书日历
- 飞书文档

### 2. Agent 层

- OpenClaw 承接对话
- 顶层 router 只做意图识别、缺失字段判断、skill 选择
- 任务型 skills 执行训练业务动作
- 系统内置提交流程负责主真相提交与关键投影更新

### 3. 数据层

- 飞书多维表承接当前运行时真相
- 当前最少包含：
  - `sessions`
  - `sets`
  - `exercise_catalog`
  - `constraints`
  - `session_summaries`

### 4. 未来适配层

- `fitness-assistant/backend/` 保留为未来独立后端与 App 的适配层骨架
- 当前不是主运行路径

## 当前正式技能

- `start_session`
- `log_set`
- `bulk_ingest_workout`
- `amend_set`
- `swap_exercise`
- `suggest_next_set`
- `end_session`
- `query_context`
- `pre_workout_decision`
- `conditioning_protocol_adjust`

## 提交与投影分层

### 主真相层

- `sessions`
- `sets`
- `exercise_catalog`
- `constraints`

### 投影层

- `session_summaries`
- 飞书日历
- 飞书文档 / 展示视图

### 固定流程

1. skill 生成结构化结果
2. 系统提交主真相对象
3. 系统同步关键投影
4. 投影失败时标记 `pending_sync`

## 强约束

- prompt 不能记住 active session
- 聊天历史不能承担训练状态真相
- 图片识别不能直接入库
- 所有建议都必须基于结构化历史

## 当前不做

- 正式 App UI
- 训记级记录交互
- 独立数据库迁移
- 营养/热量体系

## 未来迁移方向

未来会做独立记录器 App。那时：

- App 承接高频训练记录
- 飞书承接计划、复盘、管理台和弱交互
- 当前 skill 协议与训练模型必须可复用
