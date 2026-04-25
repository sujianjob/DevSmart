# 总体架构

## 架构目标

支撑从需求到任务上下文包的最小闭环，并为后续外部工具集成、质量建议和审计治理保留扩展点。

## 分层

```text
前端控制台
  -> API 层
  -> 工作流编排层
  -> Agent 能力层
  -> 外部工具 Adapter
  -> 数据与审计层
```

## 核心组件

| 组件 | 职责 |
|:---|:---|
| Web Console | 需求输入、PRD 审批、任务查看、流程回放 |
| FastAPI | API、SSE、Schema 校验 |
| LangGraph | 状态机、HITL、中断恢复 |
| PM Agent | PRD 生成、澄清问题、评审摘要 |
| Coder Agent | 任务控制、上下文包、外部执行结果回收 |
| QA Agent | 测试建议、风险点、人工执行清单 |
| Event Store | 流程事件和审计记录 |

## Coder Agent 定位

Coder Agent 不做 IDE 内编码体验。它负责：

- 生成执行指令。
- 提供任务上下文包。
- 调度人类或外部 Coding Agent。
- 回收 PR、Commit 和执行摘要。
- 记录审计事件。

## 外部集成原则

- GitHub：先读仓库结构，再考虑 PR 状态回收。
- Jira/Linear：先单向创建任务，再考虑双向同步。
- CI：只读状态，不自动触发。
- 模型：通过模型路由选择，不硬编码。
