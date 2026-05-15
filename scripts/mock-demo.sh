#!/usr/bin/env bash
set -euo pipefail

# 可选脚本：写入演示数据，便于本地走通需求澄清到 PRD/AC 的演示路径。
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEMO_DIR="$ROOT_DIR/demo"
DEMO_FILE="$DEMO_DIR/mock-demo-data.json"

mkdir -p "$DEMO_DIR"

cat > "$DEMO_FILE" <<'JSON'
{
  "generated_at": "2026-05-15T00:00:00Z",
  "flow": [
    {
      "step": "输入需求",
      "content": "支持批量导入客户线索",
      "owner": "产品经理"
    },
    {
      "step": "澄清问题",
      "questions": [
        "导入文件支持哪些格式？",
        "重复客户线索如何处理？",
        "导入失败时是否需要下载错误明细？"
      ]
    },
    {
      "step": "PRD 生成",
      "sections": [
        "背景与目标",
        "目标用户",
        "用户故事",
        "功能范围",
        "非目标"
      ]
    },
    {
      "step": "AC 生成",
      "items": [
        "有效文件上传后应生成导入任务并展示处理进度",
        "重复线索应按用户确认的规则跳过或覆盖",
        "失败记录应提供可下载的错误明细"
      ]
    },
    {
      "step": "评审输出",
      "artifact": "requirement-package-001"
    }
  ]
}
JSON

echo "[DevSmart] 已写入演示数据：$DEMO_FILE"
echo "[DevSmart] 可按路径演示：输入需求 -> 澄清问题 -> PRD 生成 -> AC 生成 -> 评审输出"
