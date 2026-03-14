"""
飞书 Webhook 接收端
处理飞书表格的变更通知
"""

from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
import json

router = APIRouter()


@router.post("/feishu")
async def handle_feishu_webhook(
    request: Request,
    x_feishu_token: Optional[str] = Header(None),
    x_feishu_timestamp: Optional[str] = Header(None),
    x_feishu_signature: Optional[str] = Header(None)
):
    """
    接收飞书Webhook事件
    
    事件类型：
    - record.created: 新建记录
    - record.updated: 修改记录
    - record.deleted: 删除记录
    """
    body = await request.body()
    
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # 验证签名（生产环境需要）
    # if not verify_signature(x_feishu_token, x_feishu_timestamp, x_feishu_signature, body):
    #     raise HTTPException(status_code=401, detail="Invalid signature")
    
    # 处理挑战请求（飞书Webhook验证）
    if "challenge" in data:
        return {"challenge": data["challenge"]}
    
    event_type = data.get("header", {}).get("event_type")
    
    if event_type == "record.created":
        await handle_record_created(data.get("event", {}))
    elif event_type == "record.updated":
        await handle_record_updated(data.get("event", {}))
    elif event_type == "record.deleted":
        await handle_record_deleted(data.get("event", {}))
    else:
        print(f"未处理的事件类型: {event_type}")
    
    return {"status": "ok"}


async def handle_record_created(event: dict):
    """处理新建记录"""
    table_id = event.get("table_id")
    record = event.get("record", {})
    
    print(f"[Webhook] 新建记录: table={table_id}, record={record.get('record_id')}")
    # TODO: 写入本地数据库
    return True


async def handle_record_updated(event: dict):
    """处理更新记录"""
    table_id = event.get("table_id")
    record = event.get("record", {})
    
    print(f"[Webhook] 更新记录: table={table_id}, record={record.get('record_id')}")
    # TODO: 更新本地数据库
    return True


async def handle_record_deleted(event: dict):
    """处理删除记录"""
    table_id = event.get("table_id")
    record_id = event.get("record_id")
    
    print(f"[Webhook] 删除记录: table={table_id}, record={record_id}")
    # TODO: 删除本地记录
    return True


def verify_signature(token: str, timestamp: str, signature: str, body: bytes) -> bool:
    """验证飞书Webhook签名"""
    import hmac
    import hashlib
    
    # 从环境变量获取Encrypt Key
    encrypt_key = "your_encrypt_key"  # TODO: 从配置读取
    
    # 计算签名
    string_to_sign = f"{timestamp}\n{encrypt_key}\n{body.decode()}\n"
    expected_signature = hmac.new(
        encrypt_key.encode(),
        string_to_sign.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return signature == expected_signature
