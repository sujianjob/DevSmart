# Agent 框架选型

## 结论

POC 阶段选择 LangGraph。

## 理由

| 要求 | LangGraph 匹配度 |
|:---|:---|
| 状态机 | 高 |
| Human-in-the-Loop | 高 |
| 中断恢复 | 高 |
| 流程可控 | 高 |
| 长链路任务 | 高 |

## 不选其他框架的原因

| 框架 | 暂不采用原因 |
|:---|:---|
| AutoGen | 更偏多 Agent 对话，流程确定性较弱 |
| CrewAI | 封装较重，POC 后期定制成本高 |
| Semantic Kernel | 更适合函数/插件式集成，复杂流程需更多胶水 |
| LlamaIndex Workflows | RAG 能力强，但当前核心是流程控制 |

## 使用边界

- LangGraph 只负责流程状态和编排。
- 业务数据仍由应用层模型管理。
- 模型选择由模型路由处理。
