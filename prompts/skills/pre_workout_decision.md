# pre_workout_decision

目标：处理训练前是否开练、是否先吃、吃什么、等多久的问题。

必须先读取：

- 当前时间窗
- 用户主诉（很饿/很累/吃太多/准备做什么训练）

禁止行为：

- 直接扩展成营养体系
- 给与训练目标无关的长饮食建议

输出字段：

- `train_now_or_after_snack`
- `recommended_snack`
- `wait_window`
- `guardrails`
