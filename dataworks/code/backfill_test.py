"""DataWorks 补数据测试脚本

Usage:
    export $(cat .env | xargs) && python3 dataworks/code/run_workflow.py
"""

import os
import time

from alibabacloud_tea_openapi.models import Config
from alibabacloud_dataworks_public20200518.client import Client
from alibabacloud_dataworks_public20200518.models import (
    RunCycleDagNodesRequest,
    GetDagRequest,
)

NODE_ID = 1033546459
BIZ_DATE = "2026-02-27 00:00:00"

client = Client(Config(
    access_key_id=os.getenv("ALIYUN_ACCESS_KEY_ID"),
    access_key_secret=os.getenv("ALIYUN_ACCESS_KEY_SECRET"),
    endpoint="dataworks.cn-hangzhou.aliyuncs.com",
))

# 1. 触发补数据
print(f"触发补数据: 节点={NODE_ID}, 业务日期={BIZ_DATE}")
resp = client.run_cycle_dag_nodes(RunCycleDagNodesRequest(
    project_env="PROD",
    root_node_id=NODE_ID,
    name=str(NODE_ID),
    start_biz_date=BIZ_DATE,
    end_biz_date=BIZ_DATE,
    include_node_ids=str(NODE_ID),
    parallelism=True,
))
dag_id = resp.body.data
print(f"DAG ID: {dag_id}")

# 2. 轮询状态
print("等待执行完成...")
for i in range(60):
    time.sleep(10)
    resp = client.get_dag(GetDagRequest(project_env="PROD", dag_id=dag_id))
    status = resp.body.data.status
    print(f"  [{(i+1)*10}s] {status}")

    if status == "SUCCESS":
        print("补数据完成!")
        break
    if status == "FAILURE":
        print("补数据失败!")
        break
else:
    print("超时(600s)")
