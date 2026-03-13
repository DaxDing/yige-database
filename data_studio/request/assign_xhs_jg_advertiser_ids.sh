#!/bin/sh
# 赋值节点 - 输出聚光 advertiser_id 列表（逗号分隔）
# 下游遍历节点通过 ${dag.foreach.current} 获取当前迭代值
# 从飞书 API 获取投放账户 ID 列表

WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/15c1fd3d-6cd5-4c5b-96e3-86c3cdf2b40e"

# 手动指定 advertiser_ids 时直接输出，跳过 API 请求
if [ -n "${jg_manual_ids}" ]; then
    echo "${jg_manual_ids}"
    exit 0
fi

response=$(curl -s -H "x-api-key: feishu_key" "http://121.41.12.184/feishu_api/lookup/jg?date=${bizdate}")
ids=$(echo "$response" | sed 's/.*\[//;s/\].*//;s/"//g;s/ //g')

if [ -z "$ids" ]; then
    safe_response=$(echo "$response" | sed 's/"/\\"/g')
    curl -s --location --request POST "$WEBHOOK_URL" \
        -H 'Content-Type: application/json' \
        -d "{\"msg_type\": \"text\", \"content\": {\"text\": \"聚光 advertiser_id 列表获取失败\\n报表: 实时计划\\n业务时间: ${bizdate}\\n时间: $(date '+%Y-%m-%d %H:%M:%S')\\nResponse: $safe_response\"}}" >/dev/null 2>&1

    echo "-1"
    exit 0
fi

echo "$ids"
