# conditioning_protocol_adjust

目标：处理 4x4、Zone2 等有氧协议调参。

必须先读取：

- `protocol_type`
- 当前关键指标（心率、配速、spm、RPE、呼吸反馈）

禁止行为：

- 只盯一个指标给建议
- 忽略安全边界

输出字段：

- `protocol_type`
- `adjustment_action`
- `target_metrics`
- `guardrails`
- `why_short`
