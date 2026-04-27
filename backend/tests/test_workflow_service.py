"""工作流服务测试。"""

from backend.app.services.workflow_service import InMemoryWorkflowRepository, WorkflowService, WorkflowTask
from backend.app.workflow.supervisor import WorkflowStatus, WorkflowTransitionError


def _build_service() -> tuple[WorkflowService, InMemoryWorkflowRepository]:
    repo = InMemoryWorkflowRepository()
    repo.tasks["task_1"] = WorkflowTask(task_id="task_1", status=WorkflowStatus.CREATED.value)
    return WorkflowService(repo), repo


def test_start_workflow_to_pending_approval() -> None:
    service, repo = _build_service()

    task = service.start_workflow("task_1")

    assert task.status == WorkflowStatus.PENDING_APPROVAL.value
    assert [event.to_status for event in repo.events] == [
        WorkflowStatus.PRD_GENERATING.value,
        WorkflowStatus.CLARIFYING.value,
        WorkflowStatus.PENDING_APPROVAL.value,
    ]


def test_approve_prd_to_completed() -> None:
    service, repo = _build_service()
    service.start_workflow("task_1")

    task = service.approve_prd("task_1", comments="同意")

    assert task.status == WorkflowStatus.COMPLETED.value
    assert [event.to_status for event in repo.events][-3:] == [
        WorkflowStatus.TASK_SPLITTING.value,
        WorkflowStatus.CONTEXT_PACKAGING.value,
        WorkflowStatus.COMPLETED.value,
    ]


def test_reject_prd_to_rejected() -> None:
    service, repo = _build_service()
    service.start_workflow("task_1")

    task = service.reject_prd("task_1", reason="信息不足", comments="补充异常路径")

    assert task.status == WorkflowStatus.REJECTED.value
    assert repo.events[-1].to_status == WorkflowStatus.REJECTED.value


def test_approve_without_pending_should_fail() -> None:
    service, _ = _build_service()

    try:
        service.approve_prd("task_1", comments="同意")
    except WorkflowTransitionError:
        pass
    else:
        raise AssertionError("预期触发 WorkflowTransitionError")
