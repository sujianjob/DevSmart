import type { Event, PRD, Task } from '../types';

const API_BASE_URL = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`请求失败：${response.status} ${response.statusText}`);
  }

  return (await response.json()) as T;
}

export const apiClient = {
  createTask(payload: Pick<Task, 'title' | 'description' | 'assignee'>) {
    return request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  getTask(taskId: string) {
    return request<Task>(`/tasks/${taskId}`);
  },

  getTaskEvents(taskId: string) {
    return request<Event[]>(`/tasks/${taskId}/events`);
  },

  submitPRDApproval(payload: Pick<PRD, 'id' | 'status'>) {
    return request<PRD>(`/prds/${payload.id}/approval`, {
      method: 'POST',
      body: JSON.stringify({ status: payload.status }),
    });
  },

  splitTask(taskId: string) {
    return request<Task[]>(`/tasks/${taskId}/split`, {
      method: 'POST',
    });
  },

  replayWorkflow(taskId: string) {
    return request<Event[]>(`/tasks/${taskId}/replay`, {
      method: 'POST',
    });
  },
};
