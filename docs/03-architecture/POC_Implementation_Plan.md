# POC 实施计划

> 详细 30 天拆解见 [30 天 POC 详细目标](Thirty_Day_POC_Plan.md)。

## 目标

交付 AI 研发流程指挥中心 POC，跑通：

```text
需求输入 -> PRD 生成/澄清 -> 人工审批 -> 任务拆解 -> 上下文包生成 -> 流程回放
```

## 工程任务

### 1. 后端

- 初始化 FastAPI。
- 定义 Task、PRD、ContextPackage、WorkflowEvent、Approval Schema。
- 实现 LangGraph 状态机。
- 实现 SSE 事件输出。

### 2. Agent

- PM Agent：生成 PRD 和澄清问题。
- Supervisor：控制状态流转。
- Coder Agent：拆任务并生成上下文包。

### 3. 前端

- 任务创建页。
- PRD 审批页。
- 任务拆解页。
- 流程回放页。

### 4. 验证

- 单元测试：Agent 节点和 Schema。
- 集成测试：审批通过路径和驳回重试路径。
- 手工演示：至少 5 个示例需求。

## 成功指标

| 指标 | 目标 |
|:---|:---|
| PRD 生成成功率 | ≥ 80% |
| PRD 初稿可采纳率 | ≥ 50% |
| 任务拆解可采纳率 | ≥ 60% |
| 从需求到任务包耗时 | ≤ 10 分钟 |
