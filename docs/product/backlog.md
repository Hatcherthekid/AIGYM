# 健身助手 Backlog

> 遵循：`rules/dev/iteration_and_pm.md`
> 每个条目必须可执行 + 可验收（入口 + 预期结果）

---

## Now（当前迭代 - Iteration 1）

### Phase 1：基础设施（2026-03-13 至 2026-03-20）

| ID | 任务 | 入口 | 验收标准 | 依赖 | 状态 |
|---|------|------|---------|------|------|
| P1-6 | 初始化项目目录结构 | `fitness-assistant/` | 目录结构符合规范，可提交GitHub | 无 | ✅ done |
| P1-1 | 初始化PostgreSQL数据库 | `scripts/init_db.sql` | `psql -c "\dt"` 显示所有表 | P1-6 | ✅ done |
| P1-2 | 创建训练记录表Schema | `backend/models/training.py` | 表结构符合Schema设计，有索引 | P1-1 | ✅ done |
| P1-3 | 搭建FastAPI基础框架 | `backend/main.py` | `curl /health` 返回200 | P1-6 | ✅ done |
| P1-4 | ~~配置飞书Webhook接收端~~ | ~~`backend/api/webhooks.py`~~ | ~~飞书控制台显示验证通过~~ | ~~P1-3~~ | ⏭️ **deferred** |
| P1-5 | 实现基础CRUD API | `backend/api/training.py` | Postman测试全部通过 | P1-2, P1-3 | ✅ done |

**Iteration 1 Goal（已调整）：** 完成项目目录搭建 + FastAPI框架，数据库推迟到 Iteration 3

**架构决策调整（2026-03-14）：**
- **前期简化**：飞书多维表格作为主数据库，机器人直接操作
- **PostgreSQL 推迟**：Iteration 3 再考虑数据迁移到本地数据库
- **后端角色变化**：前期主要提供 AI 建议/计算服务，不存储主数据

**架构决策：** 开发服务与AI角色（训练师/康复师）统一放在 `backend/services/ai/` 目录下管理，单仓库模式。

---

## Next（下个迭代 - Iteration 2）

### Phase 2：核心功能（计划：2026-03-20 至 2026-04-03）

| ID | 任务 | 入口 | 验收标准 | 依赖 | 状态 |
|---|------|------|---------|------|------|
| P2-1 | 实现指令路由系统 | `backend/services/command_router.py` | 支持 `/记录` `/修改` `/删除` `/llm` 等指令 | 无 | todo |
| ~~P2-2~~ | ~~集成OCR识别~~ | ~~`backend/services/ocr.py`~~ | ~~无需单独 OCR，LLM 自带图片识别能力~~ | ~~Q1~~ | ❌ **cancelled** |
| P2-3 | 实现飞书表格读写 | `backend/services/feishu.py` | 调用飞书API读写表格，字段正确 | P1-5 | todo |
| P2-4 | ~~实现飞书Webhook回写~~ | ~~`backend/api/webhooks.py`~~ | ~~表格编辑后数据库更新~~ | ~~P1-4~~ | ⏭️ **deferred** |
| P2-5 | 实现指令处理器 | `backend/api/commands.py` | 支持 /记录 /llm /今天练什么 /查看 /帮助 | P2-1 | todo |
| P2-6 | 实现 AI 训练建议 | `backend/services/ai/trainer.py` | 基于历史记录生成今日训练计划 | P2-3 | todo |

**指令与 Agent 设计原则（新增）：**

采用**指令路由 + Agent 自主决策**架构：

| 指令 | 路由方式 | 处理逻辑 | 示例 |
|-----|---------|---------|------|
| `/记录` | 规则路由 | 结构化解析 → RecorderAgent → 直接写飞书 | `/记录 卧推 60kg 10次 4组` |
| `/llm` | LLM 自主路由 | LLM 理解意图 → 决策调用子 agent/skill | `/llm [图片]` `/llm 肩膀疼今天能练吗？` |
| `/今天练什么` | 固定路由 | → TrainerAgent 生成计划 | `/今天练什么 背` |
| `/查看` | 固定路由 | → QuerierAgent 查询飞书 | `/查看 昨天` |

**Agent 体系：**
- `RecorderAgent`: 写入飞书表格
- `QuerierAgent`: 读取飞书表格
- `TrainerAgent`: 生成训练计划、分析趋势
- `RehabAgent`: 伤病建议、动作替代
- `LLMRouter`: 理解复杂输入，自主决策调用其他 agents

**图片/OCR 处理：**
- 无需独立 OCR 组件
- 图片通过 `/llm` 指令传给 LLM，LLM 自带 OCR 和意图理解能力
- LLM 决策：直接回答 / 提取数据给 RecorderAgent / 咨询 RehabAgent 等

**Iteration 2 详细设计（新增）：**

#### 数据模型更新（关键变更）
从"一行=一个动作"改为**"一行=一组"**：

| 字段 | 说明 | 示例 |
|-----|------|------|
| 日期 | 训练日期 | 2026-03-14 |
| 训练日ID | 唯一标识 | 20260314-PUSH |
| 序号 | 动作序号 | 1, 2, 3... |
| 动作 | 动作名称 | 卧推 |
| 组号 | 第几组 | 1, 2, 3... |
| 重量 | 含单位 | 100kg |
| 次数 | 完成次数 | 5 |
| RPE | 自觉用力程度 1-10 | 9 |
| 组类型 | 热身/正式/递减/力竭 | 正式 |
| 备注 | 该组感受 | 左肩不适 |
| 容量 | 自动计算 | 500 |

#### 指令详细设计

