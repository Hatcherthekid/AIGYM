# 健身助手产品需求文档 (PRD)

> 状态：讨论中 | 最后更新：2026-03-13

---

## 1. 产品定位

面向有训练经验的健身爱好者，提供**训练记录管理**、**智能计划生成**、**伤病康复指导**的AI助手。

**核心原则：**
- 不过度健美化，提供MVP（最小可行）方案
- 约束驱动：根据伤病、器械、时间限制输出可执行方案
- 可计算的：缺口、容量、预测结果透明可校准

---

## 2. 输入层设计

### 2.1 多模态输入支持

| 输入类型 | 处理方式 | 示例 |
|---------|---------|------|
| 自由文本 | NLP解析 → 结构化 | "卧推4组，15kg×10，20kg×12..." |
| 训练APP截图 | OCR + 视觉LLM提取 |  Keep/训记/其他APP截图 |
| 设备屏幕 | OCR识别关键指标 | Concept2 PM5屏幕（spm/配速） |
| 混合输入 | 合并处理 | 截图 + 补充说明 |

### 2.2 Agent编排流程

```
用户输入
    ↓
意图识别（主Agent）
    ↓
角色路由 → Skill选择
    ↓
二次包装 → 执行Skill
    ↓
结构化输出 + 飞书可视化
```

**意图分类：**
- `log_training` - 记录训练
- `plan_week` - 生成/调整周计划
- `what_today` - 今天练什么
- `exercise_substitution` - 动作替代
- `rehab_guidance` - 康复指导
- `hyrox_plan` - HYROX专项
- `instant_decision` - 即时决策（饿/累/吃多）
- `data_interpretation` - 数据解读

---

## 3. 角色系统（自动切换）

| 角色 | 触发条件 | 核心能力 |
|-----|---------|---------|
| **训练师** | 计划生成、容量管理、动作替代 | 周计划编排、强度波峰管理、器械适配 |
| **康复师** | 肩/踝/腰等伤病相关 | 红线判断、回归路线、可做/不可做清单 |
| **运动科学顾问** | 周期化、HYROX专项、学术问题 | 能量系统训练、比赛准备、文献依据 |

**角色切换逻辑：**
- 关键词触发：疼痛、术后、撞击 → 康复师
- 上下文继承：多轮对话保持当前角色
- 混合场景：康复师 + 训练师协作（伤病约束下的计划）

---

## 4. 记忆分层策略

### 4.1 三层记忆模型

| 层级 | 时间范围 | 用途 | 存储 |
|-----|---------|------|------|
| **热点缓存** | 最近3天 | 今天练什么、即时决策 | Redis |
| **短期记忆** | 最近7天 | 周计划重排、部位容量计算 | PostgreSQL |
| **长期趋势** | 最近30天 | 动作PR趋势、周期评估 | PostgreSQL + 时序分析 |

### 4.2 场景化记忆调用

| 用户问题 | 记忆深度 | 数据组合 |
|---------|---------|---------|
| "今天练什么？" | 热点+短期 | 最近3天训练内容 + 当前酸痛状态 |
| "这周怎么排？" | 短期 | 最近7天各部位容量分布 |
| "卧推应该多重？" | 短期+长期 | 本周胸部容量 + 近30天卧推重量趋势 |
| "我进步了吗？" | 长期 | 各动作30天PR曲线 |

---

## 5. 数据库设计

### 5.1 核心表结构

