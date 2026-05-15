# 状态机定义

## 需求包主状态

```text
created
  -> analyzing
  -> clarifying
  -> prd_generating
  -> ac_generating
  -> gap_checking
  -> pending_review
  -> approved
```

异常状态：

```text
pending_review -> rejected
任意状态 -> failed
```

## 评审状态

| 状态 | 说明 |
|:---|:---|
| pending | 等待人工评审 |
| approved | 评审通过 |
| rejected | 驳回，带反馈重新生成 |
| needs_changes | 需要补充信息或局部修改 |

## 事件记录

每次状态变化必须记录：

- `event_id`
- `requirement_id`
- `event_type`
- `actor`
- `input_summary`
- `output_summary`
- `created_at`

## 不记录

- 不记录模型内部推理过程。
- 不记录未脱敏密钥。
- 不记录不必要的个人敏感信息。
