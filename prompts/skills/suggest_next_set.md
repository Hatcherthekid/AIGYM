# suggest_next_set

目标：根据当前动作表现给出下一组建议。

必须先读取：

- 当前动作本次已完成 sets
- 该动作最近历史
- 用户当前反馈

禁止行为：

- 没看当前表现就建议加重
- 只给理论，不给动作级建议

输出字段：

- `action`
- `recommended_weight`
- `recommended_reps`
- `recommended_tempo`
- `why_short`
