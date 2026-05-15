import { useState } from 'react';
import { apiClient } from '../api/client';
import { EventTimeline } from '../components';
import type { Event } from '../types';

export function WorkflowReplayPage() {
  const [taskId, setTaskId] = useState('');
  const [events, setEvents] = useState<Event[]>([]);

  const handleReplay = async () => {
    const replayEvents = await apiClient.replayWorkflow(taskId);
    setEvents(replayEvents);
  };

  return (
    <main>
      <h1>工作流回放</h1>
      <input value={taskId} onChange={(e) => setTaskId(e.target.value)} placeholder="输入任务 ID" />
      <button type="button" onClick={handleReplay} disabled={!taskId}>
        回放
      </button>
      <EventTimeline events={events} />
    </main>
  );
}
