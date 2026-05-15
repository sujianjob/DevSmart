# 数据模型设计

## POC 核心实体

```text
Workspace
  -> RequirementPackage
  -> Clarification
  -> PRD
  -> AcceptanceCriteria
  -> GapItem
  -> ReviewRecord
  -> WorkflowEvent
```

## 实体说明

| 实体 | 说明 |
|:---|:---|
| Workspace | 空间或项目容器 |
| RequirementPackage | 一次从模糊需求到评审输出的需求包 |
| Clarification | 澄清问题和用户回答 |
| PRD | 结构化产品需求文档 |
| AcceptanceCriteria | 验收标准清单 |
| GapItem | 信息缺口、假设、风险和待确认项 |
| ReviewRecord | 评审动作、意见和结论 |
| WorkflowEvent | 状态变化和关键事件 |

## RequirementPackage 示例

```json
{
  "requirement_id": "req_001",
  "raw_requirement": "支持团队成员邮箱邀请",
  "clarity_status": "needs_clarification",
  "prd_id": "prd_001",
  "ac_ids": ["ac_001", "ac_002"],
  "gap_item_ids": ["gap_001"],
  "review_status": "pending"
}
```

## AC 示例

```json
{
  "ac_id": "ac_001",
  "requirement_id": "req_001",
  "scenario": "成功发送邀请",
  "given": "当前用户拥有成员管理权限",
  "when": "输入有效邮箱并提交邀请",
  "then": "系统创建邀请记录并提示发送成功"
}
```

## 审计原则

记录：

- 输入摘要
- 输出摘要
- 用户回答
- 评审动作
- 状态变更
- 产物引用

不记录：

- 模型内部推理链
- 明文密钥
- 不必要的个人敏感信息
