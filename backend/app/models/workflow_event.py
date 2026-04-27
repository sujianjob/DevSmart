"""工作流事件模型。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True)
class WorkflowEvent:
    """状态变更事件。"""

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
    ) -> "WorkflowEvent":
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