```sql
-- 训练记录表
training_logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    date DATE NOT NULL,
    exercise_name VARCHAR(128) NOT NULL,
    body_part VARCHAR(64),           -- 胸/背/腿/肩/手臂/核心
    equipment VARCHAR(64),           -- 杠铃/哑铃/史密斯/器械
    sets JSONB,                      -- [{reps: 10, weight: 20, rpe: 8}, ...]
    total_volume INTEGER,            -- 总容量(kg)
    notes TEXT,
    source VARCHAR(32),              -- text/ocr/screenshot
    created_at TIMESTAMP DEFAULT NOW()
);

-- 用户状态快照（供Agent快速读取）
user_state (
    user_id VARCHAR(64) PRIMARY KEY,
    last_7_days_volume JSONB,        -- {chest: 12000, back: 15000, ...}
    last_30_days_pr JSONB,           -- {bench_press: {max: 80, trend: "up"}, ...}
    recent_exercises JSONB,          -- 最近3天训练记录ID列表
    current_constraints JSONB,       -- 伤病/器械限制
    soreness_map JSONB,              -- 当前酸痛分布
    updated_at TIMESTAMP
);

-- 生成的训练计划
training_plans (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    week_start DATE NOT NULL,
    plan_json JSONB,                 -- 完整周计划结构
    actual_completion JSONB,         -- 实际完成情况回填
    constraints_applied JSONB,       -- 应用的约束条件
    feishu_doc_token VARCHAR(128),   -- 飞书文档ID
    created_at TIMESTAMP DEFAULT NOW()
);

-- 单次训练单（当日执行）
daily_workouts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    plan_id INTEGER REFERENCES training_plans(id),
    date DATE NOT NULL,
    target_body_parts VARCHAR(64)[],
    workout_json JSONB,              -- 动作列表+参数
    completed BOOLEAN DEFAULT FALSE,
    completion_rate DECIMAL(3,2),    -- 完成率
    user_feedback JSONB,             -- 主观反馈（累/轻松/疼痛等）
    feishu_msg_id VARCHAR(128)       -- 飞书卡片消息ID
);
```

### 5.2 索引设计

```sql
CREATE INDEX idx_logs_user_date ON training_logs(user_id, date DESC);
CREATE INDEX idx_logs_exercise ON training_logs(user_id, exercise_name, date DESC);
CREATE INDEX idx_logs_body_part ON training_logs(user_id, body_part, date DESC);
CREATE INDEX idx_plans_user_week ON training_plans(user_id, week_start DESC);
```

---

## 6. 飞书集成方案

### 6.1 可视化维度

| 数据类型 | 飞书载体 | 展示形式 |
|---------|---------|---------|
| 训练记录历史 | 多维表格 | 表格 + 自动图表（容量趋势、PR曲线） |
| 周计划 | 云文档 | 富文本计划表（可打印） |
| 单次训练单 | 卡片消息 | 可勾选完成的任务清单 |
| 月度复盘 | 云文档 | 自动生成报告（进步/瓶颈/建议） |

### 6.2 数据流

```
用户记录训练
    ↓
写入数据库
    ↓
同步到飞书多维表格（异步Webhook）
    ↓
自动更新图表 + 触发通知
```

### 6.3 飞书文档模板

**周计划文档结构：**
- 本周目标（部位分布、强度波峰）
- 每日安排表格（日期/部位/主项/组数/备注）
- 伤病注意事项（红色标注）
- 上周完成情况回顾

---

## 7. 核心场景详细设计

### 场景1：训练记录（截图+文本）

**输入示例：**
- 截图：训记APP的卧推记录界面
- 文本："今天肩有点紧，卧推没敢上重量"

**处理流程：**
1. OCR提取：动作名、组数、重量、次数
2. LLM理解文本中的状态信息（肩紧）
3. 结构化存储
4. 更新用户状态快照（胸部容量+1）
5. 飞书多维表格自动+1行

**输出：**
```json
{
  "confirmed_log": {
    "exercise": "卧推",
    "sets": [{"weight": 60, "reps": 10, "rpe": 7}],
    "notes": "肩紧，保守重量"
  },
  "feedback": "记录完成。肩部紧张，建议下次训练前做肩袖热身。"
}
```

### 场景2：今天练什么

**输入：** 无（主动询问）或 "今天时间只有40分钟"

**记忆调用：**
- 最近3天训练内容（避免部位重复）
- 当前酸痛分布
- 时间约束

**输出示例：**

> **今天建议：拉训练（背+二头）**
> 
> 理由：
> - 前天腿/昨天推，背已经休息48小时
> - 你上周拉的容量偏低，需要补
> - 40分钟刚好完成主项+2个辅助
> 
> **训练单：**
> 1. 引体向上 4组×力竭（预计8-10次）
> 2. 杠铃划船 3组×8 @ 50kg
> 3. 单臂哑铃划船 3组×10 @ 20kg
> 
> 时间预算：35-40分钟

