# 实施计划 - AI 原生系统 POC

# 目标描述
构建一个 **概念验证 (POC)** 系统，以验证核心架构决策：**LangGraph 监督者模式 (Supervisor)**、**异步事件循环** 和 **B/S 架构的人机协作**。
构建目标是一个基于 **FastAPI + React** 的 Web 系统（任务指挥中心），能够接收用户需求，将其路由给 PM/Coder Agent，并提供可视化的状态流转与人工审批能力。

## 核心技术规格 (Technical Specifications)

### 1. 核心依赖版本 (Validated by Context7 & Search)
- **LangGraph**: `^1.0.3` (Context7 验证: 支持 v1.0+ 稳定版)
- **LangChain**: `^1.2.0` (最新稳定版)
- **FastAPI**: `^0.122.0` (Context7 验证: 0.122+ / Search: 0.128)
- **React**: `^19.0.0` (建议使用最新稳定版)
- **Vite**: `^7.0.0` (Context7 验证: v7.0.0)

### 2. LangGraph 状态机设计
我们使用 **StateGraph** 并启用 SQLite Checkpointer 来支持持久化和“时光倒流”。

**Schema 定义**:
```python
class AgentState(TypedDict):
    task_id:str
    messages: Annotated[List[BaseMessage], add_messages]
    current_stage: Literal['planning', 'coding', 'review', 'approval']
    review_comments: List[str]
    next_action: Optional[str]
```

**Human-in-the-loop (HITL) 机制**:
- 使用 `graph.compile(checkpointer=memory, interrupt_before=["human_approval"])`。
- Agent 运行到 `human_approval` 节点前会自动暂停。
- 用户通过 API 调用 `graph.update_state(thread_id, {"review_comments": "..."})` 后，再次调用 `invoke` 恢复执行。

### 3. API 接口定义 (REST + SSE)
- `POST /tasks`: 创建新任务 (返回 `thread_id`)。
- `GET /tasks/{thread_id}/stream`: **SSE** 端点，实时推送 Agent 的每一步思考 (Op names, Tool calls)。
- `POST /tasks/{thread_id}/approve`: 人工审批通过，恢复执行。
- `POST /tasks/{thread_id}/reject`: 拒绝并附带修改意见，让 Agent 重试。

### 4. 前端交互设计 (Mission Control)
- **状态可视化**: 使用 React Flow 或 Mermaid 实时渲染当前 Active Node。
- **流式响应**: 解析 SSE 事件流，实现打字机效果展示 Agent 的思考过程。
- **审批卡片**: 当收到 `interrupt` 事件时，弹窗显示 diff/plan，要求用户操作。

## 待完成任务 (Tasks)

### 步骤 1: 系统基础设施搭建 (System Infrastructure)
- 借鉴标准化思路，创建清晰的目录结构：
    - `/.ai-context/`: 存放 Agent 运行时的上下文状态。
    - `/prompts/`: 借鉴 Vibe Coding 理念，将 Prompt 与代码分离管理的目录。
- 初始化 Backend (`backend/`): FastAPI + LangGraph.
- 初始化 Frontend (`frontend/`): React + Vite + TailwindCSS.

### 步骤 2: 核心大脑 API 化 (Supervisor Service)
- 实现 `backend/app/agents/supervisor.py` (LangGraph 逻辑)。
- 暴露 REST API:
    - `POST /tasks`: 提交新需求。
    - `GET /tasks/{id}/events`: SSE (Server-Sent Events) 推送 Agent 的思考过程与状态变更。

### 步骤 3: "连接器" Agent (PM & Coder)
- **PM Agent**: 读取 `/docs/` 模拟 RAG，生成计划。
- **Coder Agent**:
    - 生成 `task_context.json`。
    - 进入 "Pending" 状态，等待前端用户点击 "确认执行" (Human-in-the-loop)。

### 步骤 4: Web 控制台 (Mission Control)
- 开发一个简易的 "任务指挥中心"：
    - 左侧：对话框 (提交需求)。
    - 右侧：实时拓扑图 (Mermaid/ReactFlow)，显示 Supervisor -> PM -> Coder 的流转状态。
    - 底部：人工审批按钮 ("Approve Execution")。

## 验证计划 (Comprehensive Verification Strategy)

### 1. 单元测试 (Unit Testing)
- **Agent Logic**: 使用 `pytest` 单独测试 PM 和 Coder 的 Node 函数。
    - *Input*: 模拟的 `AgentState` 字典。
    - *Assert*: 检查返回的 `task_context` 结构和 `next_step` 路由决策。
- **Schema Validation**: 验证所有 Pydantic 模型能否正确解析非法数据。

### 2. 集成测试 (Integration Testing)
- **Supervisor Graph**:
    - 验证 "User -> PM -> Coder -> Interrupt" 的标准流转路径。
    - 验证 **Checkpointer** 持久化：模拟服务重启后，能否通过 `thread_id` 恢复状态。
- **API Endpoints**:
    - `POST /tasks`: 验证任务创建能否立刻返回 `thread_id`。
    - `GET /tasks/stream`: 验证 SSE 连接能否维持并推送 JSON 数据。

### 3. 端到端测试 (E2E Manual Walkthrough)
- **场景：人工驳回重做**
    1. 前端提交需求 "Login Page"。
    2. 等待 PM Agent 生成计划 -> 自动流转到 Coder Agent。
    3. Coder 生成 Mock 代码 -> 系统进入 `Wait for Approval` 状态。
    4. **人工干预**：点击 "Reject" 并输入 "使用 TypeScript"。
    5. **期望结果**：Graph 恢复执行，路由回 Coder Agent，Coder 重新生成包含 TypeScript 的指令。

### 4. 专项验证：HITL (Human-in-the-loop)
- 验证 `interrupt_before=["human_approval"]` 是否真的挂起了线程。
- 验证能否在“挂起”状态下读取当前的 `State (Memory)`。
- 验证 `update_state` 能否修改内存中的 `feedback` 字段。
