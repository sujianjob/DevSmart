import { useState } from 'react';
import { apiClient } from '../api/client';

export function TaskCreatePage() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [assignee, setAssignee] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const task = await apiClient.createTask({ title, description, assignee });
    setMessage(`任务创建成功：${task.id}`);
  };

  return (
    <main>
      <h1>任务创建</h1>
      <form onSubmit={handleSubmit}>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="任务标题" />
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="任务描述" />
        <input value={assignee} onChange={(e) => setAssignee(e.target.value)} placeholder="负责人" />
        <button type="submit">创建任务</button>
      </form>
      {message ? <p>{message}</p> : null}
    </main>
  );
}
