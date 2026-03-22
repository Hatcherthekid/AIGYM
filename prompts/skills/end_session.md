# end_session

目标：结束当前训练并生成短复盘。

必须先读取：

- active session
- 本次 session 所有 sets
- 最近一次同类 session

禁止行为：

- 没有结构化对比就声称有进步
- 输出泛泛鼓励

输出字段：

- `completed_overview`
- `comparison_to_last`
- `cool_down_actions`
- `next_time_note`
