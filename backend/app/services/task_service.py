"""任务服务层：当前使用内存存储。"""

from __future__ import annotations

from datetime import datetime, timezone

from app.models import Approval, Task, TaskCreateRequest, TaskStatus, WorkflowEvent


class TaskService:
    """任务服务，负责任务生命周期。"""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._events: list[WorkflowEvent] = []

    def create_task(self, payload: TaskCreateRequest) -> Task:
        task = Task(title=payload.title, description=payload.description)
        self._tasks[task.id] = task
        self._append_event(task.id, "task_created", f"任务 {task.title} 已创建")
        return task

    def get_task(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list_tasks(self, status: TaskStatus | None = None) -> list[Task]:
        tasks = list(self._tasks.values())
        if status is None:
            return tasks
        return [task for task in tasks if task.status == status]

    def approve_task(self, task_id: str, approval: Approval) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.status = TaskStatus.approved
        task.updated_at = datetime.now(timezone.utc)
        self._append_event(task_id, "task_approved", f"审批人：{approval.reviewer}；{approval.comment}")
        return task

    def reject_task(self, task_id: str, approval: Approval) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.status = TaskStatus.rejected
        task.updated_at = datetime.now(timezone.utc)
        self._append_event(task_id, "task_rejected", f"审批人：{approval.reviewer}；{approval.comment}")
        return task

    def list_events(self, task_id: str | None = None) -> list[WorkflowEvent]:
        if task_id is None:
            return list(self._events)
        return [event for event in self._events if event.task_id == task_id]

    def _append_event(self, task_id: str, event_type: str, detail: str) -> None:
        self._events.append(
            WorkflowEvent(task_id=task_id, event_type=event_type, detail=detail)
        )
