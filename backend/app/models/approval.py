"""审批模型定义。"""

from datetime import datetime

from pydantic import BaseModel, Field


class Approval(BaseModel):
    """审批或驳回请求。"""

    reviewer: str = Field(..., min_length=1, description="审批人")
    comment: str = Field(default="", description="审批意见")


class ApprovalSchema(BaseModel):
    """用于前后端联调的人工审批记录模型。"""

    approval_id: str = Field(..., description="审批记录唯一标识")
    task_id: str = Field(..., description="所属任务标识")
    prd_id: str = Field(..., description="审批目标 PRD 标识")
    approved: bool = Field(..., description="是否批准")
    comments: str = Field(default="", description="审批备注")
    reason: str | None = Field(default=None, description="驳回原因")
    actor: str = Field(..., description="审批人或角色")
    created_at: datetime = Field(..., description="审批时间")
