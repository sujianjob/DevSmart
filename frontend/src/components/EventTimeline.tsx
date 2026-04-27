import type { Event } from '../types';

export interface EventTimelineProps {
  events: Event[];
}

export function EventTimeline({ events }: EventTimelineProps) {
  if (events.length === 0) {
    return <p>暂无事件</p>;
  }

  return (
    <ol>
      {events.map((event) => (
        <li key={event.id}>
          <strong>{event.actor}</strong>：{event.message}
          <div>{new Date(event.createdAt).toLocaleString()}</div>
        </li>
      ))}
    </ol>
  );
}
