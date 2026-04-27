"""任务相关 API。"""

from fastapi import APIRouter, HTTPException, Query

from app.models import Approval, Task, TaskCreateRequest, TaskStatus
from app.services import TASK_SERVICE

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, summary="创建任务")
def create_task(payload: TaskCreateRequest) -> Task:
    """创建新任务。"""

    return TASK_SERVICE.create_task(payload)


@router.get("", response_model=list[Task], summary="查询任务列表")
def list_tasks(status: TaskStatus | None = Query(default=None)) -> list[Task]:
    """按状态查询任务列表。"""

    return TASK_SERVICE.list_tasks(status=status)


@router.get("/{task_id}", response_model=Task, summary="查询任务详情")
def get_task(task_id: str) -> Task:
    """查询单个任务详情。"""

    task = TASK_SERVICE.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.post("/{task_id}/approve", response_model=Task, summary="审批任务")
def approve_task(task_id: str, approval: Approval) -> Task:
    """审批任务。"""

    task = TASK_SERVICE.approve_task(task_id, approval)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.post("/{task_id}/reject", response_model=Task, summary="驳回任务")
def reject_task(task_id: str, approval: Approval) -> Task:
    """驳回任务。"""

    task = TASK_SERVICE.reject_task(task_id, approval)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task
