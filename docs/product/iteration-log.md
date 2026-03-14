# 健身助手迭代日志

> 遵循：`rules/dev/iteration_and_pm.md`
> 格式：Goal / Done / Not done / Verification / Next

---

## Iteration 0：文档与规划 ✅ COMPLETED

**时间**：2026-03-13  
**状态**：已完成

### Goal
1. 完成PRD按规范重写
2. 确定系统架构和数据库设计
3. 建立项目管理文档（Backlog + 决策记录）

### Done
- [x] PRD按 `prd_policy.md` 规范重写，包含完整checklist（20个任务）
  - 产物：`docs/product/fitness-assistant-prd.md`
- [x] 系统架构文档完成，含数据库Schema、API设计、同步机制
  - 产物：`docs/fitness-system-architecture.md`
- [x] 创建迭代日志（本文件）
  - 产物：`docs/product/iteration-log.md`
- [x] 创建Backlog，所有任务含入口+验收标准
  - 产物：`docs/product/backlog.md`
- [x] 创建决策记录，5个ADR + 3个待决策
  - 产物：`docs/product/decisions.md`
- [x] 创建开发规则文档
  - 产物：`docs/product/dev-rules.md`
- [x] 更新AGENTS.md，添加限制条件索引
  - 产物：`AGENTS.md`（更新）

### Not done
- 无（本次迭代100%完成）

### Verification
- [x] `ls docs/product/` 显示6个文档
- [x] `cat docs/product/fitness-assistant-prd.md | grep "任务 Checklist"` 显示20个任务
- [x] 每个Backlog任务具备：入口 + 验收标准 + 状态
- [x] `cat AGENTS.md | grep "需求不清，禁止开工"` 显示限制条件
- [x] Rule文件存在：`rules/product/prd_policy.md`, `rules/dev/iteration_and_pm.md`

### Next
1. **Iteration 1**：Phase 1 - 数据库 + FastAPI框架
2. 确定OCR方案（Q1决策，截止2026-03-20）

### 复盘笔记
**学到了什么：**
- 先写规范文档再开工，避免后期返工
- PRD的checklist要具体到"可执行+可验证"，不能抽象
- Rule文件要独立保存，AGENTS.md只放索引

**下次避免什么：**
- 避免一次性想太多功能，按Phase分批交付
- 避免在AGENTS.md写太多细节，保持索引性质

---

## Iteration 1：基础设施 🔄 IN PROGRESS

**时间**：2026-03-13 至 2026-03-20  
**状态**：进行中

### 架构调整（2026-03-14）
- 决策：开发服务与AI角色统一单仓库管理（ADR-006）
- 新增任务 P1-6：初始化项目目录结构
- 目录规划：`backend/` 含 `services/ai/` 子目录

### Goal
1. 完成项目目录结构搭建，可提交GitHub
2. 完成PostgreSQL数据库搭建和Schema初始化
3. 搭建FastAPI基础框架，实现/health端点
4. 配置飞书Webhook接收端，完成验证

### Code Complete ✅ (已完成验证)
- [x] P1-6：初始化项目目录结构（`fitness-assistant/` 目录树）→ **已推送到 GitHub**
- [x] P1-3：搭建FastAPI基础框架（`main.py` + `/health` 端点）→ **✅ 验证通过**
- [x] P1-2：创建训练记录表Schema（`models/training.py`）→ **✅ 6个表已创建**
- [x] P1-1：初始化PostgreSQL数据库（`scripts/init_db.sql`）→ **✅ 数据库就绪**
- [x] P1-5：实现基础CRUD API（`api/training.py` 框架）→ **✅ CRUD全部测试通过**
- [x] P1-4：配置飞书Webhook接收端（`api/webhooks.py`）→ **路由完成，待飞书配置验证**

### Verification Pending ⏳
- [x] 安装 PostgreSQL 并运行 `init_db.sql` ✅
- [x] 配置数据库连接（SQLAlchemy session）✅
- [x] 实现真实的 CRUD 操作（替换 TODO）✅
- [x] 启动服务并测试 `/health` 端点 ✅
- [ ] 配置飞书开发者后台并完成 Webhook 验证（需飞书配置）

### Verification
#### 代码检查（已完成）
- [x] `ls fitness-assistant/` 显示完整目录结构
- [x] `cat backend/main.py` 包含 `/health` 端点
- [x] `cat backend/models/training.py` 包含5个数据模型
- [x] `cat scripts/init_db.sql` 包含所有建表语句
- [x] `cat backend/api/webhooks.py` 包含Webhook处理器

#### 功能验证
- [x] `curl http://localhost:8000/health` 返回 `{"status": "ok"}` ✅
- [x] `psql -d fitness -c "\dt"` 显示所有表 ✅
- [ ] 飞书开发者控制台显示Webhook验证通过（需飞书配置）

### Next
1. 配置飞书开发者后台并完成 Webhook 验证（P1-4）
2. 开始 Iteration 2：核心功能开发

---

## Iteration 1 补充记录：2026-03-14 验证完成

### 本次完成
- [x] P1-1: PostgreSQL 数据库安装 + 建表（6个表）
- [x] P1-2: SQLAlchemy 模型定义 + database.py 配置
- [x] P1-3: FastAPI 服务启动，/health 验证通过
- [x] P1-5: 完整 CRUD API 实现 + 测试通过
  - POST /logs - 创建记录
  - GET /logs - 列表查询
  - GET /logs/{id} - 单条查询
  - PUT /logs/{id} - 更新（支持乐观锁）
  - DELETE /logs/{id} - 删除
  - GET /summary - 汇总统计

### 验证记录
```bash
# 健康检查
$ curl http://127.0.0.1:8000/health
{"status":"ok","service":"fitness-assistant","version":"0.1.0"}

# 创建测试记录
$ curl -X POST /api/v1/training/logs -d '{...}'
{"id": 1, "total_volume": 1160, "message": "训练记录已创建"}

# 数据库验证
$ psql -d fitness -c "\dt"
6 rows: training_logs, training_sessions, exercise_pr, user_snapshot, sync_log, offline_queue
```

### 阻塞项
- 无

---

## 迭代计划概览

| 迭代 | 时间 | 主题 | 状态 |
|-----|------|------|------|
| Iteration 0 | 2026-03-13 | 文档与规划 | ✅ 完成 |
| Iteration 1 | 2026-03-13 ~ 20 | 基础设施 | 🔄 进行中 |
| Iteration 2 | 2026-03-20 ~ 04-03 | 核心功能 | ⏳ 待开始 |
| Iteration 3 | 计划中 | 增强功能 | ⏳ 待规划 |
| Iteration 4 | 计划中 | 角色AI | ⏳ 待规划 |
| Iteration 5 | 计划中 | 优化与文档 | ⏳ 待规划 |

---

## 附录：文档索引

| 文档 | 路径 |
|-----|------|
| PRD | `docs/product/fitness-assistant-prd.md` |
| Backlog | `docs/product/backlog.md` |
| 决策记录 | `docs/product/decisions.md` |
| 系统架构 | `docs/fitness-system-architecture.md` |
| 开发规则 | `docs/product/dev-rules.md` |
| Rule - PRD | `rules/product/prd_policy.md` |
| Rule - 迭代 | `rules/dev/iteration_and_pm.md` |
