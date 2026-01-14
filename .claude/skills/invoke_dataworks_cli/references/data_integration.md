# DataWorks 数据集成

## 概述

数据集成用于在不同数据源之间同步数据，支持：
- 离线批量同步
- 实时增量同步

## 数据同步节点

### 创建

新建 → 数据集成 → 离线同步

### 组成部分

```
┌─────────────────────────────────────────────────────────┐
│                    数据同步任务                           │
│  ┌─────────┐    ┌─────────────┐    ┌─────────┐         │
│  │ Reader  │ ─→ │ Transformer │ ─→ │ Writer  │         │
│  │ (读取)   │    │ (转换,可选)  │    │ (写入)   │         │
│  └─────────┘    └─────────────┘    └─────────┘         │
└─────────────────────────────────────────────────────────┘
```

## Reader 类型

### RestAPI Reader

从 REST API 读取数据。

**配置项**：

| 配置 | 说明 | 示例 |
|------|------|------|
| `url` | API 地址 | `https://api.example.com/data` |
| `method` | 请求方法 | GET/POST |
| `customHeader` | 自定义请求头 | `{"Authorization": "Bearer ${token}"}` |
| `parameters` | 请求参数/Body | JSON 格式 |
| `dataPath` | 数据路径 | `data.items` |
| `column` | 字段映射 | 见下文 |

**customHeader 配置**：

```json
{
  "Authorization": "Bearer ${access_token}",
  "Content-Type": "application/json; charset=utf-8"
}
```

**parameters 配置（POST Body）**：

```json
{
  "page_size": 100,
  "app_token": "${app_token}",
  "table_id": "${table_id}"
}
```

**dataPath 说明**：

API 返回：
```json
{
  "code": 0,
  "data": {
    "items": [
      {"id": 1, "name": "a"},
      {"id": 2, "name": "b"}
    ]
  }
}
```

配置 `dataPath: data.items` 将提取 items 数组。

**column 配置**：

```json
[
  {"name": ".", "type": "string"}  // 整行作为字符串
]

// 或提取特定字段
[
  {"name": "id", "type": "long"},
  {"name": "name", "type": "string"}
]
```

### MySQL Reader

```json
{
  "datasource": "mysql_source",
  "table": ["table_name"],
  "column": ["id", "name", "created_at"],
  "where": "created_at > '${bizdate}'"
}
```

### PostgreSQL Reader

```json
{
  "datasource": "pg_source",
  "table": ["public.table_name"],
  "column": ["*"],
  "splitPk": "id"
}
```

## Writer 类型

### PostgreSQL Writer

**配置项**：

| 配置 | 说明 |
|------|------|
| `datasource` | 数据源名称 |
| `table` | 目标表 |
| `column` | 写入字段 |
| `preSql` | 写入前执行 |
| `postSql` | 写入后执行 |
| `writeMode` | 写入模式 |

**writeMode 选项**：

| 模式 | 说明 |
|------|------|
| `insert` | 直接插入 |
| `copy` | COPY 批量写入（推荐） |
| `update` | 更新已有记录 |
| `replace` | 替换已有记录 |

**完整配置示例**：

```json
{
  "datasource": "pg_target",
  "table": "public.target_table",
  "column": ["id", "name", "raw_data", "ds"],
  "preSql": [
    "TRUNCATE TABLE public.target_table"
  ],
  "postSql": [
    "UPDATE public.target_table SET ds = '${bizdate}'"
  ],
  "writeMode": "copy"
}
```

### MySQL Writer

```json
{
  "datasource": "mysql_target",
  "table": "target_table",
  "column": ["id", "name"],
  "writeMode": "replace",
  "batchSize": 1024
}
```

### MaxCompute Writer

```json
{
  "datasource": "odps_target",
  "table": "target_table",
  "partition": "ds=${bizdate}",
  "truncate": true,
  "column": ["*"]
}
```

## 参数引用

### 调度参数

在数据同步任务中可以引用调度参数：

| 参数类型 | 引用格式 | 示例 |
|---------|---------|------|
| 系统参数 | `${bizdate}` | 业务日期 |
| 自定义参数 | `${param_name}` | 自定义值 |
| 节点输入参数 | `${input_param}` | 上游传递 |

### 引用位置

```
URL:        https://api.example.com/data?date=${bizdate}
Header:     {"Authorization": "Bearer ${access_token}"}
Body:       {"app_token": "${app_token}"}
preSql:     DELETE FROM table WHERE ds = '${bizdate}'
postSql:    UPDATE table SET ds = '${bizdate}'
where:      created_at >= '${bizdate}'
partition:  ds=${bizdate}
```

## 脚本模式

### 切换到脚本模式

点击「转换脚本」可以查看/编辑完整 JSON 配置。

### 完整脚本示例

```json
{
  "job": {
    "content": [
      {
        "reader": {
          "name": "restapireader",
          "parameter": {
            "url": "https://open.feishu.cn/open-apis/bitable/v1/apps/${app_token}/tables/${table_id}/records/search",
            "method": "POST",
            "customHeader": {
              "Authorization": "Bearer ${access_token}",
              "Content-Type": "application/json; charset=utf-8"
            },
            "parameters": {
              "page_size": 100
            },
            "dataPath": "data.items",
            "column": [
              {"name": ".", "type": "string"}
            ]
          }
        },
        "writer": {
          "name": "postgresqlwriter",
          "parameter": {
            "datasource": "pg_target",
            "table": "public.raw_data",
            "column": ["raw_data"],
            "preSql": ["TRUNCATE TABLE public.raw_data"],
            "postSql": ["UPDATE public.raw_data SET ds = '${bizdate}'"],
            "writeMode": "copy"
          }
        }
      }
    ],
    "setting": {
      "speed": {
        "channel": 2,
        "throttle": false
      },
      "errorLimit": {
        "record": 0
      }
    }
  }
}
```

## 错误处理

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `http_request_error` | API 请求失败 | 检查 URL、Header、认证 |
| `Invalid access token` | Token 无效 | 检查上游赋值节点、权限 |
| `Connection refused` | 网络不通 | 检查数据源配置、白名单 |
| `column not found` | 字段不匹配 | 检查 column 配置 |
| `permission denied` | 权限不足 | 检查数据库用户权限 |

### 调试技巧

1. **查看详细日志**：运维中心 → 任务实例 → 查看日志
2. **检查参数替换**：日志中搜索 `variable replacement`
3. **验证 API**：先用 curl 测试 API 是否正常
4. **检查数据源**：管理中心 → 数据源 → 测试连接

## 性能优化

| 配置 | 说明 | 建议 |
|------|------|------|
| `channel` | 并发数 | 2-5，根据数据源承受能力 |
| `batchSize` | 批量写入大小 | 1024-4096 |
| `throttle` | 限速 | 大数据量时开启 |
| `splitPk` | 分片键 | 大表读取时配置 |
