"""
训练记录 API 路由
CRUD 操作
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid

from database import get_db
from models.training import TrainingLog

router = APIRouter()


# ============ 数据模型 ============

class SetData(BaseModel):
    reps: int
    weight: float
    rpe: Optional[int] = None
    note: Optional[str] = None


class TrainingLogCreate(BaseModel):
    date: date
    exercise_name: str
    body_part: str
    exercise_type: Optional[str] = "主项"
    equipment: Optional[str] = "杠铃"
    sets: List[SetData]
    duration_minutes: Optional[int] = None
    source: Optional[str] = "manual_new"


class TrainingLogResponse(BaseModel):
    id: int
    date: date
    exercise_name: str
    body_part: str
    total_volume: int
    source: str
    created_at: str
    
    class Config:
        from_attributes = True


class TrainingLogUpdate(BaseModel):
    exercise_name: Optional[str] = None
    body_part: Optional[str] = None
    sets: Optional[List[SetData]] = None
    duration_minutes: Optional[int] = None
    version: int  # 乐观锁版本


# ============ API 端点 ============

@router.post("/logs", response_model=dict)
async def create_training_log(log: TrainingLogCreate, db: Session = Depends(get_db)):
    """创建训练记录"""
    # 计算总容量
    total_volume = sum(s.weight * s.reps for s in log.sets)
    
    # 生成 session_id（简单实现：日期字符串）
    session_id = log.date.strftime("%Y%m%d")
    
    # 创建数据库记录
    db_log = TrainingLog(
        date=log.date,
        session_id=session_id,
        exercise_name=log.exercise_name,
        body_part=log.body_part,
        exercise_type=log.exercise_type,
        equipment=log.equipment,
        sets=[s.model_dump() for s in log.sets],
        total_volume=total_volume,
        duration_minutes=log.duration_minutes,
        source=log.source,
        version=1
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return {
        "id": db_log.id,
        "total_volume": total_volume,
        "sync_status": "pending",
        "message": "训练记录已创建（待同步到飞书）"
    }


@router.get("/logs", response_model=List[TrainingLogResponse])
async def list_training_logs(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    body_part: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """查询训练记录列表"""
    query = db.query(TrainingLog)
    
    if start_date:
        query = query.filter(TrainingLog.date >= start_date)
    if end_date:
        query = query.filter(TrainingLog.date <= end_date)
    if body_part:
        query = query.filter(TrainingLog.body_part == body_part)
    
    logs = query.order_by(desc(TrainingLog.date)).limit(limit).all()
    
    return [
        TrainingLogResponse(
            id=log.id,
            date=log.date,
            exercise_name=log.exercise_name,
            body_part=log.body_part,
            total_volume=log.total_volume or 0,
            source=log.source,
            created_at=log.created_at.isoformat() if log.created_at else ""
        )
        for log in logs
    ]


@router.get("/logs/{log_id}", response_model=dict)
async def get_training_log(log_id: int, db: Session = Depends(get_db)):
    """获取单条训练记录"""
    log = db.query(TrainingLog).filter(TrainingLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    return {
        "id": log.id,
        "date": log.date.isoformat(),
        "session_id": log.session_id,
        "exercise_name": log.exercise_name,
        "body_part": log.body_part,
        "exercise_type": log.exercise_type,
        "equipment": log.equipment,
        "sets": log.sets,
        "total_volume": log.total_volume,
        "duration_minutes": log.duration_minutes,
        "source": log.source,
        "version": log.version,
        "created_at": log.created_at.isoformat() if log.created_at else None,
        "updated_at": log.updated_at.isoformat() if log.updated_at else None
    }


@router.put("/logs/{log_id}")
async def update_training_log(log_id: int, log_update: TrainingLogUpdate, db: Session = Depends(get_db)):
    """更新训练记录（支持乐观锁）"""
    db_log = db.query(TrainingLog).filter(TrainingLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    # 乐观锁版本检查
    if db_log.version != log_update.version:
        raise HTTPException(
            status_code=409,
            detail=f"版本冲突：当前版本 {db_log.version}，请求版本 {log_update.version}"
        )
    
    # 更新字段
    if log_update.exercise_name:
        db_log.exercise_name = log_update.exercise_name
    if log_update.body_part:
        db_log.body_part = log_update.body_part
    if log_update.sets:
        db_log.sets = [s.model_dump() for s in log_update.sets]
        db_log.total_volume = sum(s.weight * s.reps for s in log_update.sets)
    if log_update.duration_minutes is not None:
        db_log.duration_minutes = log_update.duration_minutes
    
    # 版本号+1
    db_log.version += 1
    
    db.commit()
    db.refresh(db_log)
    
    return {
        "success": True,
        "new_version": db_log.version,
        "message": "记录已更新"
    }


@router.delete("/logs/{log_id}")
async def delete_training_log(log_id: int, db: Session = Depends(get_db)):
    """删除训练记录"""
    db_log = db.query(TrainingLog).filter(TrainingLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    db.delete(db_log)
    db.commit()
    
    return {"success": True, "message": "记录已删除"}


@router.get("/summary")
async def get_training_summary(
    period: str = Query("7d", regex="^(7d|30d|90d)$"),
    db: Session = Depends(get_db)
):
    """获取训练汇总统计"""
    from datetime import datetime, timedelta
    
    days = int(period[:-1])
    start = datetime.now().date() - timedelta(days=days)
    
    query = db.query(TrainingLog).filter(TrainingLog.date >= start)
    logs = query.all()
    
    # 统计
    total_volume = sum(log.total_volume or 0 for log in logs)
    total_sets = sum(len(log.sets) if log.sets else 0 for log in logs)
    unique_dates = len(set(log.date for log in logs))
    
    # 按部位统计
    body_part_stats = {}
    for log in logs:
        bp = log.body_part
        if bp not in body_part_stats:
            body_part_stats[bp] = {"volume": 0, "count": 0}
        body_part_stats[bp]["volume"] += log.total_volume or 0
        body_part_stats[bp]["count"] += 1
    
    return {
        "period": period,
        "total_sessions": unique_dates,
        "total_exercises": len(logs),
        "total_volume": total_volume,
        "total_sets": total_sets,
        "body_part_stats": body_part_stats
    }
