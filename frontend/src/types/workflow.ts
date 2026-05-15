export interface TaskSchema {
  task_id: string;
  requirement: string;
  status: string;
  project_context: Record<string, unknown>;
  prd_id?: string | null;
  current_context_package_id?: string | null;
  created_at: string;
  updated_at: string;
}

export interface PRDSchema {
  prd_id: string;
  task_id: string;
  version: number;
  title: string;
  summary: string;
  goals: string[];
  non_goals: string[];
  functional_requirements: string[];
  risk_notes: string[];
  status: string;
  created_at: string;
}

export interface ContextPackageSchema {
  context_package_id: string;
  task_id: string;
  prd_summary: string;
  acceptance_criteria: string[];
  technical_constraints: string[];
  suggested_files: string[];
  api_contracts: string[];
  test_scenarios: string[];
  open_questions: string[];
  created_at: string;
}

export interface WorkflowEventSchema {
  event_id: string;
  task_id: string;
  event_type: string;
  actor: string;
  input_summary: string;
  output_summary: string;
  tool_calls: string[];
  artifact_refs: string[];
  created_at: string;
}

export interface ApprovalSchema {
  approval_id: string;
  task_id: string;
  prd_id: string;
  approved: boolean;
  comments: string;
  reason?: string | null;
  actor: string;
  created_at: string;
}

export interface DemoWorkflowBundle {
  task: TaskSchema;
  prd: PRDSchema;
  context_package: ContextPackageSchema;
  events: WorkflowEventSchema[];
  approval: ApprovalSchema;
}
