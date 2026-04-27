/**
 * 与后端对齐的任务状态。
 */
export type TaskStatus = 'pending' | 'running' | 'blocked' | 'completed' | 'failed';

/**
 * 任务实体。
 */
export interface Task {
  id: string;
  title: string;
  description: string;
  assignee: string;
  status: TaskStatus;
  createdAt: string;
  updatedAt: string;
}

/**
 * PRD 审批状态。
 */
export type PRDApprovalStatus = 'draft' | 'reviewing' | 'approved' | 'rejected';

/**
 * PRD 实体。
 */
export interface PRD {
  id: string;
  taskId: string;
  title: string;
  content: string;
  status: PRDApprovalStatus;
  reviewer?: string;
  submittedAt?: string;
}

/**
 * 工作流事件类型。
 */
export type EventType = 'task_created' | 'prd_submitted' | 'approved' | 'rejected' | 'task_split' | 'workflow_replayed';

/**
 * 事件实体。
 */
export interface Event {
  id: string;
  type: EventType;
  taskId: string;
  actor: string;
  message: string;
  createdAt: string;
}
