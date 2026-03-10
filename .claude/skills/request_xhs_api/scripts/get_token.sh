#!/bin/bash
# 获取小红书平台 Access Token
# Usage: get_token.sh <platform> [id]
#   platform: jg | pgy
#   id: advertiser_id (jg) | user_id (pgy)

set -euo pipefail

API_URL="http://121.41.12.184/api/xiaohongshu/token/valid"
PLATFORM="${1:?Usage: get_token.sh <jg|pgy> [id]}"
ID="${2:-}"

case "$PLATFORM" in
    jg)
        if [ -z "$ID" ]; then
            # 从环境变量或默认值获取
            ID="${XHS_JG_ADVERTISER_ID:-7152346}"
        fi
        BODY="{\"type\": \"jg\", \"advertiser_id\": $ID}"
        ;;
    pgy)
        if [ -z "$ID" ]; then
            ID="${XHS_PGY_USER_ID:-5cf89d080000000018003029}"
        fi
        BODY="{\"type\": \"pgy\", \"user_id\": \"$ID\"}"
        ;;
    *)
        echo "Error: platform must be jg or pgy" >&2
        exit 1
        ;;
esac

response=$(curl -s --location --request POST "$API_URL" \
    -H 'Content-Type: application/json' \
    -d "$BODY")

token=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$token" ]; then
    echo "Error: token fetch failed - $response" >&2
    exit 1
fi

echo "$token"
