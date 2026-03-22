# Fitness Assistant / AIGYM Workspace

当前仓库不是一个已经完成的“FastAPI + PostgreSQL 健身系统”，而是一个**飞书 MVP + 可迁移训练内核**的工作区。

## 当前真实定位

- 飞书：运行壳、表格、日历、文档
- OpenClaw：对话入口与路由层
- Kimi / GPT：可替换模型层
- 飞书多维表：当前运行时结构化真相层
- `fitness-assistant/backend/`：未来适配层骨架，不是当前主运行路径

## 当前核心目标

- 验证训练记录是否可靠
- 验证训练 agent 是否能基于历史做更聪明的调整
- 为未来独立记录器 App 预埋训练内核

## 当前正式能力范围

- 开始训练
- 记录一组
- 修改/删除一组
- 动作替换
- 下一组建议
- 结束训练
- 训练前补给/是否开练
- 4x4 / Zone2 等协议调参

## 目录说明

- `docs/product/`：产品文档与设计真相
- `prompts/`：router 与各 skill prompt
- `schemas/`：核心对象与 skill I/O schema
- `fixtures/`：真实样例与 mock 数据
- `fitness-assistant/backend/`：未来适配层骨架

### 推荐阅读顺序

如果你要更新飞书 / OpenClaw 配置，先看：

1. `docs/product/openclaw-update-playbook.md`
2. `docs/product/training-agent-skill-design.md`
3. `schemas/skill-io.md`
4. `prompts/router.md`
5. `prompts/skills/`

## 关键原则

- 仓库文档优先于飞书后台配置
- 不允许 prompt 记住长期训练状态
- 不允许图片识别直接写入正式记录
- 不允许把飞书表字段当作最终产品模型
