# DevSmart API 接口规范

本文档定义了 DevSmart 平台的 RESTful API 接口规范，包括认证、核心资源操作和实时通信接口。

---

## 1. 概述

### 1.1 基本信息

| 项目 | 说明 |
|:---|:---|
| **Base URL** | `https://api.devsmart.io/v1` |
| **协议** | HTTPS (TLS 1.3) |
| **认证方式** | Bearer Token (JWT) / API Key |
| **响应格式** | JSON |
| **字符编码** | UTF-8 |

### 1.2 通用请求头

```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
Accept: application/json
X-Request-ID: <uuid>  # 可选，用于请求追踪
```

### 1.3 通用响应格式

**成功响应**：
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**分页响应**：
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

**错误响应**：
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数错误",
    "details": [
      { "field": "title", "message": "标题不能为空" }
    ]
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## 2. 认证接口

### 2.1 用户登录

**POST** `/auth/login`

**请求体**：
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "张三"
    }
  }
}
```

### 2.2 刷新令牌

**POST** `/auth/refresh`

**请求体**：
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### 2.3 用户登出

**POST** `/auth/logout`

**请求头**：需要 `Authorization: Bearer <token>`

### 2.4 OAuth 登录

**GET** `/auth/oauth/{provider}`

- 支持的 provider: `google`, `github`, `gitlab`
- 返回重定向 URL

---

## 3. 项目接口

### 3.1 获取项目列表

**GET** `/projects`

**查询参数**：
| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `team_id` | UUID | 是 | 团队 ID |
| `status` | string | 否 | 状态筛选：`active`/`archived`/`paused` |
| `page` | int | 否 | 页码，默认 1 |
| `page_size` | int | 否 | 每页数量，默认 20 |

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "DevSmart Core",
      "description": "核心服务开发",
      "status": "active",
      "tech_stack": {
        "languages": ["TypeScript", "Python"],
        "frameworks": ["Next.js", "FastAPI"]
      },
      "repository_url": "https://github.com/org/repo",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": { ... }
}
```

### 3.2 创建项目

**POST** `/projects`

**权限**：Admin+

**请求体**：
```json
{
  "team_id": "uuid",
  "name": "新项目",
  "description": "项目描述",
  "tech_stack": {
    "languages": ["TypeScript"],
    "frameworks": ["React"]
  },
  "repository_url": "https://github.com/org/repo"
}
```

### 3.3 获取项目详情

**GET** `/projects/{id}`

### 3.4 更新项目

**PUT** `/projects/{id}`

**权限**：Admin+

### 3.5 删除项目

**DELETE** `/projects/{id}`

**权限**：Owner

---

## 4. PRD 接口

### 4.1 获取 PRD 列表

**GET** `/projects/{projectId}/prds`

**查询参数**：
| 参数 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `status` | string | 否 | 状态：`draft`/`reviewing`/`approved`/`archived` |
| `created_by` | UUID | 否 | 创建者筛选 |
| `page` | int | 否 | 页码 |

### 4.2 创建 PRD

**POST** `/projects/{projectId}/prds`

**权限**：Member+

**请求体**：
```json
{
  "title": "用户认证功能 PRD",
  "content": {
    "background": "业务背景描述...",
    "objectives": ["目标1", "目标2"],
    "user_stories": [
      {
        "role": "普通用户",
        "action": "通过邮箱注册账号",
        "benefit": "以便使用平台功能"
      }
    ],
    "acceptance_criteria": [
      {
        "id": "AC001",
        "description": "用户可以使用邮箱和密码注册",
        "priority": "high"
      }
    ],
    "non_functional": {
      "performance": "注册接口响应时间 < 500ms",
      "security": "密码需加密存储"
    },
    "out_of_scope": ["社交登录"]
  }
}
```

### 4.3 AI 生成 PRD

**POST** `/projects/{projectId}/prds/generate`

**权限**：Member+

