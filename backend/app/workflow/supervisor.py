"""工作流状态机入口（占位实现）。"""

from app.models.task import TaskStatus


class WorkflowSupervisor:
    """工作流总控入口。"""

    def next_status(self, current: TaskStatus, action: str) -> TaskStatus:
        """根据动作返回下一个状态。"""

        if current == TaskStatus.pending and action == "approve":
            return TaskStatus.approved
        if current == TaskStatus.pending and action == "reject":
            return TaskStatus.rejected
        return current
