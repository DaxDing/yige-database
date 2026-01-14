# DataWorks Python 节点

## 节点类型

| 类型 | 用途 | 运行环境 |
|------|------|---------|
| **PyODPS** | MaxCompute Python 开发 | MaxCompute 集群 |
| **Python 赋值节点** | 参数传递 | Serverless |
| **Notebook** | 交互式分析 | 个人开发环境 |

## PyODPS 节点

### 创建

新建 → MaxCompute → PyODPS 2

### 内置变量

| 变量 | 说明 |
|------|------|
| `odps` | MaxCompute 入口对象 |
| `o` | 同 odps |
| `args` | 调度参数字典 |

### 基础用法

```python
# 执行 SQL
odps.execute_sql('SELECT * FROM table LIMIT 10')

# 获取表
table = odps.get_table('table_name')
print(table.schema)

# 读取数据
with table.open_reader() as reader:
    for record in reader:
        print(record)

# 写入数据
with table.open_writer() as writer:
    writer.write([['value1', 'value2']])
```

### 使用调度参数

```python
# 获取调度参数
bizdate = args['bizdate']
custom_param = args.get('custom_param', 'default')

# SQL 中使用参数
sql = f"SELECT * FROM table WHERE ds = '{bizdate}'"
odps.execute_sql(sql)
```

### DataFrame 操作

```python
from odps.df import DataFrame

# 创建 DataFrame
df = DataFrame(odps.get_table('table_name'))

# 过滤
df_filtered = df[df.ds == args['bizdate']]

# 聚合
result = df.groupby('category').agg(count=df.id.count())

# 写入表
result.persist('output_table', partition=f"ds={args['bizdate']}")
```

## Python 赋值节点

### 创建

新建 → 通用 → 赋值节点 → Python

### 参数传递

```python
# 最后一行 print 的值成为 outputs
result = "hello world"
print(result)
```

### 获取 API Token 示例

```python
import urllib.request
import json

app_id = "cli_xxx"
app_secret = "xxx"

data = json.dumps({
    "app_id": app_id,
    "app_secret": app_secret
}).encode('utf-8')

req = urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=data,
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read())
    token = result.get("tenant_access_token", "")

print(token)  # outputs
```

### 限制

| 限制 | 说明 |
|------|------|
| 运行环境 | Serverless，资源有限 |
| 第三方库 | 仅标准库可用 |
| 输出大小 | 最大 2MB |

## Notebook 节点

### 创建

新建 → Notebook

### 特点

| 特点 | 说明 |
|------|------|
| 交互式 | 支持分步执行 |
| 可视化 | 支持图表输出 |
| 环境隔离 | 个人开发环境 |
| 依赖管理 | 可安装 pip 包 |

### 使用场景

- 数据探索分析
- 模型开发调试
- 可视化报表

### 调度 Notebook

Notebook 可以配置为调度任务：

1. 保存 Notebook
2. 配置调度参数
3. 提交发布

## 常用代码片段

### HTTP 请求（标准库）

```python
import urllib.request
import json

def http_get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def http_post(url, data, headers=None):
    headers = headers or {"Content-Type": "application/json"}
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())
```

### 日期处理

```python
from datetime import datetime, timedelta

# 当前日期
today = datetime.now().strftime('%Y%m%d')

# 昨天
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

# 解析日期字符串
dt = datetime.strptime('20260107', '%Y%m%d')
```

### JSON 处理

```python
import json

# 解析
data = json.loads('{"key": "value"}')

# 序列化
json_str = json.dumps(data, ensure_ascii=False)

# 提取嵌套值
value = data.get('nested', {}).get('key', 'default')
```

### 环境变量

```python
import os

# 获取调度参数（PyODPS）
bizdate = args.get('bizdate')

# 获取环境变量
region = os.environ.get('SKYNET_REGION', 'cn-hangzhou')
```

## 调试技巧

### 本地调试 PyODPS

```python
from odps import ODPS

# 本地连接 MaxCompute
odps = ODPS(
    access_id='xxx',
    secret_access_key='xxx',
    project='project_name',
    endpoint='http://service.cn-hangzhou.maxcompute.aliyun.com/api'
)

# 模拟 args
args = {'bizdate': '20260107'}

# 执行代码
# ...
```

### 日志输出

```python
import sys

# 输出到 stderr（不影响 outputs）
print("Debug info", file=sys.stderr)

# 正常输出（赋值节点的 outputs）
print(result)
```
