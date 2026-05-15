"""API 路由聚合。"""

from fastapi import APIRouter

from app.api import events, tasks

api_router = APIRouter()
api_router.include_router(tasks.router)
api_router.include_router(events.router)
