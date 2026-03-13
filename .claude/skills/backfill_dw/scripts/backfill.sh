#!/bin/bash
# 创意层补数据：自动获取 token → 核对 ODS → 合并写入 → 重跑 DWD
# 用法: bash backfill.sh <advertiser_ids> <start_date> <end_date>
# 示例: bash backfill.sh 9590195,8936364,8517830 2026-02-14 2026-03-12

set -euo pipefail

ADV_IDS="${1:?用法: $0 <advertiser_ids> <start_date> <end_date>}"
START_DATE="${2:?缺少 start_date (YYYY-MM-DD)}"
END_DATE="${3:?缺少 end_date (YYYY-MM-DD)}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# 加载环境变量
export $(grep -v '^#' "$PROJECT_ROOT/.env" | grep -v '^\s*$' | xargs)

# 逐个 advertiser_id 获取 token
IFS=',' read -ra ID_ARRAY <<< "$ADV_IDS"
TOKENS=""

for ADV_ID in "${ID_ARRAY[@]}"; do
  echo "获取聚光 token (advertiser_id=$ADV_ID)..."
  TOKEN_RESPONSE=$(curl -s -X POST "http://121.41.12.184/api/xiaohongshu/token/valid" \
    -H "Content-Type: application/json" \
    -d "{\"type\": \"jg\", \"advertiser_id\": $ADV_ID}")

  TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('access_token','') or d.get('token',''))" 2>/dev/null)

  if [ -z "$TOKEN" ]; then
    echo "advertiser_id=$ADV_ID token 获取失败: $TOKEN_RESPONSE" >&2
    exit 1
  fi
  echo "  token 获取成功"

  if [ -n "$TOKENS" ]; then
    TOKENS="$TOKENS,$TOKEN"
  else
    TOKENS="$TOKEN"
  fi
done

# 执行补数据
python3 "$SCRIPT_DIR/load_creative_hi.py" \
  --start "$START_DATE" \
  --end "$END_DATE" \
  --advertiser-ids "$ADV_IDS" \
  --tokens "$TOKENS"
