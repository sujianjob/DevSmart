"""审批模型定义。"""

from pydantic import BaseModel, Field


class Approval(BaseModel):
    """审批或驳回请求。"""

    reviewer: str = Field(..., min_length=1, description="审批人")
    comment: str = Field(default="", description="审批意见")
