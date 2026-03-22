# 健身训练 Agent 设计稿（飞书 MVP / 可迁移内核）

> 状态：active  
> 更新：2026-03-22

## 1. 设计目标

这份文档定义当前飞书 MVP 的训练内核、skill 边界和数据模型。

核心判断：

- 飞书只是当前运行壳
- 训练内核要为未来独立记录器 App 预埋
- 记录可靠优先于交互顺手
- agent 需要更聪明，但不能靠 prompt 硬记状态

## 2. 核心对象

### `Session`
- 一次训练会话
- 同时只能有一个 `active session`

### `Set`
- 一组训练表现
- 一组一对象，不打包成 JSON 大字段

### `Exercise`
- 标准动作实体
- 支撑动作归一、历史聚合、替代动作

### `Constraint`
- 当前限制条件
- 包含伤病、器械限制、时间限制、疲劳状态

### `SessionSummary`
- 训练结束后的短复盘

### `SourceArtifact`
- 图片、截图、设备屏幕、文本来源
- 导入候选先落这里，再确认是否转正式记录

## 3. 状态定义

### SessionStatus

- `draft`
- `active`
- `paused`
- `completed`
- `cancelled`

### ImportStatus

- `pending_review`
- `confirmed`
- `rejected`

## 4. 当前飞书表映射

当前阶段最少映射 5 张表：

1. `sessions`
2. `sets`
3. `exercise_catalog`
4. `constraints`
5. `session_summaries`

### 运行原则

- 飞书表是当前运行时真相层
- 但模型定义以仓库文档和 schema 为准
- 日历只承接 session 级信息
- 文档只消费 summary 级信息

## 5. Router 设计

顶层 `router` 只做四件事：

1. 识别意图
2. 判断是否缺少关键字段
3. 选择 skill
4. 输出固定参数结构

Router 不做：

- 不记长期状态
- 不自己回答复杂训练问题
- 不跳过 skill 直接脑补历史

## 6. Skills

### `start_session`
- 用途：开始训练 / 今天练什么
- 输入：focus、goal、available_minutes、constraints
- 输出：session 草案、plan_items

### `log_set`
- 用途：记录一组
- 输入：exercise_raw、weight、reps、rpe、note、source
- 输出：结构化 set、置信度、是否需确认

### `bulk_ingest_workout`
- 用途：一次导入多动作、多组训练记录
- 输入：source_artifact_id、candidate_entries、confirmation_mode、confirmed_entries
- 输出：候选 workout payload、确认结果、待提交主对象列表
- 说明：它只负责批量导入候选与确认，不直接承担 summary / 日历更新

### `amend_set`
- 用途：改一组 / 删一组
- 输入：target_set_id 或定位条件、operation、updated_fields
- 输出：修改结果

### `swap_exercise`
- 用途：器械限制 / 疼痛 / 时间不足时换动作
- 输入：original_exercise、constraints、session_state
- 输出：替代动作、原因、回归门槛

### `suggest_next_set`
- 用途：下一组建议
- 输入：current_set_feedback、recent_sets、history_context
- 输出：加减重/次数/节奏建议

### `end_session`
- 用途：结束训练
- 输入：session_id、completed_sets、risk_feedback
- 输出：短复盘、收尾建议、下次调整

### `query_context`
- 用途：查历史、查 active session、查某动作上下文
- 输入：query_type、filters
- 输出：结构化历史摘要

### `pre_workout_decision`
- 用途：训练前补给/是否开练
- 输入：hunger_level、time_to_train、goal_hint
- 输出：建议先吃还是先练、推荐补给、等待窗口

### `conditioning_protocol_adjust`
- 用途：4x4 / Zone2 等协议调参
- 输入：protocol_type、current_metrics、feedback
- 输出：配速/心率/spm 调整建议和 guardrails

## 7. 用户层 Skill 与系统提交流程

当前阶段必须把“用户可见能力”和“数据一致性流程”分开。

### 7.1 用户层 Skills

用户层 skills 负责：

- 理解意图
- 组织上下文
- 生成结构化结果
- 决定要写哪些主真相对象

用户层 skills 不负责：

- 逐个更新 summary、日历、文档
- 自己兜底所有跨表同步

### 7.2 系统内置提交流程

每个会产生写操作的 skill，在得到结构化结果后，都要进入固定的系统流程：

1. `commit_main_entities`
   - 先写主真相对象
2. `run_projections`
   - 再同步关键投影
3. `mark_pending_sync_if_failed`
   - 投影失败时标记 `pending_sync`

### 7.3 主真相层

- `sessions`
- `sets`
- `exercise_catalog`
- `constraints`

### 7.4 投影层

- `session_summaries`
- 飞书日历
- 飞书文档 / 展示视图

### 7.5 固定原则

- skill 只允许直接写主真相对象
- 投影层只能由系统内置提交流程更新
- 投影失败不回滚主真相写入
- 但必须显式返回 `pending_sync`

## 8. 图片导入硬约束

- 图片识别结果不能直接写入正式 `Set`
- 必须先形成候选导入对象
- 以下情况默认要求确认：
  - 动作名置信度低
  - 重量或次数异常
- 识别出与当前训练 focus 明显冲突的动作
- 禁止模型补齐图里不存在的重量、次数、动作

## 9. 输出风格约束

训练场景输出必须短、可执行。

默认形式：

- 一句话结论
- 3 到 5 条下一步
- 必要时给红线或回退路径

避免：

- 长篇解释
- 没有依据的鼓励
- 模糊建议

## 10. 当前阶段的优先级

第一优先级：

- `log_set`
- `amend_set`
- `bulk_ingest_workout`
- 图片导入确认机制

第二优先级：

- `start_session`
- `query_context`

第三优先级：

- `swap_exercise`
- `suggest_next_set`
- `end_session`

第四优先级：

- `pre_workout_decision`
- `conditioning_protocol_adjust`
