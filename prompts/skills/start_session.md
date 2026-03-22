# start_session

目标：根据最近训练历史、当前限制条件和时间预算生成一份今日训练草案，并决定是否创建或更新 active session。

必须先读取：

- 最近 3 次 session
- 当前 active session
- 当前 constraints

禁止行为：

- 不查历史直接给计划
- 忽略当前伤病/时间限制
- 输出过长背景分析

输出字段：

- `focus`
- `goal`
- `available_minutes`
- `constraints`
- `plan_items`
- `rationale_short`
- `create_or_update_session`
