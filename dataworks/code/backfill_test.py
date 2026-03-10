"""DataWorks 冒烟测试触发节点脚本（支持日期范围）

Usage:
    export $(cat .env | xargs) && python3 dataworks/code/backfill_test.py
"""

import os
from datetime import datetime, timedelta

from alibabacloud_tea_openapi.models import Config
from alibabacloud_dataworks_public20200518.client import Client
from alibabacloud_dataworks_public20200518.models import RunSmokeTestRequest

ACCESS_KEY_ID = os.getenv("ALIYUN_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
ENDPOINT = "dataworks.cn-hangzhou.aliyuncs.com"

NODE_ID = 1033549414
BIZ_DATE_START = "2026-02-27"
BIZ_DATE_END = "2026-02-28"
JG_MANUAL_IDS = ""   # 聚光手动指定 advertiser_ids，逗号分隔
PGY_MANUAL_IDS = ""  # 蒲公英手动指定 user_ids，逗号分隔

client = Client(Config(
    access_key_id=ACCESS_KEY_ID,
    access_key_secret=ACCESS_KEY_SECRET,
    endpoint=ENDPOINT,
))

start = datetime.strptime(BIZ_DATE_START, "%Y-%m-%d")
end = datetime.strptime(BIZ_DATE_END, "%Y-%m-%d")
current = start

while current <= end:
    date_str = current.strftime("%Y-%m-%d")
    bizdate_str = date_str.replace("-", "")
    node_params = f"bizdate={bizdate_str}"
    if JG_MANUAL_IDS:
        node_params += f" jg_manual_ids={JG_MANUAL_IDS}"
    if PGY_MANUAL_IDS:
        node_params += f" pgy_manual_ids={PGY_MANUAL_IDS}"
    resp = client.run_smoke_test(RunSmokeTestRequest(
        project_env="PROD",
        bizdate=f"{date_str} 00:00:00",
        name=f"backfill_{NODE_ID}_{date_str}",
        node_id=NODE_ID,
        node_params=node_params,
    ))
    print(f"[{date_str}] dag_id={resp.body.data}")
    current += timedelta(days=1)
