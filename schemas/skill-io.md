# Skill I/O

## Router Output

```json
{
  "intent": "log_set",
  "skill": "log_set",
  "need_clarification": false,
  "missing_fields": [],
  "arguments": {}
}
```

## Common Skill Return

```json
{
  "message": "",
  "data": {},
  "confidence": 0.0,
  "needs_confirmation": false,
  "next_actions": [],
  "commit_status": "committed",
  "pending_sync_targets": []
}
```

## Key Skill Fields

- `start_session`
  - `focus`
  - `goal`
  - `available_minutes`
  - `constraints`
  - `plan_items`

- `log_set`
  - `exercise_raw`
  - `exercise_id`
  - `weight`
  - `reps`
  - `rpe`
  - `set_type`
  - `confidence`

- `bulk_ingest_workout`
  - `source_artifact_id`
  - `candidate_entries`
  - `confirmation_mode`
  - `confirmed_entries`
  - `commit_status`
  - `pending_sync_targets`

- `amend_set`
  - `target_set_id`
  - `operation`
  - `updated_fields`

- `suggest_next_set`
  - `action`
  - `recommended_weight`
  - `recommended_reps`
  - `why_short`

- `pre_workout_decision`
  - `hunger_level`
  - `time_to_train`
  - `recommended_snack`
  - `wait_window`

- `conditioning_protocol_adjust`
  - `protocol_type`
  - `current_metrics`
  - `adjustment_action`
  - `guardrails`

## Commit / Projection Rules

- 用户层 skill 只允许直接写主真相对象：
  - `sessions`
  - `sets`
  - `exercise_catalog`
  - `constraints`
- 投影层只能由系统内置提交流程更新：
  - `session_summaries`
  - 飞书日历
  - 飞书文档 / 展示视图
- 投影失败时：
  - `commit_status = pending_sync`
  - `pending_sync_targets = [...]`
