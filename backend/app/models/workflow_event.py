from datetime import datetime

from pydantic import BaseModel, Field


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
