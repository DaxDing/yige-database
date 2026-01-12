# DataWorks Shell 节点开发指南

## 节点类型对比

| 类型 | 创建路径 | outputs | 用途 |
|------|---------|---------|------|
| **Shell 节点** | 新建 → 通用 → Shell | 需手动配置 | 纯脚本执行 |
| **赋值节点** | 新建 → 通用 → 赋值节点 → Shell | 自动捕获 | 脚本 + 参数传递 |

## 执行环境

### 运行时环境

| 项目 | 规格 |
|------|------|
| Shell | `/bin/sh` (POSIX)，**非 bash** |
| 执行方式 | `/bin/sh script.sql 参数1 参数2` |
| 工作目录 | 临时目录，每次不同 |

### 可用命令

| 命令 | 状态 | 备注 |
|------|------|------|
| `curl` | ✅ | HTTP 请求 |
| `wget` | ✅ | 下载文件 |
| `grep` | ✅ | 文本搜索 |
| `sed` | ✅ | 文本替换 |
| `awk` | ✅ | 文本处理 |
| `jq` | ❌ | 需用 grep/sed 替代 |
| `python` | ⚠️ | 部分资源组可用 |

### POSIX 兼容语法

```sh
# ❌ Bash 特有语法
#!/bin/bash
set -euo pipefail
if [[ -z "${VAR:-}" ]]; then
[[ $a == $b ]]
${array[@]}

# ✅ POSIX 兼容语法
# 无 shebang 或只用注释
set -e
if [ -z "${VAR}" ]; then
[ "$a" = "$b" ]
# 不支持数组
```

## 参数传递

### 输入参数

DataWorks 传递参数格式：`KEY=VALUE`

```sh
# DataWorks 执行: /bin/sh script.sql KEY1=value1 KEY2=value2
# $1 = "KEY1=value1"
# $2 = "KEY2=value2"

# 解析为环境变量
eval "$1"
eval "$2"

# 使用
echo $KEY1  # value1
echo $KEY2  # value2
```

### 输出参数（赋值节点）

赋值节点自动捕获**最后一行 `echo`** 作为 `outputs`：

```sh
# 中间输出（不会被捕获）
echo "Processing..."

# 最后一行（自动成为 outputs）
echo "$result"
```

**多值输出**：用逗号分隔，下游用 `${param[0]}`、`${param[1]}` 访问

```sh
echo "value1,value2,value3"
```

## JSON 解析

### 无 jq 环境的替代方案

```sh
response='{"code":0,"data":{"token":"abc123","expire":7200}}'

# 提取简单字段
code=$(echo "$response" | grep -o '"code":[0-9]*' | grep -o '[0-9]*')
token=$(echo "$response" | grep -o '"token":"[^"]*"' | sed 's/"token":"//;s/"$//')

# 提取嵌套字段
expire=$(echo "$response" | grep -o '"expire":[0-9]*' | grep -o '[0-9]*')

# 检查 code
if [ "$code" != "0" ]; then
    echo "Error: $response" >&2
    exit 1
fi

echo "$token"
```

### 常用 grep/sed 模式

| 目标 | 命令 |
|------|------|
| 提取字符串值 | `grep -o '"key":"[^"]*"' \| sed 's/"key":"//;s/"$//'` |
| 提取数字值 | `grep -o '"key":[0-9]*' \| grep -o '[0-9]*'` |
| 提取布尔值 | `grep -o '"key":\(true\|false\)' \| sed 's/"key"://'` |
| 检查字段存在 | `echo "$json" \| grep -q '"key"'` |

## 错误处理

```sh
# 设置错误退出
set -e

# 检查必需参数
if [ -z "${APP_ID}" ]; then
    echo "Error: APP_ID is required" >&2
    exit 1
fi

# HTTP 请求错误处理
response=$(curl -s -w "\n%{http_code}" "$URL")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" != "200" ]; then
    echo "HTTP Error: $http_code" >&2
    echo "Response: $body" >&2
    exit 1
fi
```

## 完整模板

### API Token 获取（赋值节点）

```sh
# 飞书 Token 获取
# 参数: $1=FEISHU_APP_ID=xxx  $2=FEISHU_APP_SECRET=xxx

set -e

eval "$1"
eval "$2"

if [ -z "${FEISHU_APP_ID}" ] || [ -z "${FEISHU_APP_SECRET}" ]; then
    echo "Error: Missing credentials" >&2
    exit 1
fi

response=$(curl -s \
    -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d "{\"app_id\":\"${FEISHU_APP_ID}\",\"app_secret\":\"${FEISHU_APP_SECRET}\"}")

code=$(echo "$response" | grep -o '"code":[0-9]*' | grep -o '[0-9]*')

if [ "$code" != "0" ]; then
    echo "API Error: $response" >&2
    exit 1
fi

token=$(echo "$response" | grep -o '"tenant_access_token":"[^"]*"' | sed 's/"tenant_access_token":"//;s/"$//')

echo "$token"
```

### 数据处理（普通 Shell 节点）

```sh
# 参数: $1=INPUT_FILE=xxx  $2=OUTPUT_PATH=xxx

eval "$1"
eval "$2"

# 下载文件
curl -s -o /tmp/input.json "$INPUT_FILE"

# 处理数据
cat /tmp/input.json | grep -v "^#" | sed 's/old/new/g' > /tmp/output.json

# 上传结果
curl -s -X PUT -T /tmp/output.json "$OUTPUT_PATH"

echo "Done"
```

## 调试技巧

### 本地测试

```bash
# 模拟 DataWorks 执行
/bin/sh your_script.sh "KEY1=value1" "KEY2=value2"
```

### 日志输出

```sh
# 标准输出 → 日志
echo "Info: Processing step 1"

# 标准错误 → 错误日志（不影响 outputs）
echo "Debug: variable=$var" >&2
```

### 查看完整响应

```sh
# 临时调试：输出完整响应
echo "DEBUG Response: $response" >&2
```
