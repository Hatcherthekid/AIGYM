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
| P2-1 | 实现指令解析系统 | `backend/services/command_router.py` | `/记录 卧推 60kg 10次 4组` 正确解析为结构化数据 | 无 | todo |
| P2-2 | 集成OCR识别 | `backend/services/ocr.py` | 5张截图准确率≥90% | Q1决策 | todo |
| P2-3 | 实现飞书表格读写 | `backend/services/feishu.py` | 调用飞书API读写表格，字段正确 | P1-5 | todo |
| P2-4 | ~~实现飞书Webhook回写~~ | ~~`backend/api/webhooks.py`~~ | ~~表格编辑后数据库更新~~ | ~~P1-4~~ | ⏭️ **deferred** |
| P2-5 | 实现指令处理器 | `backend/api/commands.py` | 支持 /记录 /llm /今天练什么 /查看 /帮助 | P2-1 | todo |
| P2-6 | 实现 AI 训练建议 | `backend/services/ai/trainer.py` | 基于历史记录生成今日训练计划 | P2-3 | todo |

**指令设计原则（新增）：**
采用**指令式交互**而非自然语言解析，提升可控性和用户体验：

| 指令 | 场景 | 示例 |
|-----|------|------|
| `/记录` | 快速标准记录 | `/记录 卧推 60kg 10次 4组` |
| `/llm` | 复杂描述记录 | `/llm 今天练胸，先用60kg热身，然后80kg正式组` |
| `/今天练什么` | 获取训练建议 | `/今天练什么` 或 `/今天练什么 背` |
| `/查看` | 查询历史记录 | `/查看 昨天` 或 `/查看 卧推` |
| `/帮助` | 显示帮助信息 | `/帮助` |

**阻塞项：**
- P2-2 依赖 Q1（OCR方案）决策，需在 2026-03-20 前完成

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
| Q1 | OCR方案选型？飞书原生vs第三方 | 2026-03-20 | P2-2 |
| Q2 | 是否需要本地SQLite离线缓存？ | 2026-03-25 | P3-3 设计 |
| Q3 | 周报生成时机（周日/周一） | 2026-03-30 | P3-4 设计 |

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