**请求体**：
```json
{
  "requirement": "我们需要一个用户认证功能，支持邮箱注册登录，并有密码找回功能",
  "context": {
    "tech_stack": ["TypeScript", "Next.js"],
    "constraints": ["需要符合 GDPR 规范"],
    "references": ["参考竞品 A 的注册流程"]
  }
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "用户认证功能 PRD",
    "status": "draft",
    "content": { ... },
    "generated_by": "ai",
    "generation_meta": {
      "model": "gpt-4o",
      "tokens_used": 2500,
      "duration_ms": 8000
    }
  }
}
```

### 4.4 获取 PRD 详情

**GET** `/prds/{id}`

### 4.5 更新 PRD

**PUT** `/prds/{id}`

**权限**：仅 Draft 状态可编辑；Member 只能编辑自己创建的

### 4.6 提交 PRD 评审

**POST** `/prds/{id}/submit-review`

**权限**：创建者 / Admin+

**响应**：
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "reviewing",
    "submitted_at": "2024-01-15T10:30:00Z"
  }
}
```

### 4.7 批准 PRD

**POST** `/prds/{id}/approve`

**权限**：Admin+

### 4.8 打回 PRD

**POST** `/prds/{id}/reject`

**权限**：Admin+

**请求体**：
```json
{
  "reason": "验收标准不够明确，请补充边缘场景"
}
```

### 4.9 一致性校验

**POST** `/prds/{id}/validate`

**说明**：触发 AI 对 PRD 进行逻辑一致性检查

**响应**：
```json
{
  "success": true,
  "data": {
    "is_valid": false,
    "issues": [
      {
        "severity": "warning",
        "type": "logic_conflict",
        "description": "AC001 和 AC003 存在逻辑冲突",
        "location": "acceptance_criteria",
        "suggestion": "建议明确两个条件的优先级"
      },
      {
        "severity": "info",
        "type": "missing_edge_case",
        "description": "未覆盖密码输入错误超过限制的场景"
      }
    ]
  }
}
```

---

## 5. 任务接口

### 5.1 获取任务列表

**GET** `/prds/{prdId}/tasks`

**查询参数**：
| 参数 | 类型 | 说明 |
|:---|:---|:---|
| `status` | string | `pending`/`ai_processing`/`human_review`/`done`/`cancelled` |
| `assigned_agent` | string | Agent 类型筛选 |

### 5.2 从 PRD 分解任务

**POST** `/prds/{prdId}/tasks/generate`

**权限**：Admin+

**说明**：Supervisor Agent 自动将 PRD 分解为开发任务

**请求体**：
```json
{
  "options": {
    "granularity": "medium",
    "include_tests": true
  }
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "uuid",
        "title": "实现用户注册 API",
        "description": "创建 POST /auth/register 接口...",
        "status": "pending",
        "priority": 1,
        "estimated_points": 3,
        "suggested_agent": "coder"
      },
      {
        "id": "uuid",
        "title": "编写注册功能单元测试",
        "status": "pending",
        "priority": 2,
        "suggested_agent": "qa"
      }
    ],
    "total_generated": 5
  }
}
```

### 5.3 获取任务详情

**GET** `/tasks/{id}`

**响应**：
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "prd_id": "uuid",
    "title": "实现用户注册 API",
    "description": "...",
    "status": "ai_processing",
    "assigned_agent": "coder",
    "assigned_to": null,
    "priority": 1,
    "context": {
      "related_files": ["src/api/auth.ts", "src/models/user.ts"],
      "api_docs": ["POST /api/users - 创建用户"],
      "architecture_notes": "遵循 Repository 模式"
    },
    "external_ref": {
      "jira_id": "DEV-123",
      "jira_url": "https://jira.example.com/browse/DEV-123"
    },
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### 5.4 更新任务状态

**PUT** `/tasks/{id}/status`

**请求体**：
```json
{
  "status": "human_review",
  "reason": "AI 处理完成，等待确认"
}
```

### 5.5 确认任务

**POST** `/tasks/{id}/confirm`

**权限**：Member+（仅能确认分配给自己的任务）

**请求体**：
```json
{
  "action": "approve",
  "feedback": "代码质量良好，符合预期"
}
```

或：
```json
{
  "action": "redo",
  "feedback": "需要增加输入验证逻辑"
}
```

### 5.6 同步到外部系统

**POST** `/tasks/{id}/sync`

**权限**：Admin+

**请求体**：
```json
{
  "target": "jira",
  "options": {
    "project_key": "DEV",
    "issue_type": "Task"
  }
}
```

---

## 6. Agent 接口

### 6.1 获取 Agent 列表

**GET** `/agents`

**查询参数**：
| 参数 | 类型 | 说明 |
|:---|:---|:---|
| `team_id` | UUID | 团队 ID |
| `type` | string | Agent 类型：`pm`/`coder`/`qa`/`designer`/`supervisor`/`ops` |
| `status` | string | 状态：`idle`/`running`/`paused`/`error` |

### 6.2 创建 Agent

**POST** `/agents`

**权限**：Admin+

**请求体**：
```json
{
  "team_id": "uuid",
  "type": "coder",
  "name": "Coder-01",
  "model": "gpt-4o",
  "config": {
    "temperature": 0.3,
    "max_tokens": 4096,
    "tools_enabled": ["code_repository", "issue_tracker"],
    "auto_context_injection": true,
    "external_cli": "cursor-cli"
  }
}
```

### 6.3 获取 Agent 详情

**GET** `/agents/{id}`

### 6.4 更新 Agent 配置

**PUT** `/agents/{id}`

**权限**：Admin+

### 6.5 启动 Agent

**POST** `/agents/{id}/start`

**权限**：Admin+

### 6.6 停止 Agent

**POST** `/agents/{id}/stop`

**权限**：Admin+

### 6.7 暂停 Agent

**POST** `/agents/{id}/pause`

**权限**：Admin+

### 6.8 恢复 Agent

**POST** `/agents/{id}/resume`

**权限**：Admin+

### 6.9 获取 Agent 执行历史

**GET** `/agents/{id}/executions`

**查询参数**：
| 参数 | 类型 | 说明 |
|:---|:---|:---|
| `status` | string | `running`/`success`/`failed`/`cancelled` |
| `start_time` | datetime | 开始时间筛选 |
| `end_time` | datetime | 结束时间筛选 |

**响应**：
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "task_id": "uuid",
      "status": "success",
      "input": { "task_title": "实现注册 API" },
      "output": { "pr_url": "https://github.com/..." },
      "tokens_used": 3500,
      "duration_ms": 45000,
      "trace_id": "langsmith-trace-123",
      "started_at": "2024-01-15T10:30:00Z",
      "finished_at": "2024-01-15T10:30:45Z"
    }
  ],
  "pagination": { ... }
}
```

