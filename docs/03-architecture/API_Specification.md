# API 规格

## POC API

| 方法 | 路径 | 用途 |
|:---|:---|:---|
| `POST` | `/tasks` | 创建需求任务 |
| `GET` | `/tasks/{task_id}` | 查询任务详情 |
| `GET` | `/tasks/{task_id}/events` | 读取任务事件 |
| `POST` | `/tasks/{task_id}/approve` | 批准当前 PRD |
| `POST` | `/tasks/{task_id}/reject` | 驳回当前 PRD |
| `GET` | `/tasks/{task_id}/context-packages` | 获取上下文包 |

## 创建任务

请求：

```json
{
  "requirement": "支持团队成员邮箱邀请",
  "project_context": {
    "tech_stack": ["React", "FastAPI"],
    "constraints": ["必须支持邀请过期"]
  }
}
```

响应：

```json
{
  "task_id": "task_001",
  "status": "created"
}
```

## 审批 PRD

```json
{
  "approved": true,
  "comments": "同意进入任务拆解"
}
```

## 驳回 PRD

```json
{
  "reason": "缺少重复邀请处理",
  "comments": "请补充邀请过期、重复邀请和权限边界"
}
```

## 事件结构

```json
{
  "event_id": "evt_001",
  "task_id": "task_001",
  "event_type": "prd_generated",
  "actor": "pm_agent",
  "input_summary": "用户输入团队邀请需求",
  "output_summary": "生成 PRD 初稿",
  "created_at": "2026-04-25T10:00:00Z"
}
```

## 约束

- API 不返回模型内部推理过程。
- 模型字段使用路由别名，如 `reasoning-model`、`code-model`。
- POC 阶段不提供公开外部 API Key。
