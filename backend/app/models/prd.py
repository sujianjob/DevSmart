"""PRD 模型定义。"""

from datetime import datetime

from pydantic import BaseModel, Field


class PRD(BaseModel):
    """产品需求文档摘要。"""

    task_id: str = Field(..., description="关联任务 ID")
    background: str = Field(default="", description="需求背景")
    objective: str = Field(default="", description="目标说明")
    scope: str = Field(default="", description="范围定义")


class PRDSchema(BaseModel):
    """用于前后端联调的 PRD 数据模型。"""

    prd_id: str = Field(..., description="PRD 唯一标识")
    task_id: str = Field(..., description="所属任务标识")
    version: int = Field(..., ge=1, description="PRD 版本号")
    title: str = Field(..., description="PRD 标题")
    summary: str = Field(..., description="PRD 摘要")
    goals: list[str] = Field(default_factory=list, description="目标列表")
    non_goals: list[str] = Field(default_factory=list, description="非目标列表")
    functional_requirements: list[str] = Field(
        default_factory=list,
        description="功能需求列表",
    )
    risk_notes: list[str] = Field(default_factory=list, description="风险说明")
    status: str = Field(..., description="PRD 状态")
    created_at: datetime = Field(..., description="创建时间")
