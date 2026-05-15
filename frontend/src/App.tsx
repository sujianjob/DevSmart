import { Navigate, Route, Routes } from 'react-router-dom';
import {
  HomePage,
  PRDApprovalPage,
  TaskCreatePage,
  TaskSplitPage,
  WorkflowReplayPage,
} from './pages';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/tasks/create" element={<TaskCreatePage />} />
      <Route path="/prd/approval" element={<PRDApprovalPage />} />
      <Route path="/tasks/split" element={<TaskSplitPage />} />
      <Route path="/workflow/replay" element={<WorkflowReplayPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