### 场景3：动作替代

**输入：** "没有史密斯机，怎么替代保加利亚蹲？"

**角色：** 训练师

**输出：**

> **替代方案：**
> 
> 原动作：保加利亚蹲（史密斯）
> 替代：哑铃后脚抬高蹲
> 
> **调整要点：**
> - 后脚高度降低（减少髋关节压力）
> - 手持哑铃，重心更易控制
> - 建议重量：单侧12-15kg（参考你史密斯30kg）
> 
> **执行参数：** 3组×10次/腿，休息90秒

### 场景4：康复优先训练（肩）

**输入：** "肩峰撞击，侧平举痛，今天还能练推吗？"

**角色：** 康复师 → 训练师

**输出：**

> **评估结果：暂缓推训练**
> 
> 红线：
> - 侧平举疼痛 = 肩峰下间隙受压
> - 推训练会加剧撞击
> 
> **替代方案：**
> 今天改拉训练（背+二头），推类动作全停
> 
> **康复日安排（训练后做）：**
> 1. 肩袖激活：弹力带外旋 2组×15
> 2. 肩胛稳定：YTWL 1组×10各方向
> 3. 胸小肌松解：筋膜球 2分钟
> 
> **回归推训练标准：**
> - 侧平举无痛
> - 肩环绕无弹响
> - 预计3-5天后重新评估

### 场景5：HYROX专项计划

**输入：** "想准备年底HYROX，现在怎么练？"

**角色：** 运动科学顾问

**输出结构：**
- 能力评估（当前有氧基础、跑步水平）
- 周期划分（基础期→专项期→比赛期）
- Zone2 vs 4×4 vs 混合耐力的配比
- 踝/肩友好的低冲击替代

---

## 8. 一期范围（MVP）

### 8.1 包含功能

| 模块 | 功能 |
|-----|------|
| 训练记录 | 文本输入 + 截图OCR识别 |
| 计划生成 | 周计划 + "今天练什么" |
| 动作库 | 替代动作推荐、执行要点 |
| 康复指导 | 肩/踝/腰的约束判断与改造 |
| 数据看板 | 飞书多维表格可视化 |

### 8.2 明确不做

- ❌ 饮食热量计算
- ❌ 睡眠追踪
- ❌ 体重/体脂曲线
- ❌ 社交功能（打卡/分享）
- ❌ 视频动作指导

---

## 9. 技术栈建议

| 模块 | 技术方案 |
|-----|---------|
| Agent编排 | OpenClaw主Agent + Skill子系统 |
| 截图OCR | 飞书视觉API / Qwen-VL / Claude Vision |
| 数据存储 | PostgreSQL + Redis |
| 飞书集成 | 飞书开放平台API（多维表格+文档+卡片） |
| 后端服务 | Python FastAPI / Node.js |
| 部署 | Docker + 云服务器 |

---

## 10. 待讨论事项

- [ ] Skill详细Prompt设计（各角色的system prompt）
- [ ] OCR方案选型（飞书内置 vs 第三方）
- [ ] 飞书应用权限申请流程
- [ ] 用户 onboarding 流程设计
- [ ] 错误处理机制（OCR失败、意图识别模糊）
- [ ] 多用户隔离与数据安全

---

## 附录：示例对话流

### 对话1：记录训练

**User：** [发送训记截图] 今天卧推容量日

**Agent：**
> 识别到训练记录：
> - 卧推：5组×(60kg×10, 70kg×8, 75kg×6, 70kg×7, 65kg×8)
> - 上斜哑铃卧推：3组×12 @ 22kg
> 
> 总容量：约12,800kg，胸部
> 
> 已记录，同步到飞书表格。

---

### 对话2：询问今天练什么

**User：** 明天练什么？只有45分钟

**Agent：**
> 分析：
> - 昨天：胸（推）
> - 前天：休息
> - 当前状态：无明显酸痛
> 
> **建议：拉训练**
> 
> 45分钟版本：
> 1. 引体向上 4组×力竭
> 2. 杠铃划船 3组×8
> 3. 高位下拉 3组×12
> 4. 二头弯举 2组×15（可选）
> 
> 预估：40-45分钟

---

*文档结束*
