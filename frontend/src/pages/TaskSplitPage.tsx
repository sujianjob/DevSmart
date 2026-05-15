import { useState } from 'react';
import { apiClient } from '../api/client';

export function TaskSplitPage() {
  const [taskId, setTaskId] = useState('');
  const [resultCount, setResultCount] = useState<number | null>(null);

  const handleSplit = async () => {
    const splitTasks = await apiClient.splitTask(taskId);
    setResultCount(splitTasks.length);
  };

  return (
    <main>
      <h1>任务拆分</h1>
      <input value={taskId} onChange={(e) => setTaskId(e.target.value)} placeholder="输入任务 ID" />
      <button type="button" onClick={handleSplit} disabled={!taskId}>
        执行拆分
      </button>
      {resultCount !== null ? <p>已生成子任务：{resultCount} 个</p> : null}
    </main>
  );
}
