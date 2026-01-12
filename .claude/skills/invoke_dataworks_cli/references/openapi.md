# DataWorks OpenAPI

## 概述

DataWorks 提供 OpenAPI 接口，支持通过 API 管理数据开发、调度、运维等功能。

## 认证方式

### AccessKey 认证

```bash
# 环境变量
export ALIBABA_CLOUD_ACCESS_KEY_ID=xxx
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=xxx
```

### SDK 调用

```python
from alibabacloud_dataworks_public20200518.client import Client
from alibabacloud_tea_openapi.models import Config

config = Config(
    access_key_id='xxx',
    access_key_secret='xxx',
    region_id='cn-hangzhou'
)
client = Client(config)
```

## 常用 API

### 项目管理

| API | 说明 |
|-----|------|
| `ListProjects` | 列出项目 |
| `GetProject` | 获取项目详情 |
| `CreateProject` | 创建项目 |
| `UpdateProject` | 更新项目 |

### 节点管理

| API | 说明 |
|-----|------|
| `ListNodes` | 列出节点 |
| `GetNode` | 获取节点详情 |
| `CreateFile` | 创建文件/节点 |
| `UpdateFile` | 更新文件/节点 |
| `DeleteFile` | 删除文件/节点 |
| `DeployFile` | 发布文件 |

### 实例管理

| API | 说明 |
|-----|------|
| `ListInstances` | 列出实例 |
| `GetInstance` | 获取实例详情 |
| `GetInstanceLog` | 获取实例日志 |
| `RunCycleDagNodes` | 运行周期任务 |
| `RunSmokeTest` | 冒烟测试 |
| `RerunInstance` | 重跑实例 |
| `StopInstance` | 停止实例 |

### 数据源管理

| API | 说明 |
|-----|------|
| `ListDataSources` | 列出数据源 |
| `GetDataSource` | 获取数据源详情 |
| `CreateDataSource` | 创建数据源 |
| `UpdateDataSource` | 更新数据源 |
| `DeleteDataSource` | 删除数据源 |

## CLI 调用示例

### 列出项目

```bash
aliyun dataworks-public ListProjects \
  --region cn-hangzhou \
  --PageSize 100
```

### 列出节点

```bash
aliyun dataworks-public ListNodes \
  --region cn-hangzhou \
  --ProjectId 530486 \
  --PageSize 100
```

### 获取实例日志

```bash
aliyun dataworks-public GetInstanceLog \
  --region cn-hangzhou \
  --ProjectEnv PROD \
  --InstanceId 123456789
```

### 触发任务运行

```bash
aliyun dataworks-public RunCycleDagNodes \
  --region cn-hangzhou \
  --ProjectEnv PROD \
  --NodeId 123456 \
  --BizDate "2026-01-07"
```

### 创建数据源

```bash
aliyun dataworks-public CreateDataSource \
  --region cn-hangzhou \
  --ProjectId 530486 \
  --Name "my_pg_source" \
  --Type "postgresql" \
  --ConnectionPropertiesMode "UrlMode" \
  --ConnectionProperties '{
    "address": [{"host": "pgm-xxx.pg.rds.aliyuncs.com", "port": "5432"}],
    "database": "mydb",
    "username": "user",
    "password": "pass",
    "envType": "Prod"
  }'
```

## Python SDK 示例

### 安装

```bash
pip install alibabacloud_dataworks_public20200518
```

### 列出项目

```python
from alibabacloud_dataworks_public20200518.client import Client
from alibabacloud_dataworks_public20200518.models import ListProjectsRequest
from alibabacloud_tea_openapi.models import Config

config = Config(
    access_key_id='xxx',
    access_key_secret='xxx',
    region_id='cn-hangzhou'
)
client = Client(config)

request = ListProjectsRequest(page_size=100)
response = client.list_projects(request)
print(response.body.data.projects)
```

### 触发任务

```python
from alibabacloud_dataworks_public20200518.models import RunCycleDagNodesRequest

request = RunCycleDagNodesRequest(
    project_env='PROD',
    node_id=123456,
    biz_date='2026-01-07'
)
response = client.run_cycle_dag_nodes(request)
print(response.body)
```

## 数据服务 API

### 创建 API

DataWorks 支持将数据表快速发布为 API：

**路径**：数据服务 → 新建 API

配置：
1. 选择数据源和表
2. 配置请求参数
3. 配置返回字段
4. 设置访问权限

### API 调用

```bash
curl -X POST "https://xxx.cn-hangzhou.aliyuncs.com/api/path" \
  -H "Content-Type: application/json" \
  -H "appCode: your_app_code" \
  -d '{"param1": "value1"}'
```

## 错误码

| 错误码 | 说明 | 解决 |
|--------|------|------|
| `InvalidParameter` | 参数错误 | 检查参数格式 |
| `Forbidden` | 无权限 | 检查 RAM 权限 |
| `Throttling` | 请求过频 | 降低调用频率 |
| `InternalError` | 内部错误 | 稍后重试 |

## 最佳实践

### 批量操作

```python
# 分页获取所有节点
all_nodes = []
page_number = 1
while True:
    request = ListNodesRequest(
        project_id=project_id,
        page_number=page_number,
        page_size=100
    )
    response = client.list_nodes(request)
    nodes = response.body.data.nodes
    if not nodes:
        break
    all_nodes.extend(nodes)
    page_number += 1
```

### 错误重试

```python
import time
from alibabacloud_tea_util.models import RuntimeOptions

runtime = RuntimeOptions(
    autoretry=True,
    max_attempts=3,
    read_timeout=30000,
    connect_timeout=30000
)

response = client.list_projects_with_options(request, runtime)
```
