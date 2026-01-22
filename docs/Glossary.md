# DevSmart 术语表 (Glossary)

本文档定义了 DevSmart 平台中使用的核心术语，确保团队沟通的一致性。

---

## 1. Agent 相关术语

| 术语 | 英文全称 | 定义 | 角色定位 |
|:---|:---|:---|:---|
| **PM Agent** | Product Manager Agent | 产品经理智能体，负责需求分析和文档生成 | **执行器** - 生成 PRD、需求澄清、竞品分析 |
| **Coder Agent** | Coder Coordinator Agent | 开发协调智能体，负责任务编排和状态同步 | **协调器** - 任务分发、上下文注入、状态同步；**不直接写代码** |
| **QA Agent** | Quality Assurance Agent | 质量保障智能体，负责测试策略和质量把控 | **执行器** - 测试用例生成、回归范围筛选、测试报告分析 |
| **Designer Agent** | UI/UX Designer Agent | 设计智能体，负责原型和设计规范 | **执行器** - 原型生成、设计规范检查、UI 一致性校验 |
| **Supervisor Agent** | Supervisor Agent | 总控智能体，系统的"大脑" | **协调器** - 语义路由、任务拆解、全局监控、跨 Agent 协同 |
| **Ops Agent** | Operations Agent | 运维智能体，负责运维分析和建议 | **执行器** - 告警分析、根因推断、变更关联（仅建议，不自动执行） |

### Agent 角色定位说明

- **执行器 (Executor)**：直接产出具体交付物（文档、测试用例、设计稿等）的 Agent
- **协调器 (Coordinator)**：负责任务编排、状态管理、跨系统同步的 Agent，不直接产出代码或文档

---

## 2. 核心概念术语

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| **HITL** | Human-in-the-Loop | 人机协作模式，关键节点需人工确认后才能流转到下一步 |
| **PRD** | Product Requirements Document | 产品需求文档，包含背景、用户故事、验收标准等结构化内容 |
| **上下文注入** | Context Injection | Coder Agent 自动为任务添加相关信息（代码片段、历史讨论、规范约束、接口定义） |
| **Time Travel** | Time Travel | 历史工作流回放功能，可回溯 Agent 决策过程和操作链路 |
| **RAG** | Retrieval Augmented Generation | 检索增强生成，通过向量检索为 AI 提供相关上下文 |
| **MCP** | Model Context Protocol | 模型上下文协议，用于 Agent 与外部工具的标准化通信 |
| **Golden Dataset** | Golden Dataset | 黄金测试集，用于验证 Prompt 变更后 AI 能力是否退化 |
| **Code CLI** | Code CLI | 外部编码工具的命令行接口（如 Cursor CLI、Copilot CLI），由 Coder Agent 调度 |

---

## 3. 状态术语

### 3.1 PRD 状态

| 状态 | 英文 | 适用对象 | 定义 |
|:---|:---|:---|:---|
| **草稿** | Draft | PRD | AI 生成或人工创建后的初始状态，可自由编辑 |
| **评审中** | Reviewing | PRD | 已提交评审，等待评审人确认 |
| **已批准** | Approved | PRD | 评审通过，可分解为开发任务 |
| **已归档** | Archived | PRD | 完成生命周期，归档保存 |

### 3.2 Task 状态

| 状态 | 英文 | 适用对象 | 定义 |
|:---|:---|:---|:---|
| **待处理** | Pending | Task | 任务已创建，等待 Agent 或人工认领 |
| **AI 处理中** | AI Processing | Task | Agent 正在处理该任务 |
| **待人工确认** | Human Review | Task | Agent 处理完成，等待人工确认结果 |
| **已完成** | Done | Task | 任务完成，验收通过 |

### 3.3 Agent 状态

| 状态 | 英文 | 适用对象 | 定义 |
|:---|:---|:---|:---|
| **空闲** | Idle | Agent | Agent 已就绪，等待任务 |
| **运行中** | Running | Agent | Agent 正在执行任务 |
| **已暂停** | Paused | Agent | Agent 被手动暂停 |
| **异常** | Error | Agent | Agent 遇到错误，需人工介入 |

---

## 4. 架构术语

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| **交互层** | Interaction Layer | 用户触达系统的界面层，包括 IDE 插件、聊天界面、仪表盘 |
| **编排层** | Orchestration Layer | 基于 LangGraph 的核心状态机，负责任务调度和 Agent 协同 |
| **能力抽象层** | Capability Interface Layer | 定义标准接口（如 ICodeRepository、IIssueTracker），解耦具体工具 |
| **工具实现层** | Tool/Plugin Layer | 能力的具体实现，通过 Adapter 模式接入各种外部工具 |
| **知识基础设施** | Knowledge Infrastructure | 系统的长期记忆，包括向量库、代码图谱、追踪存储 |

---

## 5. 权限术语

| 术语 | 英文 | 定义 |
|:---|:---|:---|
| **Owner** | 所有者 | 组织创建者，拥有全部权限 |
| **Admin** | 管理员 | 团队管理员，可管理成员和配置 |
| **Member** | 成员 | 普通成员，可使用核心功能 |
| **Guest** | 访客 | 受邀访客，只读权限 |

---

## 6. 集成术语

| 术语 | 定义 |
|:---|:---|
| **SCM Adapter** | 代码仓库适配器（GitHub、GitLab、Bitbucket） |
| **PM Adapter** | 项目管理工具适配器（Jira、Linear、Trello） |
| **CI/CD Adapter** | 持续集成/部署适配器（Jenkins、GitHub Actions） |
| **Vector DB** | 向量数据库，存储语义 Embedding（Chroma、Milvus） |
| **Code Graph** | 代码关系图谱，基于 AST 分析（Neo4j） |

---

## 7. 缩写对照表

| 缩写 | 全称 | 中文 |
|:---|:---|:---|
| PRD | Product Requirements Document | 产品需求文档 |
| HITL | Human-in-the-Loop | 人机协作 |
| RAG | Retrieval Augmented Generation | 检索增强生成 |
| MCP | Model Context Protocol | 模型上下文协议 |
| AST | Abstract Syntax Tree | 抽象语法树 |
| ADR | Architecture Decision Record | 架构决策记录 |
| SDLC | Software Development Life Cycle | 软件开发生命周期 |
| CI/CD | Continuous Integration/Continuous Deployment | 持续集成/持续部署 |
