#!/bin/sh
# Shell 赋值节点：获取有效的 advertiser_id 列表
# 调度参数：Access-Token, user_id
# 输出：逗号分隔的 advertiser_id，供 for-each 遍历使用

all_ids=""
count=0
max_count=2

while true; do
    response=$(curl -s -X POST 'https://adapi.xiaohongshu.com/api/open/jg/account/sub/page' \
        -H "Access-Token: ${Access-Token}" \
        -H 'Content-Type: application/json' \
        -d "{\"user_id\": \"${user_id}\", \"page\": 1, \"page_size\": 50}")

    ids=$(echo "$response" | sed 's/},/}\n/g' | grep '"virtual_seller_status":"有效"' | grep -o '"advertiser_id":[0-9]*' | grep -o '[0-9]*')

    for id in $ids; do
        if [ -n "$all_ids" ]; then
            all_ids="${all_ids},${id}"
        else
            all_ids="$id"
        fi
        count=$((count + 1))
        if [ "$count" -ge "$max_count" ]; then
            break 2
        fi
    done

    break
done

echo "$all_ids"