---

## 7. 知识库接口

### 7.1 语义搜索

**POST** `/knowledge/search`

**请求体**：
```json
{
  "query": "用户认证最佳实践",
  "top_k": 10,
  "filters": {
    "project_id": "uuid",
    "type": ["api_doc", "architecture"]
  },
  "threshold": 0.7
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "uuid",
        "title": "JWT 认证设计规范",
        "content_preview": "本文档定义了系统中 JWT 认证的实现规范...",
        "type": "architecture",
        "score": 0.92,
        "metadata": {
          "author": "张三",
          "updated_at": "2024-01-10T00:00:00Z"
        }
      }
    ],
    "total": 5
  }
}
```

### 7.2 上传文档

**POST** `/knowledge/documents`

**权限**：Member+

**请求体** (multipart/form-data)：
| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `file` | File | 文档文件 (PDF/Markdown/TXT) |
| `project_id` | UUID | 所属项目 |
| `title` | string | 文档标题 |
| `type` | string | 类型：`api_doc`/`architecture`/`guide`/`meeting_note` |

### 7.3 获取文档详情

**GET** `/knowledge/documents/{id}`

### 7.4 更新文档

**PUT** `/knowledge/documents/{id}`

### 7.5 删除文档

**DELETE** `/knowledge/documents/{id}`

