#!/usr/bin/env bash
set -euo pipefail

# 仅用于本地手动启动后端，不涉及任何自动化 CI/CD。
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

echo "[DevSmart] 手动启动后端服务（FastAPI）"
echo "[DevSmart] 若首次运行，请先手动安装依赖：pip install -r requirements.txt"

exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
