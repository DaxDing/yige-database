#!/bin/bash
# 创意层补数据：自动获取 token → 拉取聚光创意报表 → 写入 MaxCompute
# 用法: bash backfill.sh <advertiser_id> <start_date> <end_date>

set -euo pipefail

ADVERTISER_ID="${1:?用法: $0 <advertiser_id> <start_date> <end_date>}"
START_DATE="${2:?缺少 start_date (YYYY-MM-DD)}"
END_DATE="${3:?缺少 end_date (YYYY-MM-DD)}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# 加载环境变量
export $(grep -v '^#' "$PROJECT_ROOT/.env" | grep -v '^\s*$' | xargs)

# 获取 token
echo "获取聚光 token (advertiser_id=$ADVERTISER_ID)..."
TOKEN_RESPONSE=$(curl -s -X POST "http://121.41.12.184/api/xiaohongshu/token/valid" \
  -H "Content-Type: application/json" \
  -d "{\"advertiser_id\": $ADVERTISER_ID}")

TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('access_token','') or d.get('token',''))" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "token 获取失败，响应: $TOKEN_RESPONSE" >&2
  exit 1
fi
echo "token 获取成功"

# 执行补数据
python3 "$SCRIPT_DIR/load_creative_hi.py" \
  --start "$START_DATE" \
  --end "$END_DATE" \
  --advertiser-id "$ADVERTISER_ID" \
  --token "$TOKEN"
