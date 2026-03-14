# 健身助手系统架构文档

> 版本：v0.2 | 更新：2026-03-13 | 用户模式：单用户

---

## 1. 架构总览

```
┌────────────────────────────────────────────────────────────────┐
│                         展示层（飞书）                          │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│  多维表格     │    日历      │   Dashboard  │     文档          │
│  (训练记录)   │  (训练时段)   │  (数据分析)   │  (周报/建议)      │
└──────┬───────┴──────┬───────┴──────┬───────┴─────────┬─────────┘
       │              │              │                 │
       └──────────────┴──────────────┴─────────────────┘
                          │
                    双向同步层
              (Webhook + 主动API调用)
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
│   REST API  │    │  同步引擎    │    │ 离线队列    │
│  (HTTP)     │    │ (冲突解决)   │    │ (待同步)    │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
┌─────────────────────────▼─────────────────────────┐
│                   数据层（单用户）                  │
├─────────────────┬─────────────────┬────────────────┤
│   PostgreSQL    │     Redis       │   SQLite(离线)  │
│  (主数据库)      │   (热点缓存)     │  (本地副本)     │
└─────────────────┴─────────────────┴────────────────┘
```

---

## 2. 单用户模式简化设计

### 2.1 数据隔离（单用户无需隔离）

```sql
-- 单用户模式：省略user_id字段，简化查询
-- 所有表直接存储，无需WHERE user_id = ?

-- 训练记录表
training_logs (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    session_id VARCHAR(32),          -- 训练日ID（同一天多个动作）
    exercise_name VARCHAR(128) NOT NULL,
    body_part VARCHAR(64),           -- 胸/背/腿/肩/手臂/核心/有氧
    exercise_type VARCHAR(32),       -- 主项/辅助/热身/康复
    equipment VARCHAR(64),           -- 杠铃/哑铃/史密斯/器械/自重
    sets JSONB,                      -- [{reps: 10, weight: 60, rpe: 8, note: ""}, ...]
    total_volume INTEGER,            -- 总容量(kg)，自动计算
    duration_minutes INTEGER,        -- 该动作耗时
    source VARCHAR(32),              -- ai_ocr/ai_text/manual_edit/manual_new
    version INTEGER DEFAULT 1,       -- 乐观锁版本
    feishu_record_id VARCHAR(64),    -- 飞书表格记录ID
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 训练日汇总表（用于快速查询）
training_sessions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,       -- 一天一条
    theme VARCHAR(32),               -- 推/拉/腿/有氧/全身/康复/休息
    total_volume INTEGER,
    total_sets INTEGER,
    total_exercises INTEGER,
    duration_minutes INTEGER,
    avg_rpe DECIMAL(3,1),
    completion_rate DECIMAL(3,2),    -- 计划完成率
    feeling VARCHAR(256),            -- 主观感受
    feishu_event_id VARCHAR(64),     -- 飞书日历事件ID
    created_at TIMESTAMP DEFAULT NOW()
);

-- 动作PR追踪表（自动维护）
exercise_pr (
    id SERIAL PRIMARY KEY,
    exercise_name VARCHAR(128) UNIQUE,
    current_1rm DECIMAL(5,1),        -- 估算1RM
    max_weight DECIMAL(5,1),         -- 历史最大重量
    max_reps INTEGER,                -- 最大次数记录
    pr_date DATE,                    -- PR日期
    trend_30d VARCHAR(16),           -- up/down/stable
    last_session_date DATE,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 用户状态快照（供AI快速读取）
user_snapshot (
    id INTEGER PRIMARY KEY DEFAULT 1, -- 只有一条记录
    last_training_date DATE,
    current_streak INTEGER,          -- 连续训练天数
    weekly_volume JSONB,             -- 本周各部位容量
    monthly_volume JSONB,            -- 近4周容量
    current_constraints JSONB,       -- 当前约束（伤病/器械）
    soreness_map JSONB,              -- 酸痛分布
    next_planned_date DATE,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 同步日志（用于故障排查）
sync_log (
    id SERIAL PRIMARY KEY,
    direction VARCHAR(16),           -- feishu_to_db / db_to_feishu
    table_name VARCHAR(64),
    record_id INTEGER,
    action VARCHAR(16),              -- create/update/delete
    status VARCHAR(16),              -- success/failed/pending
    error_msg TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 离线队列
offline_queue (
    id SERIAL PRIMARY KEY,
    operation VARCHAR(16),           -- create/update/delete
    table_name VARCHAR(64),
    payload JSONB,                   -- 完整数据
    retry_count INTEGER DEFAULT 0,
    status VARCHAR(16) DEFAULT 'pending', -- pending/processing/failed
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.2 飞书表格设计（单用户固定结构）

**表格1：训练记录表**（Base ID固定配置）

| 字段ID | 字段名 | 类型 | 公式/说明 |
|-------|-------|------|----------|
| fld_id | 记录ID | 自动编号 | `LOG_{date}_{seq}` |
| fld_date | 日期 | 日期 | - |
| fld_session | 训练日 | 关联字段 | 关联训练日表 |
| fld_exercise | 动作名称 | 文本 | - |
| fld_body_part | 部位 | 单选 | 胸/背/腿/肩/手臂/核心/有氧 |
| fld_type | 类型 | 单选 | 主项/辅助/热身/康复 |
| fld_sets | 组数详情 | 文本 | JSON字符串 |
| fld_volume | 容量(kg) | 数字 | - |
| fld_rpe | 平均RPE | 数字 | - |
| fld_equipment | 设备 | 多选 | 杠铃/哑铃/史密斯/器械/自重/其他 |
| fld_notes | 备注 | 文本 | - |
| fld_source | 来源 | 单选 | AI录入/手动新建/手动修改 |
| fld_version | 版本 | 数字 | 乐观锁 |
| fld_created | 创建时间 | 日期时间 | - |
| fld_updated | 更新时间 | 日期时间 | - |

**表格2：训练日汇总表**

| 字段 | 说明 |
|-----|------|
| 日期 | 主键 |
| 主题 | 推/拉/腿/有氧/全身/康复/休息 |
| 总容量 | 公式：SUM(关联记录.容量) |
| 总组数 | 公式：SUM(关联记录.组数) |
| 动作数 | 公式：COUNT(关联记录) |
| 时长 | 用户填写或估算 |
| 平均RPE | 公式：AVG(关联记录.RPE) |
| 完成状态 | 已完成/部分完成/跳过 |
| 日历事件ID | 飞书日历关联 |

**表格3：动作档案表**

| 字段 | 说明 |
|-----|------|
| 动作名 | 主键 |
| 当前估算1RM | 自动计算 |
| 历史最大重量 | - |
| 近30天趋势 | ↑↓→ |
| 最近训练日 | - |
| 本月容量 | 公式计算 |

---

## 3. 离线同步策略

### 3.1 场景定义

```
在线 ──断开──> 离线 ──恢复──> 在线
              │
              └── 用户仍可编辑飞书表格（飞书本身支持离线）
              └── 后端服务离线期间无法同步
              └── 恢复后需要增量同步
