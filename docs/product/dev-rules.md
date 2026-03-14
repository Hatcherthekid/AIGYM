# 健身助手项目开发规则

> 基于 `rules/product/prd_policy.md` + `rules/dev/iteration_and_pm.md` 定制
> 适用：本项目所有开发活动

---

## 1. 开发准入门槛（Hard Rules）

### Rule 1：需求不清，禁止开工
```
IF 请求存在以下任一情况：
  - 目标不明确（"做个功能"但没有具体描述）
  - 范围模糊（"大概这样"但没有边界）
  - 验收标准缺失（"好了告诉我"但没有具体标准）
THEN 
  必须反问澄清，直到满足PRD Policy的最小字段
  禁止直接开始编码
```

### Rule 2：无文档不开发
```
IF 以下任一文档缺失或不完整：
  - PRD（`docs/product/*-prd.md`）
  - Backlog（`docs/product/backlog.md`）
  - 相关决策记录（`docs/product/decisions.md`）
THEN
  必须先补文档，再进入开发
  禁止"先做着看看"
```

### Rule 3：任务必须可验收
```
IF Backlog中的任务不满足：
  - 有明确的入口（文件/脚本/页面路径）
  - 有明确的验收标准（命令/输出/状态）
THEN
  必须退回补充，不得标记为doing
```

---

## 2. 迭代工作流程

### 2.1 迭代启动前
- [ ] 确认本次迭代的Goal（1-3条）
- [ ] 从Backlog的"Now"栏选取任务
- [ ] 更新迭代日志（Goal/预期Done/Verification）

### 2.2 迭代进行中
- [ ] 每个任务开始前，确认验收标准
- [ ] 开发完成后，按验收标准自测
- [ ] 更新Backlog状态（todo → doing → done）

### 2.3 迭代结束时
- [ ] 填写迭代日志（Done/Not done/Verification/Next）
- [ ] 更新"复盘笔记"
- [ ] 移动Backlog任务（Now → 已完成 / Next → Now）

---

## 3. 文档更新触发条件

| 场景 | 必须更新的文档 | 更新内容 |
|-----|--------------|---------|
| 范围/功能变更 | PRD + Backlog | 调整Scope和checklist |
| 技术方案变更 | 决策记录(ADR) | 记录Problem/Decision/Rationale |
| 任务状态变化 | Backlog | 更新status |
| 迭代完成 | 迭代日志 | Goal/Done/Not done/Next |
| 发现新问题 | 决策记录 | 添加到"待决策" |

---

## 4. 反问模板（当需求不清时）

### 场景A：目标不明确
```
"我需要确认几个点：
1. 这个功能解决什么问题？
2. 用户是谁？在什么场景下使用？
3. 不做这个会有什么影响？"
```

### 场景B：范围模糊
```
"请帮我明确边界：
1. 这个功能的输入是什么？输出是什么？
2. 有哪些明确不做（Out of scope）？
3. 和其他功能的关系是什么？"
```

### 场景C：验收标准缺失
```
"怎么算完成了？请提供：
1. 验证步骤（命令/操作路径）
2. 预期结果（输出/状态/现象）
3. 如果有界面，截图或描述预期样子"
```

---

## 5. 自检清单（每次开发前默念）

- [ ] 我理解这个需求的目标吗？
- [ ] 我知道范围边界吗？（做什么/不做什么）
- [ ] 我知道怎么验收吗？（命令/输出/状态）
- [ ] 相关文档存在且更新了吗？
- [ ] Backlog里有这个任务吗？状态对吗？

**如果任一答案是"否" → 停止开发，先补文档/澄清**

---

## 6. 项目文档索引

| 文档 | 路径 | 用途 |
|-----|------|------|
| PRD | `docs/product/fitness-assistant-prd.md` | 需求定义、范围、验收标准 |
| Backlog | `docs/product/backlog.md` | 可执行任务清单 |
| 迭代日志 | `docs/product/iteration-log.md` | 迭代记录、复盘 |
| 决策记录 | `docs/product/decisions.md` | ADR-lite、待决策事项 |
| 系统架构 | `docs/fitness-system-architecture.md` | 技术设计、Schema、API |
| 开发规则 | `docs/product/dev-rules.md` | 本文件 |

---

*规则版本：v1.0 | 创建：2026-03-13*
