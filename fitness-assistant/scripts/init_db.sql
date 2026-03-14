-- 健身助手数据库初始化脚本
-- 创建数据库: CREATE DATABASE fitness;

-- 训练记录表
CREATE TABLE IF NOT EXISTS training_logs (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    session_id VARCHAR(32),
    exercise_name VARCHAR(128) NOT NULL,
    body_part VARCHAR(64),
    exercise_type VARCHAR(32),
    equipment VARCHAR(64),
    sets JSONB,
    total_volume INTEGER,
    duration_minutes INTEGER,
    source VARCHAR(32),
    version INTEGER DEFAULT 1,
    feishu_record_id VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_training_logs_date ON training_logs(date);
CREATE INDEX IF NOT EXISTS idx_training_logs_session ON training_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_training_logs_exercise ON training_logs(exercise_name);
CREATE INDEX IF NOT EXISTS idx_training_logs_body_part ON training_logs(body_part);
CREATE INDEX IF NOT EXISTS idx_training_logs_date_body_part ON training_logs(date, body_part);
CREATE INDEX IF NOT EXISTS idx_training_logs_exercise_date ON training_logs(exercise_name, date);

-- 训练日汇总表
CREATE TABLE IF NOT EXISTS training_sessions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    theme VARCHAR(32),
    total_volume INTEGER,
    total_sets INTEGER,
    total_exercises INTEGER,
    duration_minutes INTEGER,
    avg_rpe NUMERIC(3,1),
    completion_rate NUMERIC(3,2),
    feeling VARCHAR(256),
    feishu_event_id VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_training_sessions_date ON training_sessions(date);

-- 动作PR追踪表
CREATE TABLE IF NOT EXISTS exercise_pr (
    id SERIAL PRIMARY KEY,
    exercise_name VARCHAR(128) UNIQUE NOT NULL,
    current_1rm NUMERIC(5,1),
    max_weight NUMERIC(5,1),
    max_reps INTEGER,
    pr_date DATE,
    trend_30d VARCHAR(16),
    last_session_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户状态快照表（单用户只有一条记录）
CREATE TABLE IF NOT EXISTS user_snapshot (
    id INTEGER PRIMARY KEY DEFAULT 1,
    last_training_date DATE,
    current_streak INTEGER DEFAULT 0,
    weekly_volume JSONB,
    monthly_volume JSONB,
    current_constraints JSONB,
    soreness_map JSONB,
    next_planned_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 同步日志表
CREATE TABLE IF NOT EXISTS sync_log (
    id SERIAL PRIMARY KEY,
    direction VARCHAR(16),
    table_name VARCHAR(64),
    record_id INTEGER,
    action VARCHAR(16),
    status VARCHAR(16),
    error_msg VARCHAR(512),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 离线队列表
CREATE TABLE IF NOT EXISTS offline_queue (
    id SERIAL PRIMARY KEY,
    operation VARCHAR(16),
    table_name VARCHAR(64),
    payload JSONB,
    retry_count INTEGER DEFAULT 0,
    status VARCHAR(16) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 更新时间戳触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要自动更新 updated_at 的表添加触发器
DROP TRIGGER IF EXISTS update_training_logs_updated_at ON training_logs;
CREATE TRIGGER update_training_logs_updated_at
    BEFORE UPDATE ON training_logs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_exercise_pr_updated_at ON exercise_pr;
CREATE TRIGGER update_exercise_pr_updated_at
    BEFORE UPDATE ON exercise_pr
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_snapshot_updated_at ON user_snapshot;
CREATE TRIGGER update_user_snapshot_updated_at
    BEFORE UPDATE ON user_snapshot
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 插入默认用户快照
INSERT INTO user_snapshot (id, current_streak) 
VALUES (1, 0) 
ON CONFLICT (id) DO NOTHING;
