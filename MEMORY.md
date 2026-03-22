## 2026-03-22

- AIGYM 当前阶段继续使用飞书作为 MVP 运行壳，飞书多维表作为当前运行时结构化真相层。
- 未来一定会做独立记录器 App；当前阶段只预埋训练内核，不做正式 App UI。
- 记录器是长期产品核心，但当前飞书阶段不追求训记级记录体验，只追求记录可靠和 agent 更聪明。
- Kimi / OpenClaw 当前可继续作为运行时模型与对话层，但不再作为架构设计主导。
- 仓库文档被设定为唯一设计真相，线上飞书/OpenClaw 配置后续需要做一次对齐审计。
- 训练核心正式技能集收敛为：
  - start_session
  - log_set
  - amend_set
  - swap_exercise
  - suggest_next_set
  - end_session
  - query_context
  - pre_workout_decision
  - conditioning_protocol_adjust
- 图片输入只作为补充录入；任何图片解析结果默认不能直接入库，必须经过确认。
