"""事件查询与 SSE 推送 API。"""

from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.models import WorkflowEvent
from app.services import TASK_SERVICE

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[WorkflowEvent], summary="查询事件列表")
def list_events(task_id: str | None = Query(default=None)) -> list[WorkflowEvent]:
    """查询任务事件。"""

    return TASK_SERVICE.list_events(task_id=task_id)


@router.get("/stream", summary="SSE 事件流")
async def stream_events(task_id: str | None = Query(default=None)) -> StreamingResponse:
    """返回简单轮询实现的 SSE 事件流。"""

    async def event_generator() -> AsyncGenerator[str, None]:
        sent_ids: set[str] = set()
        while True:
            events = TASK_SERVICE.list_events(task_id=task_id)
            for event in events:
                if event.id in sent_ids:
                    continue
                sent_ids.add(event.id)
                payload = json.dumps(event.model_dump(mode="json"), ensure_ascii=False)
                yield f"event: workflow\ndata: {payload}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
