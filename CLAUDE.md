# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

DevSmart 是 AI 原生研发平台设计项目，当前处于 POC 阶段。本仓库主要包含 Claude Code 技能模块和设计文档。

## 可用技能

### agent-browser - 浏览器自动化
```bash
agent-browser open <url>        # 打开页面
agent-browser snapshot -i       # 获取交互元素（带 @ref 引用）
agent-browser click @e1         # 点击元素
agent-browser fill @e2 "text"   # 填充输入框
agent-browser screenshot        # 截图
agent-browser close             # 关闭浏览器
```

核心工作流：`open` → `snapshot -i` → 使用 @ref 交互 → 每次导航后重新 `snapshot`

### web-scraper - 智能网站爬取
基于 agent-browser 的文档网站爬取工具。详见 `.claude/skills/web-scraper/SKILL.md`

**关键概念**：
- **SPA 检测**：点击后页面无白屏刷新 → 必须用 `click` 导航而非 `open`
- **5 阶段工作流**：初始化 → 导航分析 → 深度遍历 → 内容结构化 → 完整性校验
- **预设配置**：`.claude/skills/web-scraper/presets/` 下的 YAML 文件
- **断点续爬**：自动生成 `.scraper-state.json` 状态文件

### admin-reverse-docs - 后台管理系统反向文档
基于 agent-browser 的后台管理系统分析工具。详见 `.claude/skills/admin-reverse-docs/SKILL.md`

**关键概念**：
- **登录状态管理**：`agent-browser state save/load` 保存和加载认证状态
- **6 阶段工作流**：系统识别 → 导航分析 → 模块遍历 → 元素提取 → API 发现 → 文档生成
- **双重输出**：原样记录（保持后台结构）+ 智能分析（数据模型、API、业务流程）
- **断点续爬**：自动生成 `.reverse-state.json` 状态文件

### admin-tester - 后台管理系统 UI 测试
基于 admin-reverse-docs 输出的 UI 功能测试工具。详见 `.claude/skills/admin-tester/SKILL.md`

**关键概念**：
- **输入依赖**：需要 admin-reverse-docs 输出的文档目录
- **5 阶段工作流**：加载解析 → 用例生成 → 人工审核 → 执行测试 → 报告生成
- **测试类型**：列表页测试、表单测试、导航测试、操作测试
- **人工审核**：生成用例后用户可编辑 `_index.yaml` 启用/禁用用例
- **断点续测**：自动生成 `.test-state.json` 状态文件

## 技能模块结构

```
.claude/skills/{skill-name}/
├── SKILL.md          # 主文档（必需）
├── ADVANCED.md       # 高级功能（可选）
├── TEMPLATES.md      # 输出模板（可选）
└── presets/          # 预设配置目录（可选）
```

## 开发规范

- 使用中文进行所有文档和代码注释
- 遵循最小变更原则
- 技能模块的 SKILL.md 需包含 YAML frontmatter（name, description）
