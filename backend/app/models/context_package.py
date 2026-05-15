"""上下文包模型定义。"""

from datetime import datetime

from pydantic import BaseModel, Field


class ContextPackage(BaseModel):
    """任务执行上下文。"""

    task_id: str = Field(..., description="关联任务 ID")
    documents: list[str] = Field(default_factory=list, description="文档路径或标识")
    notes: str = Field(default="", description="补充说明")


class ContextPackageSchema(BaseModel):
    """用于前后端联调的任务上下文包模型。"""

    context_package_id: str = Field(..., description="上下文包唯一标识")
    task_id: str = Field(..., description="所属任务标识")
    prd_summary: str = Field(..., description="PRD 摘要")
    acceptance_criteria: list[str] = Field(default_factory=list, description="验收标准")
    technical_constraints: list[str] = Field(default_factory=list, description="技术约束")
    suggested_files: list[str] = Field(default_factory=list, description="建议修改文件")
    api_contracts: list[str] = Field(default_factory=list, description="接口契约")
    test_scenarios: list[str] = Field(default_factory=list, description="测试场景")
    open_questions: list[str] = Field(default_factory=list, description="待确认问题")
    created_at: datetime = Field(..., description="创建时间")
