# Fitness Assistant - 健身助手

> 个人健身数据中枢，AI驱动的训练计划与记录管理

## 项目简介

基于 FastAPI + PostgreSQL + 飞书生态的个人健身管理系统。

**核心功能：**
- 📊 训练记录结构化存储（支持文本/OCR截图输入）
- 🤖 AI训练建议（基于历史上下文）
- 🔄 飞书双向同步（多维表格 + 日历）
- 📈 可视化Dashboard（容量趋势、部位分布）

**项目结构：**
- `backend/` - FastAPI后端服务（含AI角色）
- `scripts/` - 数据库初始化脚本
- `docs/` - 项目文档

## 快速开始

### 环境要求
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourname/fitness-assistant.git
cd fitness-assistant

# 安装依赖
cd backend
pip install -r requirements.txt

# 初始化数据库
psql -U postgres -f scripts/init_db.sql

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入飞书配置

# 启动服务
uvicorn main:app --reload
```

### 验证安装

```bash
# 健康检查
curl http://localhost:8000/health

# 预期输出
{"status": "ok"}
```

## 文档索引

| 文档 | 路径 | 说明 |
|-----|------|------|
| PRD | `docs/product/fitness-assistant-prd.md` | 产品需求文档 |
| Backlog | `docs/product/backlog.md` | 任务清单 |
| 系统架构 | `docs/fitness-system-architecture.md` | 技术设计、Schema |
| 决策记录 | `docs/product/decisions.md` | ADR-lite |

## 开发进度

- [x] Iteration 0: 文档与规划
- [ ] Iteration 1: 基础设施（进行中）
- [ ] Iteration 2: 核心功能
- [ ] Iteration 3: 增强功能
- [ ] Iteration 4: 角色AI
- [ ] Iteration 5: 优化与文档

## License

MIT
