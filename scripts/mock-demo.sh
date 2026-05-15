#!/usr/bin/env bash
set -euo pipefail

# 可选脚本：写入演示数据，便于本地走通演示路径。
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEMO_DIR="$ROOT_DIR/demo"
DEMO_FILE="$DEMO_DIR/mock-demo-data.json"

mkdir -p "$DEMO_DIR"

cat > "$DEMO_FILE" <<'JSON'
{
  "generated_at": "2026-04-27T00:00:00Z",
  "flow": [
    {
      "step": "创建任务",
      "title": "支持批量导入客户线索",
      "owner": "产品经理"
    },
    {
      "step": "审批",
      "approver": "研发负责人",
      "status": "已通过"
    },
    {
      "step": "拆解",
      "tasks": [
        "后端接口设计",
        "前端导入页面",
        "校验规则与错误提示"
      ]
    },
    {
      "step": "回放",
      "artifact": "workflow-replay-001"
    }
  ]
}
JSON

echo "[DevSmart] 已写入演示数据：$DEMO_FILE"
echo "[DevSmart] 可按路径演示：创建任务 -> 审批 -> 拆解 -> 回放"