**权限**：Admin+

---

## 8. 团队管理接口

### 8.1 获取团队成员

**GET** `/teams/{teamId}/members`

### 8.2 邀请成员

**POST** `/teams/{teamId}/members/invite`

**权限**：Admin+

**请求体**：
```json
{
  "email": "newuser@example.com",
  "role": "member"
}
```

### 8.3 移除成员

**DELETE** `/teams/{teamId}/members/{userId}`

**权限**：Owner 或 Admin（Admin 不能移除 Owner 和其他 Admin）

### 8.4 修改成员角色

**PUT** `/teams/{teamId}/members/{userId}/role`

**权限**：Owner

**请求体**：
```json
{
  "role": "admin"
}
```

---

## 9. WebSocket 接口

### 9.1 实时任务状态更新

**WebSocket** `/ws/tasks`

**连接参数**：
```
wss://api.devsmart.io/v1/ws/tasks?token=<jwt_token>&team_id=<uuid>
```

**消息格式**：
```json
{
  "event": "task.status_changed",
  "data": {
    "task_id": "uuid",
    "from_status": "ai_processing",
    "to_status": "human_review",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**支持的事件**：
| 事件 | 说明 |
|:---|:---|
| `task.created` | 新任务创建 |
| `task.status_changed` | 任务状态变更 |
| `task.assigned` | 任务分配 |
| `task.completed` | 任务完成 |

### 9.2 Agent 执行日志流

**WebSocket** `/ws/agents/{agentId}/logs`

**消息格式**：
```json
{
  "event": "agent.log",
  "data": {
    "execution_id": "uuid",
    "level": "info",
    "message": "开始分析代码结构...",
    "timestamp": "2024-01-15T10:30:00Z",
    "metadata": {
      "step": "context_analysis",
      "progress": 30
    }
  }
}
```

### 9.3 PRD 协作编辑

**WebSocket** `/ws/prds/{prdId}/collaborate`

**说明**：支持多人实时协作编辑 PRD（基于 OT 或 CRDT）

---

## 10. 错误码定义

### 10.1 HTTP 状态码

| 状态码 | 说明 |
|:---|:---|
| `200` | 成功 |
| `201` | 创建成功 |
| `400` | 请求参数错误 |
| `401` | 未认证 |
| `403` | 无权限 |
| `404` | 资源不存在 |
| `409` | 资源冲突（如状态不允许操作） |
| `422` | 业务逻辑错误 |
| `429` | 请求过于频繁 |
| `500` | 服务器内部错误 |

### 10.2 业务错误码

| 错误码 | 说明 |
|:---|:---|
| `VALIDATION_ERROR` | 请求参数验证失败 |
| `AUTHENTICATION_FAILED` | 认证失败 |
| `PERMISSION_DENIED` | 权限不足 |
| `RESOURCE_NOT_FOUND` | 资源不存在 |
| `INVALID_STATE_TRANSITION` | 无效的状态转换 |
| `DUPLICATE_RESOURCE` | 资源已存在 |
| `RATE_LIMIT_EXCEEDED` | 超出速率限制 |
| `EXTERNAL_SERVICE_ERROR` | 外部服务调用失败 |
| `AI_GENERATION_FAILED` | AI 生成失败 |
| `AGENT_BUSY` | Agent 忙碌中 |

---

## 11. 速率限制

### 11.1 限制规则

| 计划 | 限制 |
|:---|:---|
| **Free** | 100 请求/分钟，1000 请求/天 |
| **Pro** | 500 请求/分钟，无每日限制 |
| **Enterprise** | 自定义 |

### 11.2 响应头

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705312200
```

---

## 12. API 版本管理

- 当前版本：`v1`
- 版本通过 URL 路径指定（如 `/v1/projects`）
- 重大变更将发布新版本，旧版本保持兼容至少 6 个月
- 弃用警告通过响应头 `Deprecation` 和 `Sunset` 通知
