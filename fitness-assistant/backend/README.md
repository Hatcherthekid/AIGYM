# 健身助手后端服务

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入飞书配置
```

### 3. 初始化数据库

```bash
# 创建数据库
psql -U postgres -c "CREATE DATABASE fitness;"

# 执行初始化脚本
psql -U postgres -d fitness -f ../scripts/init_db.sql
```

### 4. 启动服务

```bash
# 开发模式
uvicorn main:app --reload

# 生产模式
python main.py
```

### 5. 验证

```bash
# 健康检查
curl http://localhost:8000/health

# API文档
open http://localhost:8000/docs
```

## API 端点

| 端点 | 方法 | 说明 |
|-----|------|------|
| `/health` | GET | 健康检查 |
| `/api/v1/training/logs` | POST | 创建训练记录 |
| `/api/v1/training/logs` | GET | 查询训练记录 |
| `/api/v1/training/logs/{id}` | GET | 获取单条记录 |
| `/api/v1/training/logs/{id}` | PUT | 更新记录 |
| `/api/v1/training/logs/{id}` | DELETE | 删除记录 |
| `/api/v1/training/summary` | GET | 训练汇总 |
| `/api/v1/webhooks/feishu` | POST | 飞书Webhook |

## 目录结构

```
backend/
├── api/
│   ├── training.py      # 训练记录API
│   └── webhooks.py      # 飞书Webhook
├── models/
│   └── training.py      # SQLAlchemy模型
├── services/
│   ├── ai/              # AI角色
│   │   ├── trainer.py   # 训练师
│   │   ├── rehab.py     # 康复师
│   │   └── router.py    # 角色路由
│   ├── parser.py        # 文本解析
│   ├── ocr.py           # OCR识别
│   └── feishu.py        # 飞书集成
├── main.py              # 服务入口
├── requirements.txt     # 依赖
└── .env.example         # 环境变量模板
```
