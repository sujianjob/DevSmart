# 部署与运行边界

## POC 运行方式

POC 阶段优先本地或单机演示。

```text
Frontend
Backend
Local Database
Model Provider
```

## 不做自动 CI/CD

根据仓库约束，构建、测试、发布必须人工操作。DevSmart 本身也不提供自动发布、自动构建或工程流水线能力。

## 环境

| 环境 | 用途 |
|:---|:---|
| local | 本地开发和演示 |
| demo | 内部演示 |
| staging | 后续内测 |

## 生产阶段再评估

- 多空间隔离。
- 高可用。
- 备份恢复。
- 监控告警。
- 合规审计。

这些不进入 30 天 POC。
