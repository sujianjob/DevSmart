import { useState } from 'react';
import { ApprovalPanel } from '../components';
import type { PRDApprovalStatus } from '../types';

export function PRDApprovalPage() {
  const [status, setStatus] = useState<PRDApprovalStatus>('reviewing');

  return (
    <main>
      <h1>PRD 审批</h1>
      <ApprovalPanel status={status} onApprove={() => setStatus('approved')} onReject={() => setStatus('rejected')} />
    </main>
  );
}
