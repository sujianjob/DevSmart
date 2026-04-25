# 数据模型设计

## POC 核心实体

```text
Project
  -> WorkflowRun
  -> PRD
  -> Task
  -> ContextPackage
  -> WorkflowEvent
  -> Approval
```

## 实体说明

| 实体 | 说明 |
|:---|:---|
| Project | 项目容器 |
| WorkflowRun | 一次从需求到任务包的流程 |
| PRD | 结构化需求文档 |
| Task | 从 PRD 拆出的研发任务 |
| ContextPackage | 任务上下文包 |
| WorkflowEvent | 流程事件和审计记录 |
| Approval | 人工审批记录 |

## ContextPackage 示例

```json
{
  "task_id": "task_001",
  "prd_summary": "团队成员邀请功能",
  "acceptance_criteria": [],
  "technical_constraints": [],
  "suggested_files": [],
  "api_contracts": [],
  "test_scenarios": [],
  "open_questions": []
}
```

## 审计原则

记录：

- 输入摘要
- 输出摘要
- 工具调用
- 审批动作
- 状态变更
- 产物引用

不记录：

- 模型内部推理链
- 明文密钥
- 无必要的源码全文
