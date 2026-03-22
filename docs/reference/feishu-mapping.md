# Feishu Mapping Notes

当前飞书只做运行时映射，不定义长期产品真相。

## Required Tables

- `sessions`
- `sets`
- `exercise_catalog`
- `constraints`
- `session_summaries`

## Mapping Principles

- 日历只映射 session 级信息
- 文档只映射 summary 级信息
- 图片导入先到候选确认态，不直接入 `sets`
- 飞书字段命名可以适配，但对象含义以仓库 schema 为准

## Direct Write vs Projection

### 允许被 skill 直接写的主真相表

- `sessions`
- `sets`
- `exercise_catalog`
- `constraints`

### 只能由投影流程更新的目标

- `session_summaries`
- 飞书日历
- 飞书文档 / 展示视图

## Commit Rules

- skill 先提交主真相对象
- 提交成功后，同步关键投影
- 投影失败时，必须标记 `pending_sync`
- 不允许用户层 skill 单独改日历但不改主真相表
