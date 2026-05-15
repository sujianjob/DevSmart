"""工作流服务层。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.models.workflow_event import WorkflowStateEvent
from app.workflow.supervisor import WorkflowStatus, WorkflowSupervisor


@dataclass(slots=True)
class WorkflowTask:
    """任务最小模型。"""

    task_id: str
    status: str


class WorkflowRepository(Protocol):
    """工作流仓储接口。"""

    def get_task(self, task_id: str) -> WorkflowTask: ...

    def save_task_status(self, task_id: str, status: str) -> None: ...

    def add_workflow_event(self, event: WorkflowStateEvent) -> None: ...


class WorkflowService:
    """封装工作流状态推进逻辑。"""

    def __init__(self, repository: WorkflowRepository) -> None:
        self._repository = repository

    def start_workflow(self, task_id: str) -> WorkflowTask:
        """启动流程：created -> prd_generating -> clarifying -> pending_approval。"""

        self._advance(task_id, WorkflowStatus.PRD_GENERATING, actor="system", input_summary="启动工作流")
        self._advance(task_id, WorkflowStatus.CLARIFYING, actor="pm_agent", input_summary="PRD 初稿生成完成")
        self._advance(task_id, WorkflowStatus.PENDING_APPROVAL, actor="pm_agent", input_summary="澄清问题收敛")
        return self._repository.get_task(task_id)

    def approve_prd(self, task_id: str, comments: str) -> WorkflowTask:
        """批准 PRD：pending_approval -> task_splitting -> context_packaging -> completed。"""

        self._advance(task_id, WorkflowStatus.TASK_SPLITTING, actor="approver", input_summary=comments)
        self._advance(task_id, WorkflowStatus.CONTEXT_PACKAGING, actor="task_agent", input_summary="任务拆解完成")
        self._advance(task_id, WorkflowStatus.COMPLETED, actor="task_agent", input_summary="上下文包构建完成")
        return self._repository.get_task(task_id)

    def reject_prd(self, task_id: str, reason: str, comments: str) -> WorkflowTask:
        """驳回 PRD：pending_approval -> rejected。"""

        input_summary = f"reason={reason}; comments={comments}".strip()
        self._advance(task_id, WorkflowStatus.REJECTED, actor="approver", input_summary=input_summary)
        return self._repository.get_task(task_id)

    def _advance(
        self,
        task_id: str,
        target_status: WorkflowStatus,
        *,
        actor: str,
        input_summary: str,
    ) -> None:
        """推进一次状态并记录事件。"""

        task = self._repository.get_task(task_id)
        next_status = WorkflowSupervisor.transition(task.status, target_status.value)
        self._repository.save_task_status(task_id, next_status.value)

        event = WorkflowStateEvent.build(
            task_id=task_id,
            event_type="workflow_state_changed",
            actor=actor,
            input_summary=input_summary,
            output_summary=f"状态已更新为 {next_status.value}",
            from_status=task.status,
            to_status=next_status.value,
        )
        self._repository.add_workflow_event(event)


class InMemoryWorkflowRepository:
    """内存实现，便于本地运行和测试。"""

    def __init__(self) -> None:
        self.tasks: dict[str, WorkflowTask] = {}
        self.events: list[WorkflowStateEvent] = []

    def get_task(self, task_id: str) -> WorkflowTask:
        if task_id not in self.tasks:
            raise KeyError(f"任务不存在: {task_id}")
        return self.tasks[task_id]

    def save_task_status(self, task_id: str, status: str) -> None:
        task = self.get_task(task_id)
        self.tasks[task_id] = WorkflowTask(task_id=task.task_id, status=status)

    def add_workflow_event(self, event: WorkflowStateEvent) -> None:
        self.events.append(event)
