# Core Models

## Session

```json
{
  "session_id": "20260322-UPPER-001",
  "date": "2026-03-22",
  "status": "active",
  "focus": "upper",
  "goal": "upper hypertrophy with shoulder rehab",
  "available_minutes": 40,
  "constraints": ["shoulder_pain", "ankle_rehab"]
}
```

## Set

```json
{
  "set_id": "set_001",
  "session_id": "20260322-UPPER-001",
  "exercise_raw": "下拉",
  "exercise_id": "lat_pulldown",
  "exercise_name": "高位下拉",
  "set_index": 1,
  "weight": 26,
  "reps": 10,
  "rpe": 7,
  "set_type": "working",
  "note": "手臂累，背没感觉",
  "source": "text",
  "confidence": 0.93,
  "status": "active"
}
```

## Exercise

```json
{
  "exercise_id": "lat_pulldown",
  "canonical_name": "高位下拉",
  "aliases": ["下拉", "高位下拉"],
  "movement_pattern": "pull",
  "equipment": ["cable"],
  "swap_candidates": ["band_pulldown", "ring_row"]
}
```

## Constraint

```json
{
  "constraint_id": "constraint_001",
  "type": "pain",
  "body_area": "shoulder",
  "severity": "medium",
  "detail": "推的时候不舒服",
  "status": "active"
}
```

## SessionSummary

```json
{
  "summary_id": "summary_001",
  "session_id": "20260322-UPPER-001",
  "completed_overview": "完成拉训练+核心+肩踝康复",
  "comparison_to_last": "下拉动作质量更好，但引体后程掉速明显",
  "next_time_note": "下次引体前3组别冲爆"
}
```

## SourceArtifact

```json
{
  "artifact_id": "artifact_001",
  "artifact_type": "image",
  "import_status": "pending_review",
  "source_label": "训记截图",
  "candidate_count": 6
}
```
