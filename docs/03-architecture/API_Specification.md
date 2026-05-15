# 输出结构规格

> 本文件不定义技术 API。它只定义 POC 阶段产品输出内容的结构，便于前后端和文档保持一致。

## 需求输入

```json
{
  "raw_requirement": "支持团队成员邮箱邀请",
  "template": "feature_prd",
  "extra_context": "面向 SaaS 后台管理员"
}
```

## 澄清问题

```json
{
  "questions": [
    {
      "priority": "must",
      "question": "谁可以邀请团队成员？",
      "reason": "缺少角色和权限边界"
    }
  ]
}
```

## PRD 输出

```json
{
  "title": "团队成员邮箱邀请",
  "background": "当前团队成员添加依赖人工沟通，效率低且易遗漏。",
  "goals": ["管理员可以通过邮箱邀请成员加入团队"],
  "user_stories": ["作为管理员，我希望通过邮箱邀请成员，以便快速扩充团队。"],
  "scope": ["邀请入口", "邮箱输入", "邀请状态", "过期处理"],
  "non_goals": ["不支持批量导入"],
  "open_questions": ["邀请有效期是否固定为 7 天？"]
}
```

## AC 输出

```json
{
  "items": [
    {
      "scenario": "成功发送邀请",
      "given": "当前用户拥有成员管理权限",
      "when": "输入有效邮箱并提交邀请",
      "then": "系统提示邀请发送成功，并生成待接受邀请记录"
    }
  ]
}
```

## 待确认项

```json
{
  "items": [
    {
      "type": "assumption",
      "priority": "must",
      "content": "邀请有效期暂定 7 天，需要业务确认。"
    }
  ]
}
```

## 约束

- 输出不包含模型内部推理过程。
- 假设必须显式标记。
- AC 必须可测试、可判断。
- 技术实现字段不进入产品输出结构。
