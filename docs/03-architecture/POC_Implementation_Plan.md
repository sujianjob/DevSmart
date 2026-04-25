# 实施计划 - AI 研发流程指挥中心 POC

> 状态：重新评估后更新版
> 目标周期：30 天
> 迁移策略：无迁移，直接替换旧版 POC 规划

---

## 1. POC 目标

本 POC 的目标不是构建完整 DevSmart 商业化平台，而是验证最小核心闭环：

```text
需求输入 -> PRD 生成/澄清 -> 人工审批 -> 任务拆解 -> 上下文包生成 -> 流程状态展示 -> 审计事件记录
```

核心问题：

1. AI 生成的 PRD 是否足够让 PM 基于它修改，而不是重写。
2. AI 拆解的任务是否足够让 Tech Lead 评审和分配。
3. 任务上下文包是否足够让研发或外部 Coding Agent 开始执行。
4. 流程事件是否足够支撑团队复盘和管理。

---

## 2. 核心技术规格

### 2.1 版本原则

POC 阶段不在文档中锁死快速变化的模型和框架小版本。实施时按以下原则执行：

- 使用实施当天最新稳定版，并记录验证日期。
- 关键依赖需要锁定到明确版本写入依赖文件。
- 模型使用能力路由，不把固定模型名称硬编码到业务逻辑。

### 2.2 推荐技术栈

| 层级 | 技术 | POC 用途 |
|:---|:---|:---|
| 前端 | React + TypeScript + Vite | 任务指挥中心 |
| 后端 | FastAPI + Pydantic | REST API、SSE、Schema 校验 |
| 编排 | LangGraph | 状态机、HITL、持久化恢复 |
| 存储 | SQLite / PostgreSQL | POC 状态、任务、事件记录 |
| LLM | 模型路由 | PRD 生成、澄清问题、任务拆解 |
| 事件流 | SSE | 前端展示流程状态变化 |

### 2.3 暂不引入

30 天 POC 不引入以下生产级组件：

- Kubernetes。
- ArgoCD / 自动部署流水线。
- Milvus。
- Neo4j。
- 完整多租户权限体系。
- CI/CD 自动触发。

---

## 3. LangGraph 状态机设计

### 3.1 状态定义

```python
class AgentState(TypedDict):
    task_id: str
    requirement: str
    prd: dict | None
    clarification_questions: list[str]
    approval_status: Literal["pending", "approved", "rejected"]
    review_comments: list[str]
    tasks: list[dict]
    context_packages: list[dict]
    current_stage: Literal[
        "created",
        "prd_generating",
        "clarifying",
        "pending_approval",
        "task_splitting",
        "context_packaging",
        "completed",
        "failed"
    ]
```

### 3.2 核心节点

| 节点 | 职责 |
|:---|:---|
| `receive_requirement` | 接收用户需求并初始化状态 |
| `pm_generate_prd` | 生成 PRD 初稿 |
| `pm_clarify` | 生成澄清问题 |
| `human_approval` | 等待人工审批或驳回 |
| `split_tasks` | 将 PRD 拆解为研发任务 |
| `package_context` | 为每个任务生成上下文包 |
| `record_events` | 记录流程事件 |

### 3.3 HITL 机制

- PRD 生成后进入 `human_approval`。
- 用户可以批准、驳回或补充意见。
- 驳回后回到 `pm_generate_prd`，并带入 `review_comments`。
- 批准后进入 `split_tasks`。

---

## 4. API 接口定义

| 方法 | 路径 | 说明 |
|:---|:---|:---|
| `POST` | `/tasks` | 创建需求任务 |
| `GET` | `/tasks/{task_id}` | 查询任务详情 |
| `GET` | `/tasks/{task_id}/events` | 获取任务事件流 |
| `POST` | `/tasks/{task_id}/approve` | 批准当前 PRD |
| `POST` | `/tasks/{task_id}/reject` | 驳回当前 PRD 并提交意见 |
| `GET` | `/tasks/{task_id}/context-packages` | 获取任务上下文包 |

---

## 5. 前端交互设计

POC 只做 4 个页面：

1. **任务创建页**：输入自然语言需求。
2. **PRD 审批页**：查看 PRD，批准或驳回。
3. **任务拆解页**：查看任务列表和上下文包。
4. **流程回放页**：查看执行轨迹、工具调用、输入输出摘要、审批记录和状态变更。

注意：流程回放只展示可审计事件，不展示模型内部 Chain of Thought。

---

## 6. 待完成任务

### 步骤 1：工程基础设施

- 初始化 `backend/`。
- 初始化 `frontend/`。
- 创建 `prompts/`。
- 创建 `.ai-context/`。
- 定义任务、PRD、事件、上下文包 Schema。

### 步骤 2：Supervisor 与 PM Agent

- 实现 LangGraph 状态机。
- 实现 PM Agent PRD 生成。
- 实现澄清问题生成。
- 实现人工审批中断与恢复。

### 步骤 3：任务拆解与上下文包

- 实现任务拆解。
- 实现 `task_context.json`。
- 从 PRD 和 `/docs` 中提取技术约束。
- 明确标记 AI 推测的相关文件。

### 步骤 4：Web 指挥中心

- 实现需求输入。
- 实现 PRD 预览与审批。
- 实现任务看板。
- 实现事件时间线。

---

## 7. 验证计划

### 7.1 单元测试

- PM Agent：输入需求后输出结构化 PRD。
- Task Splitter：输入 PRD 后输出任务列表。
- Context Packager：输入任务后输出上下文包。
- Schema：非法数据必须被拒绝。

### 7.2 集成测试

- 标准路径：需求 -> PRD -> 审批 -> 任务拆解 -> 上下文包。
- 驳回路径：需求 -> PRD -> 驳回 -> 重新生成 -> 审批。
- 事件流：每一步状态变更都能被前端读取。

### 7.3 手工演示场景

准备至少 5 个典型需求：

1. 团队成员邀请。
2. 任务看板筛选。
3. 登录页重构。
4. 退款流程优化。
5. 通知中心新增告警规则。

---

## 8. 30 天成功指标

| 指标 | 目标 |
|:---|:---|
| PRD 生成成功率 | ≥ 80% |
| PRD 初稿可采纳率 | ≥ 50% |
| 任务拆解可采纳率 | ≥ 60% |
| 从需求到任务包耗时 | ≤ 10 分钟 |
| 内测用户愿意继续使用比例 | ≥ 60% |
