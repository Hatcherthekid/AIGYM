# log_set

目标：把文本输入或图片导入候选解析成单组训练记录。

必须先读取：

- active session
- 当前动作最近 sets
- exercise_catalog 候选

禁止行为：

- 不确定动作时直接写正式记录
- 不确定组数时擅自批量生成
- 从模糊图片补齐不存在的重量、次数、动作

当以下情况出现时必须要求确认：

- 动作映射置信度低
- 识别结果与当前 focus 明显冲突
- 图片导入结果异常

输出字段：

- `exercise_raw`
- `exercise_id`
- `exercise_name`
- `weight`
- `reps`
- `rpe`
- `set_type`
- `note`
- `confidence`
- `needs_confirmation`
