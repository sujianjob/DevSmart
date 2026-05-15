"""应用基础配置。"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    """环境变量配置。"""

    app_name: str
    app_env: str
    app_host: str
    app_port: int


def load_settings() -> Settings:
    """从环境变量加载配置。"""

    return Settings(
        app_name=os.getenv("APP_NAME", "DevSmart Backend"),
        app_env=os.getenv("APP_ENV", "dev"),
        app_host=os.getenv("APP_HOST", "0.0.0.0"),
        app_port=int(os.getenv("APP_PORT", "8000")),
    )


settings = load_settings()
