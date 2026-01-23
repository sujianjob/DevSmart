# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

DevSmart 是一个 **AI 原生智能研发平台**，通过 LLM 和 Agent 技术实现从需求分析、PRD 生成、任务分发到代码开发的全自动化协作流程。

**当前状态**：POC（概念验证）阶段，主要产出为架构文档、原型设计和产品规范，暂无实现代码。

## 技术栈

| 层级 | 技术 |
|:---|:---|
| 前端 | React 19.x + TypeScript 5.x + Vite 7.x + TailwindCSS 4.x + Zustand 5.x |
| 后端 | Python 3.11+ + FastAPI 0.128+ + Pydantic 2.x |
| Agent | LangGraph 1.0+（编排）+ LangChain 1.2+（LLM 集成）+ LangSmith（追踪）|
| 数据库 | PostgreSQL 16+ + Redis 7+ + Chroma/Milvus（向量库）+ Neo4j 5.x（图数据库）|
| 基础设施 | Docker 24+ + Kubernetes 1.29+ + Traefik 3.x |

## 开发命令

### Backend (Python)
```bash
uv venv                              # 创建虚拟环境
uv sync                              # 同步依赖
uv run fastapi dev app/main.py       # 运行开发服务器
uv run pytest                        # 执行测试
```

### Frontend (React)
```bash
pnpm install                         # 安装依赖
pnpm dev                             # 运行开发服务器
pnpm build                           # 生产构建
pnpm test                            # 运行测试
pnpm lint                            # 代码检查
```

## 核心架构

### 五层逻辑架构
1. **交互层**：IDE 插件、聊天界面、仪表盘
2. **编排层**：LangGraph 状态机（系统大脑）
3. **能力抽象层**：标准接口定义（ICodeRepository、IIssueTracker）
4. **工具实现层**：具体适配器（GitHub、GitLab、Jira、Linear）
5. **知识基础设施**：向量库、代码图谱、追踪存储

### Agent 拓扑
- **Supervisor Agent**：总控节点，语义路由、任务拆解、全局监控
- **PM Agent**：需求分析、PRD 生成（执行器）
- **Coder Agent**：任务协调、上下文注入、状态同步（**协调器，不直接写代码**）
- **QA Agent**：测试用例生成、Bug 分析（执行器）
- **Designer Agent**：原型生成、设计规范检查（执行器）

## 关键约束

### 语言与交流
- 所有沟通、代码注释、文档全部使用**中文**
- 新文件使用 UTF-8（无 BOM）

### 工作流规范
- **编码前必须与用户确认**：从文档/计划切换到编写代码前必须明确确认
- **编码前必须 Sequential-Thinking 分析**，保持最小变更边界
- **禁用 CI/CD 自动化**：构建、测试、发布必须人工操作
- 默认采取破坏性改动，主动清理过时代码；无迁移需求时说明"**无迁移，直接替换**"

### 质量要求
- 构建、编译、静态检查必须**零报错**
- 测试覆盖率 ≥ 90%
- 使用主流、活跃维护的库，锁定最新稳定版本
- 禁止泄露密钥或内部链接
- 所有新增或修改的代码必须补齐**中文文档和注释**

### 工具优先级
1. **Serena MCP**（首选）：代码检索、项目文档、shell 命令
2. **Sequential Thinking MCP**：编码/设计/架构变更前的分步思考
3. **Context7 MCP**：查官方文档或项目配置库
4. **外部网络**：仅用于读取公开资料，优先官方与权威来源

## 文档结构

```
docs/
├── 01-vision/          # 产品愿景（AI_Native_Concept_Paper, Product_Vision）
├── 02-product/         # 产品规范（功能规格、用户画像、状态机、权限矩阵）
├── 03-architecture/    # 架构规范（技术栈、API、数据模型、部署、安全）
prototype/              # 原型演示（工作流文档、截图、设计稿）
```

## 浏览器自动化

使用 `agent-browser` 进行 Web 自动化：
```bash
agent-browser open <url>              # 导航到页面
agent-browser snapshot -i             # 获取可交互元素
agent-browser click @e1               # 点击元素
agent-browser fill @e2 "text"         # 填充文本
```
