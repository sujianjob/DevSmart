# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## 项目概述

DevSmart 是一个 **AI 需求澄清与 PRD/AC 生成工作流工具**，用于把一句模糊需求转化为结构完整、边界清晰、可评审、可验收的需求包。

当前状态：POC 规划与早期实现阶段，产品范围以 [PRD](PRD.md) 为准。

## 当前产品边界

### 做

- 需求输入和模糊度判断。
- 信息缺口识别。
- 澄清问题生成。
- PRD 生成与编辑。
- AC 验收标准生成。
- 边界、异常、非目标和待确认项补漏。
- 评审记录和需求包导出。

### 不做

- 代码生成。
- 技术方案设计。
- API 或数据库设计。
- 研发任务拆解。
- 工程工具调度。
- 自动 CI/CD。

## 本地开发命令

### Backend

```bash
bash scripts/dev-backend.sh
```

### Frontend

```bash
bash scripts/dev-frontend.sh
```

### 测试

```bash
cd backend
python -m pytest tests
```

## 关键约束

### 语言与交流

- 所有沟通、代码注释、文档全部使用**中文**。
- 新文件使用 UTF-8（无 BOM）。

### 工作流规范

- 编码前必须 Sequential-Thinking 分析，保持最小变更边界。
- 禁用 CI/CD 自动化：构建、测试、发布必须人工操作。
- 默认采取破坏性改动，主动清理过时代码；无迁移需求时说明“无迁移，直接替换”。

### 质量要求

- 构建、编译、静态检查必须零报错。
- 测试覆盖率目标 ≥ 90%。
- 禁止泄露密钥或内部链接。
- 所有新增或修改的代码必须补齐中文文档和注释。

### 工具优先级

1. Serena MCP：代码检索、项目文档、shell 命令。
2. Sequential Thinking MCP：编码、设计或架构变更前的分步思考。
3. Context7 MCP：查官方文档或项目配置库。
4. 外部网络：仅用于读取公开资料，优先官方与权威来源。

## 文档结构

```text
docs/
├── 01-vision/          # 产品愿景和 AI 原生需求工作流
├── 02-product/         # 产品规范、用户画像、状态机、指标
├── 03-architecture/    # 实现边界、数据模型、输出结构、运行约束
prototype/              # 历史原型素材和新 POC 流程说明
```

## 浏览器自动化

使用 `agent-browser` 进行 Web 自动化：

```bash
agent-browser open <url>
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "text"
```
