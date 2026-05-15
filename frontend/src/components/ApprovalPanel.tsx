import type { PRDApprovalStatus } from '../types';

export interface ApprovalPanelProps {
  status: PRDApprovalStatus;
  onApprove: () => void;
  onReject: () => void;
}

const STATUS_TEXT: Record<PRDApprovalStatus, string> = {
  draft: '草稿',
  reviewing: '评审中',
  approved: '已通过',
  rejected: '已驳回',
};

export function ApprovalPanel({ status, onApprove, onReject }: ApprovalPanelProps) {
  return (
    <section>
      <h3>审批面板</h3>
      <p>当前状态：{STATUS_TEXT[status]}</p>
      <button type="button" onClick={onApprove} disabled={status === 'approved'}>
        通过
      </button>
      <button type="button" onClick={onReject} disabled={status === 'rejected'}>
        驳回
      </button>
    </section>
  );
}