**记录指令 - 逐组对话模式：**
```
用户: /记录
机器人: 📋 开始记录，动作1是什么？
用户: 卧推
机器人: 🏋️ 卧推 - 第1组，重量？
用户: 60kg热身
机器人: 几次？
用户: 12次RPE6
机器人: ✅ 已记录第1组。下一组？（输重量继续，或/下一动作，或/完成）
```

**快捷记录模式：**
```
/记录 深蹲 100kg 5次×5组 正式
```

**修改指令：**
```
/修改 今天 卧推 第3组 重量为90kg
/修改 昨天 深蹲 组类型为递减
/删除 今天 卧推 第5组
/删除 昨天 所有记录
```

**查看指令：**
```
/查看 今天          # 看今日已记录
/查看 昨天          # 看昨天训练
/查看 卧推          # 看所有卧推记录
/查看 本周          # 看本周汇总
```

#### 表格视图设计

1. **逐组明细**（主表，机器人写入）
2. **动作汇总**（公式自动计算，按动作分组）
3. **今日计划**（AI生成，训练前可编辑）
4. **历史趋势**（图表，1RM/容量变化）

#### 编辑权限设计
- **机器人独占写入**：表格对用户只读，只能通过指令修改
- **今日计划例外**：AI生成后，用户在训练前可通过表格直接编辑（或发/修改指令）
- **训练开始后锁定**：防止误改历史

**阻塞项：**
- 无

---

## Later（后续迭代）

### Phase 3：增强功能（计划：Iteration 3）

| ID | 任务 | 入口 | 验收标准 | 依赖 |
|---|------|------|---------|------|
| P3-1 | 集成飞书日历 | `backend/services/feishu_calendar.py` | 创建事件后日历可见，含训练内容描述 | P2-3 |
| P3-2 | 配置Dashboard图表 | `scripts/setup_feishu_dashboard.md` | 飞书多维表格显示容量趋势图、部位分布图 | P2-3 |
| P3-3 | 实现离线队列 | `backend/services/sync_queue.py` | 断网后编辑，恢复后自动同步，无数据丢失 | P2-4 |
| P3-4 | 实现周报自动生成 | `backend/services/weekly_report.py` | 周日自动生成飞书文档，含本周总结+下周建议 | P2-6 |
| P3-5 | 实现冲突解决UI | `backend/services/conflict_resolver.py` | 冲突时发送飞书消息卡片，支持选择版本 | P2-4, P3-3 |

### Phase 4：角色AI（计划：Iteration 4）

| ID | 任务 | 入口 | 验收标准 | 依赖 |
|---|------|------|---------|------|
| P4-1 | 设计训练师Prompt | `backend/ai/prompts/trainer.md` | 输入约束条件，输出可执行周计划 | 无 |
| P4-2 | 设计康复师Prompt | `backend/ai/prompts/rehab.md` | 输入疼痛描述，输出可做/不可做清单 | 无 |
| P4-3 | 实现角色自动路由 | `backend/services/ai/router.py` | 关键词触发正确角色，上下文继承 | P4-1, P4-2 |
| P4-4 | 实现动作替代推荐 | `backend/services/ai/substitution.py` | 输入器械限制，输出等价替代方案 | P4-1 |

### Phase 5：优化与文档（计划：Iteration 5）

| ID | 任务 | 入口 | 验收标准 | 依赖 |
|---|------|------|---------|------|
| P5-1 | 编写API文档 | `docs/api/README.md` | 所有端点含请求/响应示例 | P1-5 |
| P5-2 | 编写部署文档 | `docs/deployment.md` | 新环境可按文档完成部署 | P5-1 |
| P5-3 | 性能测试 | `tests/performance/locustfile.py` | API P95 < 500ms，有测试报告 | P2-5 |
| P5-4 | 用户试用反馈收集 | `docs/feedback/iteration_5.md` | 记录至少5条使用反馈，整理改进点 | P5-2 |

---

## 待决策阻塞项

| ID | 问题 | 决策期限 | 阻塞任务 |
|---|------|---------|---------|
| ~~Q1~~ | ~~OCR方案选型？~~ | ~~2026-03-20~~ | ~~P2-2~~ ❌ **cancelled** |
| Q2 | 是否需要本地SQLite离线缓存？ | 2026-03-25 | P3-3 设计 |
| Q3 | 周报生成时机（周日/周一） | 2026-03-30 | P3-4 设计 |

**决策说明：**
- Q1: 无需独立 OCR，LLM 自带图片识别能力，通过 `/llm` 指令处理图片

---

## 已完成 ✅

| ID | 任务 | 完成日期 | 验证方式 | 产物 |
|---|------|---------|---------|------|
| I0-1 | 创建项目文档结构 | 2026-03-13 | `ls docs/` 显示product/目录 | `docs/product/` |
| I0-2 | PRD按规范重写 | 2026-03-13 | 符合prd_policy.md所有要求 | `fitness-assistant-prd.md` |
| I0-3 | 系统架构文档 | 2026-03-13 | 含完整Schema、API、同步设计 | `fitness-system-architecture.md` |
| I0-4 | 创建Backlog | 2026-03-13 | 所有任务含入口+验收标准 | `backlog.md` |
| I0-5 | 创建迭代日志 | 2026-03-13 | 含Goal/Done/Verification/Next | `iteration-log.md` |
| I0-6 | 创建决策记录 | 2026-03-13 | 5个ADR + 3个待决策 | `decisions.md` |

---

## 变更日志

| 日期 | 变更 |
|-----|------|
| 2026-03-13 | 初始版本，Phase 1-5 任务规划 |
| 2026-03-13 | 补充Later阶段任务的入口和验收标准 |
| 2026-03-13 | 添加"依赖"列，标记阻塞关系 |
