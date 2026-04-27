"""PRD 模型定义。"""

from pydantic import BaseModel, Field


class PRD(BaseModel):
    """产品需求文档摘要。"""

    task_id: str = Field(..., description="关联任务 ID")
    background: str = Field(default="", description="需求背景")
    objective: str = Field(default="", description="目标说明")
    scope: str = Field(default="", description="范围定义")
