from datetime import datetime, timedelta, timezone

from ..models import (
    ApprovalSchema,
    ContextPackageSchema,
    PRDSchema,
    TaskSchema,
    WorkflowEventSchema,
)


def generate_demo_workflow_data() -> list[dict]:
    """生成 3 组用于 UI 联调的演示任务流程数据。"""

    base_time = datetime(2026, 4, 25, 10, 0, tzinfo=timezone.utc)
    demos: list[dict] = []

    seeds = [
        {
            "task_id": "task_001",
            "requirement": "支持团队成员邮箱邀请",
            "status": "approved",
            "prd_title": "团队成员邀请功能",
            "prd_summary": "支持发送邀请、校验重复邀请并处理邀请过期。",
            "approval": {"approved": True, "comments": "同意进入任务拆解", "reason": None},
        },
        {
            "task_id": "task_002",
            "requirement": "新增邀请链接失效提醒",
            "status": "rejected",
            "prd_title": "邀请失效提醒能力",
            "prd_summary": "在邀请链接过期时给出明确反馈，并支持重新发送。",
            "approval": {
                "approved": False,
                "comments": "需要补充权限边界",
                "reason": "缺少管理员和成员的可见性差异",
            },
        },
        {
            "task_id": "task_003",
            "requirement": "增加邀请审计日志导出",
            "status": "in_progress",
            "prd_title": "邀请审计日志导出",
            "prd_summary": "支持按时间范围导出邀请审计日志用于合规审查。",
            "approval": {"approved": True, "comments": "可先做 MVP", "reason": None},
        },
    ]

    for idx, seed in enumerate(seeds, start=1):
        created_at = base_time + timedelta(hours=idx)
        task_id = seed["task_id"]
        prd_id = f"prd_{idx:03d}"
        context_package_id = f"ctx_{idx:03d}"

        task = TaskSchema(
            task_id=task_id,
            requirement=seed["requirement"],
            status=seed["status"],
            project_context={
                "tech_stack": ["React", "FastAPI"],
                "constraints": ["必须支持邀请过期", "所有字段使用 snake_case"],
            },
            prd_id=prd_id,
            current_context_package_id=context_package_id,
            created_at=created_at,
            updated_at=created_at + timedelta(minutes=15),
        )

        prd = PRDSchema(
            prd_id=prd_id,
            task_id=task_id,
            version=1,
            title=seed["prd_title"],
            summary=seed["prd_summary"],
            goals=["提升邀请成功率", "降低人工排查成本"],
            non_goals=["不涉及外部邮件服务替换"],
            functional_requirements=[
                "支持创建邀请并设置有效期",
                "支持重复邀请检测",
                "支持过期状态查询",
            ],
            risk_notes=["邮件延迟可能影响用户体验"],
            status="approved" if seed["approval"]["approved"] else "rejected",
            created_at=created_at + timedelta(minutes=5),
        )

        context_package = ContextPackageSchema(
            context_package_id=context_package_id,
            task_id=task_id,
            prd_summary=seed["prd_summary"],
            acceptance_criteria=[
                "邀请链接在过期后返回明确错误码",
                "重复邀请时给出可执行提示",
            ],
            technical_constraints=["后端统一 UTC 时间", "接口返回字段保持 snake_case"],
            suggested_files=[
                "backend/app/api/tasks.py",
                "frontend/src/pages/task-detail.tsx",
            ],
            api_contracts=["POST /tasks", "GET /tasks/{task_id}/events"],
            test_scenarios=["邀请成功", "重复邀请", "邀请过期"],
            open_questions=["是否需要批量导出"],
            created_at=created_at + timedelta(minutes=10),
        )

        events = [
            WorkflowEventSchema(
                event_id=f"evt_{idx:03d}_001",
                task_id=task_id,
                event_type="task_created",
                actor="pm_agent",
                input_summary=seed["requirement"],
                output_summary="任务创建成功",
                tool_calls=["planner.create_task"],
                artifact_refs=[task_id],
                created_at=created_at,
            ),
            WorkflowEventSchema(
                event_id=f"evt_{idx:03d}_002",
                task_id=task_id,
                event_type="prd_generated",
                actor="prd_agent",
                input_summary="基于需求生成 PRD",
                output_summary=f"产出 {prd_id}",
                tool_calls=["prd.generate"],
                artifact_refs=[prd_id],
                created_at=created_at + timedelta(minutes=5),
            ),
            WorkflowEventSchema(
                event_id=f"evt_{idx:03d}_003",
                task_id=task_id,
                event_type="approval_recorded",
                actor="human_reviewer",
                input_summary="人工审批 PRD",
                output_summary="记录审批结果",
                tool_calls=[],
                artifact_refs=[f"apr_{idx:03d}"],
                created_at=created_at + timedelta(minutes=12),
            ),
        ]

        approval = ApprovalSchema(
            approval_id=f"apr_{idx:03d}",
            task_id=task_id,
            prd_id=prd_id,
            approved=seed["approval"]["approved"],
            comments=seed["approval"]["comments"],
            reason=seed["approval"]["reason"],
            actor="product_owner",
            created_at=created_at + timedelta(minutes=12),
        )

        demos.append(
            {
                "task": task.model_dump(mode="json"),
                "prd": prd.model_dump(mode="json"),
                "context_package": context_package.model_dump(mode="json"),
                "events": [event.model_dump(mode="json") for event in events],
                "approval": approval.model_dump(mode="json"),
            }
        )

    return demos
