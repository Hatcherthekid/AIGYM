"""
Future event/webhook adapter sketch.

This file is intentionally retained as a placeholder for a later backendized version.
It is not the current source of truth for the Feishu MVP runtime.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/reference")
async def webhook_reference():
    return {
        "status": "reference_only",
        "note": "Current runtime behavior is defined in repo docs and OpenClaw/Feishu configuration.",
    }
