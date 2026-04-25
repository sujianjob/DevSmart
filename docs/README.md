# DevSmart 文档地图

本文档是当前仓库的文档入口。为减少冗余，后续以少数权威文档为准，其他文档只保留摘要、约束或专项说明。

## 权威文档

| 文档 | 用途 |
|:---|:---|
| [README](../README.md) | 项目入口 |
| [PRD](../PRD.md) | 产品单一事实源 |
| [30 天 POC 详细目标](03-architecture/Thirty_Day_POC_Plan.md) | 近期交付范围 |
| [POC 实施计划](03-architecture/POC_Implementation_Plan.md) | 工程执行计划 |
| [技术栈总览](03-architecture/Tech_Stack_Overview.md) | 技术选型原则 |
| [术语表](Glossary.md) | 统一术语 |

## 专项文档

| 分类 | 文档 |
|:---|:---|
| 愿景 | [产品愿景](01-vision/Product_Vision.md)、[AI 原生概念](01-vision/AI_Native_Concept_Paper.md) |
| 产品 | [功能规格](02-product/Feature_Specification.md)、[状态机](02-product/State_Machine_Definition.md)、[指标](02-product/Success_Metrics.md) |
| 架构 | [总体架构](03-architecture/AI_Native_Architecture_Design.md)、[数据模型](03-architecture/Data_Model_Design.md)、[API](03-architecture/API_Specification.md)、[安全与可观测](03-architecture/Security_Observability.md) |
| 原型 | [原型流程](../prototype/PROTOTYPE_FLOW.md) |

## 文档维护规则

- 新事实优先写入 PRD 或 POC 实施计划。
- 不在多个文档重复维护同一套路线图。
- 模型和依赖版本不写死在业务文档中，实施时在依赖文件中锁定。
- 不承诺展示模型内部推理过程。
- 不规划自动触发 CI/CD。
