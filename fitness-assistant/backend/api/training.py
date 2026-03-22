"""
Future training API sketch.

This module is intentionally kept as a backend-adapter placeholder.
It does not describe the current production path of the Feishu MVP.

Current source of truth:
- prompts/
- schemas/
- docs/product/training-agent-skill-design.md
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/reference")
async def training_api_reference():
    """Return the intended capability surface for a future backend."""
    return {
        "status": "reference_only",
        "capabilities": [
            "start_session",
            "log_set",
            "amend_set",
            "swap_exercise",
            "suggest_next_set",
            "end_session",
            "query_context",
            "pre_workout_decision",
            "conditioning_protocol_adjust",
        ],
        "note": "Current Feishu MVP runs on Feishu tables + OpenClaw, not this backend module.",
    }
