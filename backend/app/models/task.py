from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TaskSchema(BaseModel):
    """任务主数据模型。"""

    task_id: str = Field(..., description="任务唯一标识")
    requirement: str = Field(..., description="原始需求描述")
    status: str = Field(..., description="任务状态")
    project_context: dict[str, Any] = Field(default_factory=dict, description="项目上下文")
    prd_id: str | None = Field(default=None, description="当前关联 PRD 标识")
    current_context_package_id: str | None = Field(
        default=None,
        description="当前关联上下文包标识",
    )
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