```

### 3.2 策略选择：客户端优先 + 版本冲突解决

**核心原则：**
- 飞书表格始终可编辑（飞书本身离线能力）
- 后端离线期间，变更进入队列，恢复后批量同步
- 冲突时：**时间戳优先 + 手动确认**

### 3.3 实现方案

#### A. 离线检测

```python
# 健康检查端点
GET /api/v1/health

# 飞书端Webhook检测
# 如果后端无响应，飞书侧标记"待同步"
```

#### B. 变更追踪（Change Tracking）

```sql
-- 所有表增加变更追踪触发器
CREATE TRIGGER track_changes
    AFTER INSERT OR UPDATE OR DELETE ON training_logs
    FOR EACH ROW EXECUTE FUNCTION log_change();

-- 变更记录表
change_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(64),
    record_id INTEGER,
    operation VARCHAR(16),      -- INSERT/UPDATE/DELETE
    old_data JSONB,
    new_data JSONB,
    changed_at TIMESTAMP DEFAULT NOW(),
    synced BOOLEAN DEFAULT FALSE
);
```

#### C. 同步流程

```
后端恢复在线
    ↓
1. 拉取飞书变更（since last_sync_time）
    ↓
2. 获取本地未同步的变更（change_log where synced = false）
    ↓
3. 三方合并（本地 vs 飞书 vs 基准）
    ↓
