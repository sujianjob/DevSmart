# 部署架构

## POC 部署

POC 阶段优先本地或单机部署。

```text
Frontend (Vite)
Backend (FastAPI)
SQLite / PostgreSQL
LangGraph Checkpointer
```

## 不做自动 CI/CD

根据仓库约束，构建、测试、发布必须人工操作。DevSmart 只读取外部 CI 状态并生成质量建议。

## 环境

| 环境 | 用途 |
|:---|:---|
| local | 本地开发和演示 |
| demo | 内部演示 |
| staging | 后续内测 |

## 生产阶段再评估

- Kubernetes。
- 私有化部署。
- 多租户隔离。
- 高可用。
- 灾备。
- 监控告警。

这些不进入 30 天 POC。
