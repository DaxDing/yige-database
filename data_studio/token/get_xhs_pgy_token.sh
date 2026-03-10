#!/bin/sh
# Shell 赋值节点：获取小红书蒲公英 Access Token
# 输入：${dag.foreach.current} = user_id
# 输出：Access-Token，供后续节点使用

API_URL="http://121.41.12.184/api/xiaohongshu/token/valid"
WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/15c1fd3d-6cd5-4c5b-96e3-86c3cdf2b40e"

response=$(curl -s --location --request POST "$API_URL" \
    -H 'Content-Type: application/json' \
    -d "{\"type\": \"pgy\", \"user_id\": \"${dag.foreach.current}\"}")

token=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$token" ]; then
    safe_response=$(echo "$response" | sed 's/"/\\"/g')
    curl -s --location --request POST "$WEBHOOK_URL" \
        -H 'Content-Type: application/json' \
        -d "{\"msg_type\": \"text\", \"content\": {\"text\": \"蒲公英 Token 获取失败\\n报表: 投后笔记\\n业务时间: ${bizdate}\\n时间: $(date '+%Y-%m-%d %H:%M:%S')\\nuser_id: ${dag.foreach.current}\\nResponse: $safe_response\"}}" >/dev/null 2>&1

    echo "-1"
    exit 0
fi

echo "${token}"
