# OpenClaw 更新执行手册

> 更新：2026-03-22  
> 目的：让 OpenClaw 或协作者按仓库中的设计真相，更新飞书里的训练 Agent 配置。

## 这份文档是干什么的

这不是 PRD，也不是后端开发文档。  
这份文档只回答两件事：

1. 仓库里这轮已经改了什么
2. OpenClaw 后台接下来应该怎么更新

如果要同步飞书/OpenClaw 配置，以这份文档和仓库里的 `prompts/`、`schemas/`、`docs/product/` 为准，不要再按旧的万能 prompt 或旧的后端想象来配。

## 当前仓库已经完成的重构

### 1. 统一了系统定位

现在这套系统的真实定位是：

- 飞书：运行壳、表格、日历、文档
- OpenClaw：对话入口、router、skill 调用
- Kimi / GPT：可替换模型层
- 飞书多维表：当前运行时结构化真相层
- 仓库文档：唯一设计真相
- `fitness-assistant/backend/`：未来适配层骨架，不是当前主运行路径

### 2. 训练能力被收敛成 task skills

当前正式技能集为：

- `start_session`
- `log_set`
- `amend_set`
- `swap_exercise`
- `suggest_next_set`
- `end_session`
- `query_context`
- `pre_workout_decision`
- `conditioning_protocol_adjust`
- `bulk_ingest_workout`

这些 skill 的定义在：

- `docs/product/training-agent-skill-design.md`
- `prompts/router.md`
- `prompts/skills/*.md`
- `schemas/skill-io.md`

### 3. 训练核心对象已经固定

当前训练内核固定为：

- `Session`
- `Set`
- `Exercise`
- `Constraint`
- `SessionSummary`
- `SourceArtifact`

核心规则：

- 同时只能有一个 `active session`
- 一组训练必须独立成对象
- 图片/截图先形成候选导入对象，确认后才能写正式记录
- 所有建议必须引用结构化历史，不能靠聊天记录脑补

详细定义在：

- `schemas/core-models.md`

### 4. Skill 层和提交投影层已经分开

用户可见能力继续由 skills 负责。  
数据一致性不再交给 skill 或 prompt 自己兜底，而是由系统内置提交流程负责。

固定流程：

1. `commit_main_entities`
2. `run_projections`
3. `mark_pending_sync_if_failed`

主真相层：

- `sessions`
- `sets`
- `exercise_catalog`
- `constraints`

投影层：

- `session_summaries`
- 飞书日历
- 飞书文档 / 展示视图

约束：

- skill 只允许直接写主真相对象
- `session_summaries`、日历、文档只能由投影流程更新
- 投影失败时，不回滚主真相写入，但必须标记 `pending_sync`

详情见：

- `docs/product/training-agent-skill-design.md`
- `schemas/skill-io.md`
- `docs/reference/feishu-mapping.md`

## OpenClaw 更新时必须遵守的原则

### 1. 不要再用一个万能 prompt 覆盖所有能力

OpenClaw 里必须采用：

- 一个 `router`
- 多个 task skill

不要继续使用“训练师/康复师/顾问”这种人格型拆分来代替 skill 边界。

### 2. Prompt 不能承担长期记忆

不要让 prompt：

- 记住 active session
- 自己猜历史训练
- 用聊天记录推断数据真相

训练状态、记录、限制条件，都应该来自飞书表中的结构化对象。

### 3. 图片导入必须是候选确认流程

任何截图、图片、批量导入输入：

- 不得直接写正式 `Set`
- 先进入 `bulk_ingest_workout`
- 生成候选条目
- 再由用户逐动作或整批确认

### 4. 先改运行配置，不要先扩功能

这轮优先做配置对齐，不扩新功能。  
先把已有训练闭环按新结构跑稳。

## OpenClaw 应该优先读取哪些文件

更新配置时，按下面顺序读取：

1. `docs/product/openclaw-update-playbook.md`
2. `docs/product/training-agent-skill-design.md`
3. `schemas/skill-io.md`
4. `schemas/core-models.md`
5. `prompts/router.md`
6. `prompts/skills/start_session.md`
7. `prompts/skills/log_set.md`
8. `prompts/skills/amend_set.md`
9. `prompts/skills/bulk_ingest_workout.md`
10. `docs/reference/feishu-mapping.md`

如果还需要样例，再读：

- `fixtures/real-chat-scenarios.md`
- `fixtures/mock_sessions.json`
- `fixtures/mock_sets.json`
- `fixtures/bulk_ingest_candidates.json`

## OpenClaw 更新顺序

### Step 1：更新 router

目标：