4. 冲突检测
    ├── 无冲突：直接应用
    └── 有冲突：标记待解决
    ↓
5. 应用变更
    ↓
6. 更新 last_sync_time
```

#### D. 冲突解决UI（飞书消息卡片）

当检测到冲突时，发送飞书消息：

```
⚠️ 数据冲突需确认

动作：杠铃卧推 (2025-03-13)

┌─────────────┬─────────────┐
│  飞书版本    │   本地版本   │
├─────────────┼─────────────┤
│ 重量: 60kg  │ 重量: 65kg  │
│ 修改: 10:23 │ 修改: 10:25 │
└─────────────┴─────────────┘

[使用飞书版本]  [使用本地版本]  [保留两者]
```

### 3.4 队列实现

```python
# offline_queue 表结构见上文

# 同步服务伪代码
class OfflineSyncService:
    def __init__(self):
        self.feishu_client = FeishuClient()
        self.db = Database()
    
    async def sync_loop(self):
        while True:
            if self.is_online():
                pending = await self.db.get_pending_operations()
                for op in pending:
                    try:
                        if op.direction == 'db_to_feishu':
                            await self.push_to_feishu(op)
                        else:
                            await self.pull_from_feishu(op)
                        await self.db.mark_synced(op.id)
                    except Exception as e:
                        await self.db.increment_retry(op.id, str(e))
                        if op.retry_count > 3:
                            await self.notify_conflict(op)
            
            await asyncio.sleep(30)  # 30秒检查一次
```

---

## 4. 双向同步详细设计

### 4.1 飞书 Webhook 配置

**事件订阅：**
```
URL: https://your-backend.com/api/v1/webhooks/feishu
Events:
  - record.created    # 新建记录
  - record.updated    # 修改记录
  - record.deleted    # 删除记录
```

**验证逻辑：**
```python
def verify_feishu_webhook(request):
    """验证飞书Webhook签名"""
    token = request.headers.get('X-Feishu-Token')
    timestamp = request.headers.get('X-Feishu-Timestamp')
    signature = request.headers.get('X-Feishu-Signature')
    
    # 使用配置的Encrypt Key验证
    expected = hmac_sha256(token + timestamp + request.body, ENCRYPT_KEY)
    return signature == expected
```

### 4.2 字段映射

```python
FIELD_MAPPING = {
    # 飞书字段ID -> 数据库字段名
    'fld_date': 'date',
    'fld_exercise': 'exercise_name',
    'fld_body_part': 'body_part',
    'fld_type': 'exercise_type',
    'fld_sets': 'sets',
    'fld_volume': 'total_volume',
    'fld_rpe': 'rpe',
    'fld_equipment': 'equipment',
    'fld_notes': 'notes',
    'fld_source': 'source',
    'fld_version': 'version',
}

def feishu_record_to_db(record):
    """转换飞书记录为数据库格式"""
    return {
        db_field: record[fs_field]
        for fs_field, db_field in FIELD_MAPPING.items()
        if fs_field in record
    }
```

### 4.3 同步状态机

```
                    ┌─────────────┐
     ┌─────────────│   已同步    │◀────────────┐
     │             │  (synced)   │             │
     │             └──────┬──────┘             │
     │                    │ 本地修改           │
     │                    ▼                    │
     │             ┌─────────────┐             │
     │    ┌───────│  待推送     │──────┐      │
     │    │       │(pending_out)│      │      │
     │    │       └─────────────┘      │      │
     │    │ 推送成功          推送失败 │      │
     │    │                    │重试3次 │      │
     │    ▼                    ▼       │      │
     │ ┌─────────┐         ┌─────────┐ │      │
     └─│  成功   │         │ 冲突待解 │─┘      │
       │(synced) │         │(conflict)│        │
       └─────────┘         └────┬────┘        │
                                │ 人工解决      │
                                ▼             │
                           ┌─────────┐────────┘
                           │  已解决  │
                           │(resolved)│
                           └─────────┘
