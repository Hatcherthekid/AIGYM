"""
Future ORM models for a later backendized version.

These models are retained as a migration target, not the current Feishu MVP truth.
"""

from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Numeric, 
    JSON, create_engine, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class TrainingLog(Base):
    """Future training log entity."""
    __tablename__ = "training_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, index=True)
    session_id = Column(String(32), index=True)  # 训练日ID
    exercise_name = Column(String(128), nullable=False, index=True)
    body_part = Column(String(64), index=True)  # 胸/背/腿/肩/手臂/核心/有氧
    exercise_type = Column(String(32))  # 主项/辅助/热身/康复
    equipment = Column(String(64))  # 杠铃/哑铃/史密斯/器械/自重
    sets = Column(JSON)  # [{reps: 10, weight: 60, rpe: 8, note: ""}, ...]
    total_volume = Column(Integer)  # 总容量(kg)，自动计算
    duration_minutes = Column(Integer)  # 该动作耗时
    source = Column(String(32))  # ai_ocr/ai_text/manual_edit/manual_new
    version = Column(Integer, default=1)  # 乐观锁版本
    feishu_record_id = Column(String(64))  # 飞书表格记录ID
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_date_body_part', 'date', 'body_part'),
        Index('idx_exercise_date', 'exercise_name', 'date'),
    )


class TrainingSession(Base):
    """Future training session entity."""
    __tablename__ = "training_sessions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, unique=True, index=True)
    theme = Column(String(32))  # 推/拉/腿/有氧/全身/康复/休息
    total_volume = Column(Integer)
    total_sets = Column(Integer)
    total_exercises = Column(Integer)
    duration_minutes = Column(Integer)
    avg_rpe = Column(Numeric(3, 1))
    completion_rate = Column(Numeric(3, 2))  # 计划完成率
    feeling = Column(String(256))  # 主观感受
    feishu_event_id = Column(String(64))  # 飞书日历事件ID
    created_at = Column(DateTime, server_default=func.now())


class ExercisePR(Base):
    """Future exercise PR entity."""
    __tablename__ = "exercise_pr"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_name = Column(String(128), unique=True, nullable=False)
    current_1rm = Column(Numeric(5, 1))  # 估算1RM
    max_weight = Column(Numeric(5, 1))  # 历史最大重量
    max_reps = Column(Integer)  # 最大次数记录
    pr_date = Column(Date)  # PR日期
    trend_30d = Column(String(16))  # up/down/stable
    last_session_date = Column(Date)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class UserSnapshot(Base):
    """Future user snapshot entity."""
    __tablename__ = "user_snapshot"
    
    id = Column(Integer, primary_key=True, default=1)  # 只有一条记录
    last_training_date = Column(Date)
    current_streak = Column(Integer, default=0)  # 连续训练天数
    weekly_volume = Column(JSON)  # 本周各部位容量
    monthly_volume = Column(JSON)  # 近4周容量
    current_constraints = Column(JSON)  # 当前约束（伤病/器械）
    soreness_map = Column(JSON)  # 酸痛分布
    next_planned_date = Column(Date)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class SyncLog(Base):
    """Future sync log entity."""
    __tablename__ = "sync_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    direction = Column(String(16))  # feishu_to_db / db_to_feishu
    table_name = Column(String(64))
    record_id = Column(Integer)
    action = Column(String(16))  # create/update/delete
    status = Column(String(16))  # success/failed/pending
    error_msg = Column(String(512))
    created_at = Column(DateTime, server_default=func.now())


class OfflineQueue(Base):
    """Future offline queue entity."""
    __tablename__ = "offline_queue"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    operation = Column(String(16))  # create/update/delete
    table_name = Column(String(64))
    payload = Column(JSON)  # 完整数据
    retry_count = Column(Integer, default=0)
    status = Column(String(16), default='pending')  # pending/processing/failed
    created_at = Column(DateTime, server_default=func.now())
