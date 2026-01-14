# -*- coding: utf-8 -*-
"""
PyODPS 3 节点：获取有效的 advertiser_id 列表
参数：Access_Token, user_id
输出：逗号分隔的 advertiser_id
"""
import requests

# 获取参数
ACCESS_TOKEN = args['Access-Token']
USER_ID = args['user_id']

# API 配置
url = 'https://adapi.xiaohongshu.com/api/open/jg/account/sub/page'
headers = {
    'Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

# 获取所有有效 advertiser_id
valid_ids = []
page = 1

while True:
    payload = {
        'user_id': USER_ID,
        'page': page,
        'page_size': 50
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    data = resp.json()

    if not data.get('success'):
        raise Exception('API error: ' + data.get('msg', ''))

    for item in data['data']['sub_accounts']:
        if item.get('virtual_seller_status') == '有效':
            valid_ids.append(str(item['advertiser_id']))

    total = data['data']['total']
    if page * 50 >= total:
        break

    page += 1

# 输出结果
print(','.join(valid_ids))
