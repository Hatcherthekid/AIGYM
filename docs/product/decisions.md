# 健身训练 Agent 决策记录（ADR-lite）

> 更新：2026-03-22

## ADR-001：当前阶段采用飞书 MVP，而不是先做正式 App

### Problem
训练记录器最终会是独立 App，但当前需要先快速验证训练 agent 是否真正有价值。

### Decision
当前阶段继续使用飞书作为运行壳，不开发正式 App UI。

### Rationale
- 快速上线
- 低开发成本
- 便于验证训练 agent 智能质量

### Trade-offs
- 记录体验不可能达到训记级别
- 飞书后台配置可维护性差

---

## ADR-002：飞书多维表作为当前运行时真相层

### Problem
当前没有独立后端主库，但又必须有可查询的结构化历史供 agent 使用。

### Decision
MVP 阶段以飞书多维表作为当前运行时结构化真相层。

### Rationale
- 避免前期重后端
- 先验证训练闭环

### Trade-offs
- 字段和迁移受飞书约束
- 后期迁移需要抽象层

---

## ADR-003：仓库文档优先于飞书/OpenClaw 后台配置

### Problem
飞书和 OpenClaw 后台配置难导出、难 review、易漂移。

### Decision
仓库文档、prompt、schema 是唯一设计真相；后台配置随后对齐。

### Rationale
- 可审计
- 可版本化
- 便于未来迁移

### Trade-offs
- 需要额外做线上配置对齐

---

## ADR-004：Prompt 采用 Router + Task Skills

### Problem
万能 prompt 边界模糊，容易脑补状态和历史。

### Decision
采用一个薄 router + 多个任务型 skills。

### 正式技能集

- `start_session`
- `log_set`
- `amend_set`
- `swap_exercise`
- `suggest_next_set`
- `end_session`
- `query_context`
- `pre_workout_decision`
- `conditioning_protocol_adjust`

### Trade-offs
- prompt 文件数增加
- 需要维护 skill 协议

---

## ADR-005：记录器是长期产品核心，但当前不追求记录交互体验

### Problem
记录器对长期产品非常关键，但飞书无法模拟训记级记录体验。

### Decision
当前阶段只验证记录可靠和 agent 智能，不追求飞书里的高频记录交互体验。

### Rationale
- 先验证“数据 + 教练”是否成立
- 未来 App 再承接高频记录

### Trade-offs
- 飞书阶段的记录体验天然会偏笨重

---

## ADR-006：FastAPI / SQLAlchemy 骨架保留为未来适配层

### Problem
仓库里已有后端骨架，但它不是当前线上主路径。

### Decision
不删除 `fitness-assistant/backend/`，但明确其定位为未来独立后端 / App 的适配层骨架与协议参考实现。

### Rationale
- 保留未来迁移入口
- 不浪费已有结构

### Trade-offs
- 需要在文档中明确“不是当前主实现”，防止误导

---

## ADR-007：图片输入只作为补充录入，必须经过确认

### Problem
图片识别存在幻觉，当前已出现“肩部训练被编造成胸部动作和假重量”的问题。

### Decision
图片输入只作为补充录入；所有图片解析结果先进入候选导入，确认后再写正式记录。

### Rationale
- 避免污染结构化历史
- 保留图片补录价值

### Trade-offs
- 多一步确认
- 牺牲一部分录入速度

---

## ADR-008：批量导入单独建 `bulk_ingest_workout`，不并入 `log_set`

### Problem
单组记录与整次训练导入属于两类不同任务；把多动作、多组导入硬塞给 `log_set` 会让职责混乱，也更容易在图片场景下产生幻觉写入。

### Decision
新增独立用户层 skill：`bulk_ingest_workout`。

### Rationale
- 保持 `log_set` 只处理单组记录
- 批量导入可以单独做候选确认
- 更容易控制图片与截图的风险

### Trade-offs
- 增加一个 skill 文件和对应配置
- 需要维护批量确认流程

---

## ADR-009：提交与投影由系统内置流程负责，不作为用户可调用 skill

### Problem
如果由各个用户层 skill 自己更新 summary、日历、文档，很容易出现只更新一张表或投影不一致的问题。

### Decision
采用系统内置提交流程：

- `commit_main_entities`
- `run_projections`
- `mark_pending_sync_if_failed`

该流程不暴露成用户可调用 skill。

### Rationale
- 强制先写主真相，再更新投影
- 统一处理 `pending_sync`
- 降低跨表不一致风险

### Trade-offs
- 系统分层更复杂
- 需要维护主真相表与投影表边界
