"""
训练记录 API 路由
CRUD 操作
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

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


class TrainingLogUpdate(BaseModel):
    exercise_name: Optional[str] = None
    body_part: Optional[str] = None
    sets: Optional[List[SetData]] = None
    duration_minutes: Optional[int] = None
    version: int  # 乐观锁版本


# ============ API 端点 ============

@router.post("/logs", response_model=dict)
async def create_training_log(log: TrainingLogCreate):
    """创建训练记录"""
    # 计算总容量
    total_volume = sum(s.weight * s.reps for s in log.sets)
    
    # TODO: 存入数据库
    return {
        "id": 1,  # 模拟返回
        "feishu_record_id": "rec_xxx",
        "total_volume": total_volume,
        "sync_status": "pending",
        "message": "训练记录已创建（待同步到飞书）"
    }


@router.get("/logs", response_model=List[TrainingLogResponse])
async def list_training_logs(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    body_part: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500)
):
    """查询训练记录列表"""
    # TODO: 从数据库查询
    return []


@router.get("/logs/{log_id}", response_model=dict)
async def get_training_log(log_id: int):
    """获取单条训练记录"""
    # TODO: 从数据库查询
    return {"id": log_id, "message": "Not implemented"}


@router.put("/logs/{log_id}")
async def update_training_log(log_id: int, log: TrainingLogUpdate):
    """更新训练记录（支持乐观锁）"""
    # TODO: 实现乐观锁版本检查
    return {
        "success": True,
        "new_version": log.version + 1,
        "message": "记录已更新"
    }


@router.delete("/logs/{log_id}")
async def delete_training_log(log_id: int):
    """删除训练记录"""
    return {"success": True, "message": "记录已删除"}


@router.get("/summary")
async def get_training_summary(
    period: str = Query("7d", regex="^(7d|30d|90d)$")
):
    """获取训练汇总统计"""
    return {
        "period": period,
        "total_sessions": 0,
        "total_volume": 0,
        "message": "Not implemented"
    }