```

---

## 5. Dashboard 数据聚合

### 5.1 数据源配置

**飞书多维表格仪表板：**
- 基于"训练日汇总表"创建图表
- 无需后端开发，飞书原生支持

**图表配置：**

| 图表名 | 类型 | 数据源 | 维度 | 指标 |
|-------|------|--------|------|------|
| 月度热力图 | 日历热力图 | 训练日表 | 日期 | 总容量 |
| 部位分布 | 环形图 | 训练记录表 | 部位 | 容量占比 |
| 周训练频率 | 柱状图 | 训练日表 | 周 | 训练次数 |
| 容量趋势 | 折线图 | 训练日表 | 日期 | 7日滑动平均 |
| PR追踪 | 折线图 | 动作档案表 | 日期 | 各动作1RM |

### 5.2 后端计算的高级指标

```python
# 复杂分析由后端计算，写入专门的指标表

class AnalyticsService:
    def calculate_fatigue_index(self, days=7):
        """疲劳累积指数"""
        recent = self.db.get_volume_last_n_days(days)
        baseline = self.db.get_volume_last_n_days(30) / 30 * days
        return recent / baseline  # > 1.2 警告，> 1.5 高危
    
    def calculate_balance_score(self):
        """部位平衡指数"""
        volumes = self.db.get_body_part_volume(days=30)
        # 推拉腿理想比例 1:1:1.2
        push = volumes.get('push', 0)
        pull = volumes.get('pull', 0)
        legs = volumes.get('legs', 0)
        # 计算与理想比例的偏差
        return calculate_deviation(push, pull, legs)
    
    def generate_weekly_recommendation(self):
        """生成下周建议"""
        # 基于近期容量、部位平衡、疲劳指数生成
        pass
```

### 5.3 周报自动生成

```python
# 定时任务：每周日晚上生成周报
cron: "0 20 * * 0"  # 每周日20:00

def generate_weekly_report():
    week_start = get_week_start()
    week_end = get_week_end()
    
    report = {
        'period': f'{week_start} - {week_end}',
        'summary': {
            'total_sessions': count_sessions(week_start, week_end),
            'total_volume': sum_volume(week_start, week_end),
            'completion_rate': calculate_completion(),
        },
        'body_part_distribution': get_distribution(),
        'highlights': find_highlights(),  # PR、突破等
        'warnings': check_warnings(),     # 疲劳、失衡等
        'next_week_plan': suggest_next_week(),
    }
    
    # 写入飞书文档
    doc_token = create_feishu_doc(report)
    send_notification(f"本周训练周报已生成：{doc_token}")
```

---

## 6. API 详细设计

### 6.1 训练记录 API

```yaml
# 创建训练记录
POST /api/v1/training/logs
Request:
  date: "2025-03-13"
  exercise_name: "杠铃卧推"
  body_part: "胸"
  sets:
    - {weight: 60, reps: 10, rpe: 7}
    - {weight: 70, reps: 8, rpe: 8}
  equipment: "杠铃"
  notes: "状态不错"
  source: "ai_ocr"

Response:
  id: 123
  feishu_record_id: "rec_xxx"
  sync_status: "synced"

# 批量查询
GET /api/v1/training/logs?start_date=2025-03-01&end_date=2025-03-13&body_part=胸

# 更新记录（支持乐观锁）
PUT /api/v1/training/logs/{id}
Request:
  weight: 65
  version: 2  # 乐观锁版本

Response:
  success: true
  new_version: 3

# 删除记录
DELETE /api/v1/training/logs/{id}
```

### 6.2 计划 API

```yaml
# 生成周计划
POST /api/v1/plans/generate
Request:
  week_start: "2025-03-17"
  constraints:
    available_days: ["周一", "周三", "周五"]
    max_duration: 60
    injuries: ["左肩不适"]
  preferences:
    focus: "力量增长"
    avoid: ["史密斯深蹲"]

Response:
  plan_id: "plan_001"
  days:
    - date: "2025-03-17"
      theme: "推"
      exercises: [...]
    - date: "2025-03-19"
      theme: "拉"
      exercises: [...]

# 获取今日训练
GET /api/v1/plans/today
Response:
  has_plan: true
  theme: "推"
  exercises: [...]
  estimated_duration: 50
  notes: "今日可尝试加重"

