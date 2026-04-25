# DevSmart

DevSmart 是一个 AI 原生的研发流程控制平面。它不做 IDE、代码补全或单一编码 Agent，而是把需求、PRD、任务、上下文、外部 Coding Agent、人工审批、质量建议和审计记录串成一个可控流程。

当前仓库是**文档驱动设计与 POC 规划阶段**，目标是先验证最小闭环，而不是一次性建设完整平台。

## 核心闭环

```text
需求输入 -> PRD 生成/澄清 -> 人工审批 -> 任务拆解 -> 上下文包生成 -> 执行结果回收 -> 质量建议 -> 流程回放
```

## 产品边界

| 不做 | 做 |
|:---|:---|
| IDE 内编码体验 | 研发流程编排 |
| 代码补全 | PRD、任务和上下文生成 |
| 自动替代开发者 | 协调人类开发者与外部 Coding Agent |
| 自动触发 CI/CD | 只读读取 CI 状态并生成建议 |
| 内部推理过程展示 | 展示可审计执行轨迹 |

## 30 天 POC

30 天版本只验证一个问题：DevSmart 能否把一句模糊需求转成可审批 PRD 和可执行任务上下文包。

交付物：

- 任务创建页
- PRD 审批页
- 任务拆解页
- 流程回放页
- PM Agent 初版
- Supervisor 状态机
- 任务上下文包 `task_context.json`

详细计划见 [30 天 POC 详细目标](docs/03-architecture/Thirty_Day_POC_Plan.md)。

## 文档入口

- [PRD](PRD.md)：产品单一事实源。
- [文档地图](docs/README.md)：全部文档导航。
- [POC 实施计划](docs/03-architecture/POC_Implementation_Plan.md)：近期执行依据。
- [技术栈总览](docs/03-architecture/Tech_Stack_Overview.md)：技术选型原则。
- [原型流说明](prototype/PROTOTYPE_FLOW.md)：现有原型资产说明。

## 技术原则

- 编排：LangGraph。
- 后端：FastAPI + Pydantic。
- 前端：React + TypeScript + Vite。
- 模型：使用模型路由，不在业务逻辑中硬编码具体模型。
- 部署：POC 先轻量本地服务，生产阶段再评估云原生。
- CI/CD：按仓库约束，不做自动触发，只做状态读取和人工建议。
