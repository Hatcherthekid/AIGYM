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

### Code Complete 📝 (待验证)
- [x] P1-6：初始化项目目录结构（`fitness-assistant/` 目录树）→ **已推送到 GitHub**
- [x] P1-3：搭建FastAPI基础框架（`main.py` + `/health` 端点）→ **代码完成，待启动测试**
- [x] P1-2：创建训练记录表Schema（`models/training.py`）→ **模型定义完成，待建表**
- [x] P1-1：初始化PostgreSQL数据库（`scripts/init_db.sql`）→ **脚本完成，待安装 PG**
- [x] P1-4：配置飞书Webhook接收端（`api/webhooks.py`）→ **路由完成，待配置验证**
- [x] P1-5：实现基础CRUD API（`api/training.py` 框架）→ **接口框架完成，待连数据库**

### Verification Pending ⏳
- [ ] 安装 PostgreSQL 并运行 `init_db.sql`
- [ ] 配置数据库连接（SQLAlchemy session）
- [ ] 实现真实的 CRUD 操作（替换 TODO）
- [ ] 启动服务并测试 `/health` 端点
- [ ] 配置飞书开发者后台并完成 Webhook 验证

### Verification
#### 代码检查（已完成）
- [x] `ls fitness-assistant/` 显示完整目录结构
- [x] `cat backend/main.py` 包含 `/health` 端点
- [x] `cat backend/models/training.py` 包含5个数据模型
- [x] `cat scripts/init_db.sql` 包含所有建表语句
- [x] `cat backend/api/webhooks.py` 包含Webhook处理器

#### 功能验证（待完成）
- [ ] `curl http://localhost:8000/health` 返回 `{"status": "ok"}`
- [ ] `psql -d fitness -c "\dt"` 显示所有表
- [ ] 飞书开发者控制台显示Webhook验证通过

### Next
1. 安装 PostgreSQL 并初始化数据库
2. 安装Python依赖并启动服务
3. 测试健康检查端点

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
