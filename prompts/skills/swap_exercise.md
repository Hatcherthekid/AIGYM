# swap_exercise

目标：在器械限制、疼痛或时间不足时给出替代动作。

必须先读取：

- 当前 session 计划
- exercise_catalog
- constraints

禁止行为：

- 继续安排高风险动作
- 不考虑器械条件
- 输出没有回归门槛的替代建议

输出字段：

- `original_exercise`
- `alternatives`
- `recommended_choice`
- `return_to_original_gate`
