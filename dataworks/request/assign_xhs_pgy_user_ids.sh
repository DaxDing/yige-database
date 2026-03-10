#!/bin/sh
# 赋值节点 - 输出蒲公英 user_id 列表（逗号分隔）
# 下游遍历节点通过 ${dag.foreach.current} 获取当前迭代值
# 从飞书 API 获取蒲公英用户 ID 列表

WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/15c1fd3d-6cd5-4c5b-96e3-86c3cdf2b40e"

# 手动指定 user_ids 时直接输出，跳过 API 请求
if [ -n "${pgy_manual_ids}" ]; then
    echo "${pgy_manual_ids}"
    exit 0
fi

response=$(curl -s -H "x-api-key: feishu_key" "http://121.41.12.184/feishu_api/lookup/pgy?date=${bizdate}")
ids=$(echo "$response" | sed 's/.*"user_id":\[//;s/\].*//;s/"//g')

if [ -z "$ids" ]; then
    safe_response=$(echo "$response" | sed 's/"/\\"/g')
    curl -s --location --request POST "$WEBHOOK_URL" \
        -H 'Content-Type: application/json' \
        -d "{\"msg_type\": \"text\", \"content\": {\"text\": \"蒲公英 user_id 列表获取失败\\n报表: 投后笔记\\n业务时间: ${bizdate}\\n时间: $(date '+%Y-%m-%d %H:%M:%S')\\nResponse: $safe_response\"}}" >/dev/null 2>&1

    echo "-1"
    exit 0
fi

echo "$ids"
