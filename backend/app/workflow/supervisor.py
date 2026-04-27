"""工作流状态监管器。"""

from __future__ import annotations

from enum import Enum


class WorkflowStatus(str, Enum):
    """任务流程状态。"""

    CREATED = "created"
    PRD_GENERATING = "prd_generating"
    CLARIFYING = "clarifying"
    PENDING_APPROVAL = "pending_approval"
    TASK_SPLITTING = "task_splitting"
    CONTEXT_PACKAGING = "context_packaging"
    COMPLETED = "completed"
    REJECTED = "rejected"
    FAILED = "failed"


_ALLOWED_TRANSITIONS: dict[WorkflowStatus, set[WorkflowStatus]] = {
    WorkflowStatus.CREATED: {WorkflowStatus.PRD_GENERATING, WorkflowStatus.FAILED},
    WorkflowStatus.PRD_GENERATING: {WorkflowStatus.CLARIFYING, WorkflowStatus.FAILED},
    WorkflowStatus.CLARIFYING: {WorkflowStatus.PENDING_APPROVAL, WorkflowStatus.FAILED},
    WorkflowStatus.PENDING_APPROVAL: {
        WorkflowStatus.TASK_SPLITTING,
        WorkflowStatus.REJECTED,
        WorkflowStatus.FAILED,
    },
    WorkflowStatus.TASK_SPLITTING: {WorkflowStatus.CONTEXT_PACKAGING, WorkflowStatus.FAILED},
    WorkflowStatus.CONTEXT_PACKAGING: {WorkflowStatus.COMPLETED, WorkflowStatus.FAILED},
    WorkflowStatus.COMPLETED: set(),
    WorkflowStatus.REJECTED: {WorkflowStatus.FAILED},
    WorkflowStatus.FAILED: set(),
}


class WorkflowTransitionError(ValueError):
    """状态流转非法时抛出。"""


class WorkflowSupervisor:
    """负责校验任务状态机流转规则。"""

    @staticmethod
    def transition(current_status: str, target_status: str) -> WorkflowStatus:
        """从当前状态迁移到目标状态，并进行合法性校验。"""

        try:
            current = WorkflowStatus(current_status)
            target = WorkflowStatus(target_status)
        except ValueError as exc:
            raise WorkflowTransitionError(f"未知状态: {current_status} -> {target_status}") from exc

        if target not in _ALLOWED_TRANSITIONS[current]:
            raise WorkflowTransitionError(f"非法状态流转: {current.value} -> {target.value}")

        return target
