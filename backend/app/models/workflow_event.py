"""工作流事件模型。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


@dataclass(slots=True)
class WorkflowStateEvent:
    """运行时状态变更事件。"""

    event_id: str
    task_id: str
    event_type: str
    actor: str
    input_summary: str
    output_summary: str
    from_status: str
    to_status: str
    created_at: str

    @classmethod
    def build(
        cls,
        *,
        task_id: str,
        event_type: str,
        actor: str,
        input_summary: str,
        output_summary: str,
        from_status: str,
        to_status: str,
    ) -> "WorkflowStateEvent":
        """构造带时间戳和事件编号的事件对象。"""

        return cls(
            event_id=f"evt_{uuid4().hex}",
            task_id=task_id,
            event_type=event_type,
            actor=actor,
            input_summary=input_summary,
            output_summary=output_summary,
            from_status=from_status,
            to_status=to_status,
            created_at=datetime.now(tz=timezone.utc).isoformat(),
        )


class WorkflowEventSchema(BaseModel):
    """流程事件与审计记录模型。"""

    event_id: str = Field(..., description="事件唯一标识")
    task_id: str = Field(..., description="所属任务标识")
    event_type: str = Field(..., description="事件类型")
    actor: str = Field(..., description="事件发起角色")
    input_summary: str = Field(..., description="输入摘要")
    output_summary: str = Field(..., description="输出摘要")
    tool_calls: list[str] = Field(default_factory=list, description="工具调用摘要")
    artifact_refs: list[str] = Field(default_factory=list, description="关联产物引用")
    created_at: datetime = Field(..., description="创建时间")
