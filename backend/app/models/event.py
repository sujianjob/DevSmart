"""工作流事件模型。"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class WorkflowEvent(BaseModel):
    """工作流事件实体。"""

    id: str = Field(default_factory=lambda: str(uuid4()), description="事件 ID")
    task_id: str = Field(..., description="关联任务 ID")
    event_type: str = Field(..., description="事件类型")
    detail: str = Field(default="", description="事件详情")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="创建时间"
    )
