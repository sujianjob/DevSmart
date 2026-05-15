import type { TaskStatus } from '../types';

const STATUS_LABEL_MAP: Record<TaskStatus, string> = {
  pending: '待处理',
  running: '进行中',
  blocked: '阻塞',
  completed: '已完成',
  failed: '失败',
};

export interface StatusTagProps {
  status: TaskStatus;
}

export function StatusTag({ status }: StatusTagProps) {
  return <span>状态：{STATUS_LABEL_MAP[status]}</span>;
}
