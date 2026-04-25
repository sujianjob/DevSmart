# 术语表

| 术语 | 定义 |
|:---|:---|
| DevSmart | AI 原生研发流程控制平面 |
| PRD | 产品需求文档 |
| PM Agent | 生成 PRD、澄清问题和评审摘要的 Agent |
| Supervisor | 控制流程状态和 Agent 调度的编排节点 |
| Coder Agent | 研发任务控制与上下文协调器 |
| QA Agent | 生成测试建议、风险点和人工执行清单的 Agent |
| Context Package | 面向人类开发者或外部 Coding Agent 的任务上下文包 |
| HITL | Human-in-the-Loop，人工审批和中断恢复机制 |
| WorkflowRun | 一次从需求到上下文包的完整流程 |
| WorkflowEvent | 状态变化、工具调用、审批和产物摘要 |
| 模型路由 | 按任务类型选择模型，不在业务逻辑中硬编码具体模型 |
| CI 状态读取 | 只读读取流水线状态，不自动触发构建、测试、发布 |
| 流程回放 | 展示可审计事件，不展示模型内部推理链 |
