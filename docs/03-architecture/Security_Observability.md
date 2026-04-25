# 安全与可观测性

## 安全底线

- Access Token 只存前端内存，不持久化到 localStorage。
- Refresh Token 使用 HttpOnly Cookie。
- 不记录明文密钥。
- 不上传不必要的源码全文。
- AI 推测内容必须标记。
- CI/CD 不自动触发。

## 审计事件

每个关键动作都记录为 `WorkflowEvent`：

- 创建任务。
- 生成 PRD。
- 生成澄清问题。
- 审批通过。
- 审批驳回。
- 拆解任务。
- 生成上下文包。
- 回收外部执行结果。

## 可观测性

POC 阶段记录：

- 请求耗时。
- 模型路由别名。
- Token 用量。
- 任务状态耗时。
- 错误摘要。

不记录模型内部推理过程。

## 后续扩展

- OpenTelemetry。
- Grafana。
- Loki。
- LangSmith 或自建 LLM Trace。
- 企业审计报表。
