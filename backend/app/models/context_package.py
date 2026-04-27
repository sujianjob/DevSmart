"""上下文包模型定义。"""

from pydantic import BaseModel, Field


class ContextPackage(BaseModel):
    """任务执行上下文。"""

    task_id: str = Field(..., description="关联任务 ID")
    documents: list[str] = Field(default_factory=list, description="文档路径或标识")
    notes: str = Field(default="", description="补充说明")
