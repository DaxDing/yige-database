"""DataWorks DAG 执行状态查询

Usage:
    export $(cat .env | xargs) && python3 dataworks/code/check_dag.py <dag_id>
"""

import os
import sys
from datetime import datetime, timezone, timedelta

from alibabacloud_tea_openapi.models import Config
from alibabacloud_dataworks_public20200518.client import Client
from alibabacloud_dataworks_public20200518.models import GetDagRequest

ACCESS_KEY_ID = os.getenv("ALIYUN_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
ENDPOINT = "dataworks.cn-hangzhou.aliyuncs.com"

DAG_ID = int(sys.argv[1]) if len(sys.argv) > 1 else None
if not DAG_ID:
    print("Usage: python3 check_dag.py <dag_id>")
    sys.exit(1)

tz = timezone(timedelta(hours=8))

def fmt_ts(ts):
    if not ts:
        return "-"
    return datetime.fromtimestamp(ts / 1000, tz).strftime("%Y-%m-%d %H:%M:%S")

client = Client(Config(
    access_key_id=ACCESS_KEY_ID,
    access_key_secret=ACCESS_KEY_SECRET,
    endpoint=ENDPOINT,
))

resp = client.get_dag(GetDagRequest(dag_id=DAG_ID, project_env="PROD"))
d = resp.body.data

status_icon = {"SUCCESS": "✅", "FAILURE": "❌", "RUNNING": "🔄", "CREATED": "⏳"}
print(f"DAG: {d.dag_id}  状态: {status_icon.get(d.status, '')} {d.status}")
print(f"名称: {d.name}")
print(f"类型: {d.type}")
print(f"业务日期: {fmt_ts(d.bizdate)}")
print(f"创建时间: {fmt_ts(d.create_time)}")
print(f"开始时间: {fmt_ts(d.start_time)}")
print(f"结束时间: {fmt_ts(d.finish_time)}")
