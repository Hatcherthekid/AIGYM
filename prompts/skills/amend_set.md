# amend_set

目标：定位并修改或删除某一组训练记录。

必须先读取：

- active session 最近 sets
- 相关动作最近写入记录

禁止行为：

- 没定位到目标 set 就修改
- 把“最后一组”理解成任意一组

输出字段：

- `target_set_id`
- `operation`
- `updated_fields`
- `confidence`
- `needs_confirmation`
