# 技术栈总览

## POC 技术栈

| 层级 | 技术 | 用途 |
|:---|:---|:---|
| 前端 | React + TypeScript + Vite | 任务指挥中心 |
| 后端 | FastAPI + Pydantic | API、SSE、Schema 校验 |
| 编排 | LangGraph | 状态机、HITL、中断恢复 |
| 存储 | SQLite / PostgreSQL | 任务、事件、审批、上下文包 |
| 模型 | 模型路由 | PRD、任务拆解、摘要和建议 |

## 模型路由

不在业务逻辑中硬编码具体模型。

| 路由 | 用途 |
|:---|:---|
| `reasoning-model` | PRD、澄清、评审摘要 |
| `code-model` | 代码上下文、PR 摘要 |
| `low-cost-model` | 分类、摘要、格式化 |
| `private-model` | 私有化和敏感项目 |

## 暂不引入

- Kubernetes。
- ArgoCD。
- Milvus。
- Neo4j。
- 完整多租户权限。
- 自动 CI/CD。

## 版本原则

- 实施时使用最新稳定版。
- 在依赖文件中锁定具体版本。
- 记录验证日期。
- 文档只描述原则，不维护容易过时的小版本号。