# 确认/修改计划
POST /api/v1/plans/{id}/confirm
Request:
  confirmed_days: [...]
  modifications:
    - date: "2025-03-17"
      changes: "卧推减一组"
```

### 6.3 同步 API

```yaml
# 接收飞书Webhook
POST /api/v1/webhooks/feishu
Headers:
  X-Feishu-Token: xxx
  X-Feishu-Signature: xxx
Body:
  event_type: "record.updated"
  table_id: "tbl_xxx"
  record:
    record_id: "rec_xxx"
    fields: {...}

Response:
  status: "ok"

# 手动触发同步
POST /api/v1/sync/trigger
Request:
  direction: "bidirectional"  # db_to_feishu / feishu_to_db / bidirectional
  tables: ["training_logs", "training_sessions"]

Response:
  job_id: "sync_001"
  status: "processing"

# 查询同步状态
GET /api/v1/sync/status/{job_id}
```

### 6.4 Dashboard API

```yaml
# 获取汇总数据
GET /api/v1/dashboard/summary
Response:
  this_week:
    sessions: 3
    volume: 35000
    avg_rpe: 7.5
  last_30_days:
    total_sessions: 12
    pr_count: 2
    consistency: 0.85  # 计划完成率

# 获取趋势数据
GET /api/v1/dashboard/trends?metric=volume&period=30d
Response:
  data: [
    {date: "2025-02-13", value: 12000},
    {date: "2025-02-14", value: 0},
    ...
  ]
  trend: "up"  # up/down/stable
  change_percent: 12.5

# 获取训练建议
GET /api/v1/dashboard/recommendations
Response:
  immediate:
    - type: "warning"
      message: "胸部容量连续3周过高，建议本周减载"
  next_session:
    suggested_theme: "拉"
    focus: "背部厚度"
  next_week:
    theme_distribution: {推: 1, 拉: 1, 腿: 1}
    notes: "增加一次有氧"
```

---

## 7. 部署配置

### 7.1 环境变量

```bash
# 数据库
DATABASE_URL=postgresql://user:pass@localhost:5432/fitness
REDIS_URL=redis://localhost:6379/0

# 飞书配置
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_ENCRYPT_KEY=xxx
FEISHU_VERIFICATION_TOKEN=xxx

# 飞书表格Base ID（单用户固定）
FEISHU_BASE_ID=base_xxx
FEISHU_TRAINING_LOG_TABLE=tbl_xxx
FEISHU_SESSION_TABLE=tbl_xxx
FEISHU_EXERCISE_PR_TABLE=tbl_xxx

# 服务端配置
PORT=8000
LOG_LEVEL=info
SYNC_INTERVAL_SECONDS=30
```

### 7.2 Docker Compose

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/fitness
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: fitness
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  sync-worker:
    build: .
    command: python -m services.sync.worker
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/fitness
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
```

---

## 8. 待开发清单

| 模块 | 优先级 | 状态 |
|-----|-------|------|
| 数据库Schema初始化脚本 | P0 | 待开发 |
| 飞书Webhook接收端 | P0 | 待开发 |
| 基础CRUD API | P0 | 待开发 |
| 训练记录OCR解析 | P1 | 待开发 |
| 周计划生成AI | P1 | 待开发 |
| 双向同步引擎 | P1 | 待开发 |
| 离线队列实现 | P2 | 待开发 |
| Dashboard聚合API | P2 | 待开发 |
| 周报自动生成 | P2 | 待开发 |
| 冲突解决UI | P3 | 待开发 |

---

## 附录：飞书表格字段ID速查

```json
{
  "training_logs": {
    "table_id": "tbl_xxx",
    "fields": {
      "date": "fld_xxx",
      "exercise": "fld_xxx",
      "body_part": "fld_xxx",
      "sets": "fld_xxx",
      "volume": "fld_xxx",
      "source": "fld_xxx"
    }
  },
  "training_sessions": {
    "table_id": "tbl_xxx",
    "fields": {
      "date": "fld_xxx",
      "theme": "fld_xxx",
      "total_volume": "fld_xxx"
    }
  }
}
```

---

*文档结束*