- 按 `prompts/router.md` 重写或替换现有顶层路由 prompt
- Router 只做意图识别、缺失字段判断、skill 选择、参数结构化

Router 输出必须保持为：

- `intent`
- `skill`
- `need_clarification`
- `missing_fields`
- `arguments`

不要让 router 直接输出完整训练建议，不要让 router 自己写表。

### Step 2：先落 4 个核心 skills

优先更新这 4 个：

- `start_session`
- `log_set`
- `amend_set`
- `bulk_ingest_workout`

原因：

- 这 4 个已经能覆盖开始训练、记录一组、修改一组、批量导入四条核心路径

每个 skill 都必须对齐对应 prompt 文件，不要自行合并回万能 prompt。

### Step 3：补齐 skill 输出协议

所有用户层 skill 返回时，统一带上：

- `message`
- `data`
- `confidence`
- `needs_confirmation`
- `next_actions`
- `commit_status`
- `pending_sync_targets`

其中：

- `commit_status = committed | pending_sync | rejected`
- `pending_sync_targets = []`

如果 OpenClaw 当前不支持全部字段，也至少要预留：

- `commit_status`
- `pending_sync_targets`

### Step 4：飞书表映射按主真相层 / 投影层分开

OpenClaw 更新工具调用时，要按下面规则做：

直接写入的对象只允许是：

- `sessions`
- `sets`
- `exercise_catalog`
- `constraints`

不能由用户层 skill 直接写：

- `session_summaries`
- 飞书日历
- 飞书文档

这些必须走投影更新流程。

### Step 5：补 `bulk_ingest_workout` 入口

满足以下输入时，router 必须优先路由到 `bulk_ingest_workout`：

- “帮我导入这次训练”
- “我一次发一堆动作”
- “这张训记截图帮我录一下”
- “把这张图里的训练导入”

不要继续让 `log_set` 兼容批量导入主流程。

`log_set` 只负责单组级别记录。

### Step 6：再补训练中教练能力

前 4 个核心 skill 稳定后，再继续更新：

- `swap_exercise`
- `suggest_next_set`
- `end_session`
- `query_context`
- `pre_workout_decision`
- `conditioning_protocol_adjust`

不要在前 4 个不稳时优先扩训练周边能力。

## 需要 OpenClaw 明确更新的配置点

### Router 规则

- 模糊输入先判 skill，不要先生成答案
- 缺字段时先追问
- 批量输入与图片输入优先走 `bulk_ingest_workout`
- 单组输入才走 `log_set`

### `start_session`

- 支持从目标生成训练草案
- 支持用户给出候选动作列表再编排
- 支持时长、器械、伤痛、疲劳约束
- 创建或更新 `active session`

### `log_set`

- 只处理单组记录
- 支持重量、次数、RPE、动作反馈
- 不确定动作时不能直接写
- 不能把单组误写成整次训练

### `amend_set`

- 支持“第三组改成 75kg”
- 支持“删除最后一组”
- 必须精确命中目标 set
- 修改后要重新触发 session 聚合更新

### `bulk_ingest_workout`

- 支持一次多动作、多组解析
- 支持截图导入
- 先出候选，不直接落库
- 支持逐动作确认和整批确认

## 当前不该让 OpenClaw 做的事

- 不要把 `fitness-assistant/backend/` 当成当前线上主运行路径
- 不要继续维持“一个万能 prompt 覆盖所有训练问题”
- 不要让任意 skill 直接改日历和 summary
- 不要让图片识别结果直接写入正式训练记录
- 不要为了飞书当前方便而修改训练核心模型

## OpenClaw 更新完成后的验收

至少要验证下面 6 条：

1. “今天练什么，我只有 40 分钟，肩和踝康复优先” 能走 `start_session`
2. “下拉第一组 26kg×10，背没感觉” 能走 `log_set`
3. “第三组改成 75kg” 能走 `amend_set`
4. “这张训记截图帮我导入” 能走 `bulk_ingest_workout`
5. 批量导入必须先确认，不直接入库
6. 投影失败时，返回里能看到 `pending_sync`

## 建议的执行顺序

1. 更新 router
2. 更新 `start_session`
3. 更新 `log_set`
4. 更新 `amend_set`
5. 更新 `bulk_ingest_workout`
6. 验证 4 条核心路径
7. 再更新训练中调整与结束训练相关 skills

## 一句话结论

OpenClaw 现在要做的不是“再想一套新架构”，而是按仓库里已经定好的：

- `router + task skills`
- `主真相层 + 投影层`
- `单组记录 vs 批量导入`

把线上配置更新到一致。
