"""服务层导出。"""

from app.services.task_service import TaskService

# 全局单例，方便当前内存实现共享状态。
TASK_SERVICE = TaskService()

__all__ = ["TaskService", "TASK_SERVICE"]
