# bulk_ingest_workout

目标：处理多动作、多组训练记录的批量导入。

适用输入：

- 一次性发一堆动作和组数
- 训记截图
- 设备屏幕图或其他批量训练记录来源

必须先读取：

- active session
- 当前训练 focus
- exercise_catalog

禁止行为：

- 未确认就直接写正式 `Set`
- 从模糊图片补齐不存在的数据
- 识别结果明显异常时继续整批提交

必须输出：

- `source_artifact_id`
- `candidate_entries`
- `confirmation_mode`
- `confirmed_entries`
- `commit_status`
- `pending_sync_targets`

确认原则：

- 支持逐动作确认
- 支持整批确认
- 动作、重量、次数异常时默认退回确认态
