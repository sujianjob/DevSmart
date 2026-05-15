"""FastAPI 应用入口。"""

from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["system"], summary="健康检查")
def health_check() -> dict[str, str]:
    """返回服务基础状态。"""

    return {"status": "ok", "env": settings.app_env}
