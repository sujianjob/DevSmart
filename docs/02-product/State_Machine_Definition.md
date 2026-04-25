# 状态机定义

## 任务主状态

```text
created
  -> prd_generating
  -> clarifying
  -> pending_approval
  -> task_splitting
  -> context_packaging
  -> completed
```

异常状态：

```text
pending_approval -> rejected
任意状态 -> failed
```

## 审批状态

| 状态 | 说明 |
|:---|:---|
| pending | 等待人工审批 |
| approved | 审批通过 |
| rejected | 驳回，带反馈重新生成 |

## 事件记录

每次状态变化必须记录：

- `event_id`
- `task_id`
- `event_type`
- `actor`
- `input_summary`
- `output_summary`
- `created_at`

## 不记录

- 不记录模型内部推理过程。
- 不记录未脱敏密钥。
- 不记录不必要的源码全文。
