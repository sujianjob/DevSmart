# DevSmart 文档地图

本文档是当前仓库的文档入口。后续以少数权威文档为准，其他文档只保留摘要、约束或专项说明。

## 权威文档

| 文档 | 用途 |
|:---|:---|
| [README](../README.md) | 项目入口 |
| [PRD](../PRD.md) | 产品单一事实源 |
| [30 天 POC 详细目标](03-architecture/Thirty_Day_POC_Plan.md) | 近期交付范围 |
| [POC 实施计划](03-architecture/POC_Implementation_Plan.md) | 实施顺序 |
| [能力边界说明](03-architecture/Tech_Stack_Overview.md) | 实现与配置边界 |
| [术语表](Glossary.md) | 统一术语 |

## 专项文档

| 分类 | 文档 |
|:---|:---|
| 愿景 | [产品愿景](01-vision/Product_Vision.md)、[AI 原生需求工作流](01-vision/AI_Native_Concept_Paper.md) |
| 产品 | [功能规格](02-product/Feature_Specification.md)、[状态机](02-product/State_Machine_Definition.md)、[指标](02-product/Success_Metrics.md) |
| 实施 | [产品工作流](03-architecture/AI_Native_Architecture_Design.md)、[数据模型](03-architecture/Data_Model_Design.md)、[输出结构](03-architecture/API_Specification.md)、[安全与可观测](03-architecture/Security_Observability.md) |
| 原型 | [原型流程](../prototype/PROTOTYPE_FLOW.md) |

## 文档维护规则

- 新事实优先写入 PRD 或 POC 实施计划。
- 不在多个文档重复维护同一套路线图。
- 不把技术实现、接口设计或研发执行写入产品范围。
- 不承诺展示模型内部推理过程。
- 不规划自动触发 CI/CD。
