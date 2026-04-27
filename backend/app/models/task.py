"""任务相关数据模型。"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """任务状态枚举。"""

    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class TaskCreateRequest(BaseModel):
    """创建任务请求。"""

    title: str = Field(..., min_length=1, max_length=200, description="任务标题")
    description: str = Field(..., min_length=1, description="任务描述")


class TaskQuery(BaseModel):
    """任务查询条件。"""

    status: TaskStatus | None = Field(default=None, description="按状态过滤")


class Task(BaseModel):
    """任务实体。"""

    id: str = Field(default_factory=lambda: str(uuid4()), description="任务 ID")
    title: str = Field(..., description="任务标题")
    description: str = Field(..., description="任务描述")
    status: TaskStatus = Field(default=TaskStatus.pending, description="任务状态")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="创建时间"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="更新时间"
    )
