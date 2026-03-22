"""
Reference router for the future backend/app adapter layer.

Important:
- This file is not the current production OpenClaw runtime.
- It documents the intended task-skill protocol in Python form.
- The current source of truth lives in:
  - prompts/
  - schemas/
  - docs/product/training-agent-skill-design.md
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


SKILLS = {
    "start_session",
    "log_set",
    "bulk_ingest_workout",
    "amend_set",
    "swap_exercise",
    "suggest_next_set",
    "end_session",
    "query_context",
    "pre_workout_decision",
    "conditioning_protocol_adjust",
}


@dataclass
class RouterOutput:
    intent: str
    skill: str
    need_clarification: bool
    missing_fields: List[str] = field(default_factory=list)
    arguments: Dict[str, Any] = field(default_factory=dict)


def route_text(text: str) -> RouterOutput:
    """Tiny reference router used for local reasoning and tests.

    This intentionally stays simple. The real source of truth is the router prompt.
    """
    normalized = text.strip().lower()

    if any(token in normalized for token in ["今天练什么", "开始训练"]):
        return RouterOutput("start_session", "start_session", False)

    if any(token in normalized for token in ["帮我导入", "一堆动作", "训记截图", "导入这张图", "批量导入"]):
        return RouterOutput("bulk_ingest_workout", "bulk_ingest_workout", False)

    if any(token in normalized for token in ["先吃还是先练", "很饿", "先吃晚饭"]):
        return RouterOutput("pre_workout_decision", "pre_workout_decision", False)

    if any(token in normalized for token in ["4x4", "zone2", "zone 2", "spm", "配速", "心率"]):
        return RouterOutput("conditioning_protocol_adjust", "conditioning_protocol_adjust", False)

    if any(token in normalized for token in ["删除最后一组", "改第三组", "修改第"]):
        return RouterOutput("amend_set", "amend_set", False)

    if any(token in normalized for token in ["不舒服", "器械没了", "不练推", "换动作"]):
        return RouterOutput("swap_exercise", "swap_exercise", False)

    if any(token in normalized for token in ["下一组", "要不要加重量", "还要加吗"]):
        return RouterOutput("suggest_next_set", "suggest_next_set", False)

    if any(token in normalized for token in ["做完了", "结束训练", "到这就停"]):
        return RouterOutput("end_session", "end_session", False)

    if any(token in normalized for token in ["趋势", "历史", "最近", "查看"]):
        return RouterOutput("query_context", "query_context", False)

    if any(token in normalized for token in ["kg", "次", "rpe", "×", "x"]):
        return RouterOutput("log_set", "log_set", False)

    return RouterOutput(
        intent="unknown",
        skill="query_context",
        need_clarification=True,
        missing_fields=["intent"],
        arguments={},
    )
