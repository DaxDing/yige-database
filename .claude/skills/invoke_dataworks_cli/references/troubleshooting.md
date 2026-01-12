# DataWorks 故障排查

## Shell 节点错误

### command not found

**错误示例**：
```
/path/main.sql: line 1: xxx: command not found
```

**原因与解决**：

| 原因 | 解决方案 |
|------|---------|
| 使用了 `#!/bin/bash` | 删除 shebang，DataWorks 用 `/bin/sh` 执行 |
| 使用了 bash 特有语法 | 改用 POSIX 兼容语法 |
| 命令不存在（如 jq） | 用 grep/sed 替代 |

**POSIX 兼容检查清单**：

| 检查项 | Bash | POSIX |
|--------|------|-------|
| 条件判断 | `[[ ]]` | `[ ]` |
| 字符串比较 | `==` | `=` |
| 默认值 | `${var:-default}` | 用 `if` 判断 |
| 数组 | `${arr[@]}` | 不支持 |
| pipefail | `set -o pipefail` | 不支持 |

### jq: not found

**错误**：
```
jq: command not found
```

**解决**：用 grep/sed 替代 jq

```sh
# jq 写法
token=$(echo "$json" | jq -r '.token')

# grep/sed 替代
token=$(echo "$json" | grep -o '"token":"[^"]*"' | sed 's/"token":"//;s/"$//')
```

### 参数解析失败

**错误**：
```
KEY=VALUE: command not found
```

**原因**：DataWorks 传递 `KEY=VALUE` 格式参数，需要 `eval` 解析

**解决**：
```sh
# 正确写法
eval "$1"
eval "$2"

# 错误写法
echo $1  # 输出整个 "KEY=VALUE" 字符串
```

## 参数传递错误

### ${outputs.xxx} 未替换

**现象**：下游节点收到字面字符串 `${outputs.token}`

**原因**：上游用了普通 Shell 节点，不是赋值节点

**解决**：
1. 删除原 Shell 节点
2. 新建「赋值节点」（Shell 语言）
3. 最后一行 `echo` 输出值

### 下游收不到参数

**检查清单**：

| 检查项 | 正确配置 |
|--------|---------|
| 上游节点类型 | 赋值节点 |
| 上游最后一行 | `echo "$value"` |
| DAG 依赖 | 有连线 |
| 下游输入参数 | 参数值选 `outputs` |
| 运行方式 | 运行整个工作流 |

**常见错误**：

| 错误配置 | 正确配置 |
|---------|---------|
| 参数值: `token` | 参数值: `outputs` |
| 参数值: `${outputs.token}` | 参数值: `outputs` |
| 单独运行下游 | 运行工作流或冒烟测试 |

### 参数为空

**可能原因**：

1. 上游执行失败，没有输出
2. 上游 `echo` 不是最后一行
3. 上游输出了空字符串

**调试方法**：

```sh
# 在上游节点添加调试输出
echo "DEBUG: token=$token" >&2  # 输出到 stderr，不影响 outputs
echo "$token"  # 这是 outputs
```

## API 认证错误

### Invalid access token (99991663)

**错误**：
```json
{"code": 99991663, "msg": "Invalid access token for authorization"}
```

**可能原因**：

| 原因 | 解决 |
|------|------|
| Token 未传递 | 检查上游赋值节点配置 |
| Token 过期 | Token 有效期 2 小时，确保实时获取 |
| Token 类型错误 | 确认使用 tenant_access_token |
| 应用无权限 | 开放平台添加 API 权限 |
| 文档未授权 | 将应用添加为文档协作者 |

### 飞书权限检查

1. **应用权限**：飞书开放平台 → 应用 → 权限管理
   - `bitable:app` - 多维表格读写
   - `bitable:app:readonly` - 多维表格只读

2. **文档权限**：打开多维表格 → 邀请应用机器人

### HTTP 错误

| 状态码 | 原因 | 解决 |
|--------|------|------|
| 400 | 请求参数错误 | 检查 Body 格式 |
| 401 | 认证失败 | 检查 Token |
| 403 | 权限不足 | 检查应用权限 |
| 404 | 资源不存在 | 检查 URL |
| 429 | 请求过频 | 添加重试逻辑 |
| 500 | 服务器错误 | 稍后重试 |

## 数据集成错误

### 连接失败

**错误**：
```
Connection refused
```

**检查**：
1. 数据源配置是否正确
2. 网络是否连通（VPC 配置）
3. IP 白名单是否添加
4. 端口是否开放

### 字段不匹配

**错误**：
```
column not found: xxx
```

**解决**：
1. 检查 Reader column 配置
2. 检查 Writer column 配置
3. 确保源表和目标表字段对应

### 数据类型错误

**错误**：
```
Data type mismatch
```

**解决**：
1. 检查字段类型映射
2. 添加 Transformer 转换类型
3. 使用 `cast` 函数

## 调度错误

### 任务未执行

**可能原因**：

| 原因 | 解决 |
|------|------|
| 未提交发布 | 提交节点到调度系统 |
| 依赖未完成 | 检查上游任务状态 |
| 未到调度时间 | 查看调度配置 |
| 资源组不可用 | 检查资源组状态 |

### 任务卡住

**状态**：长时间「等待资源」

**解决**：
1. 检查资源组是否有可用资源
2. 降低并发任务数
3. 使用其他资源组

### 补数据失败

**常见问题**：

| 问题 | 解决 |
|------|------|
| 上游数据不存在 | 先补上游数据 |
| 并行度过高 | 降低并行度 |
| 资源不足 | 分批补数据 |

## 日志分析

### 查看日志位置

运维中心 → 周期实例 → 点击实例 → 运行日志

### 关键日志信息

| 日志关键词 | 含义 |
|-----------|------|
| `Full Command` | 实际执行的命令 |
| `variable replacement` | 参数替换详情 |
| `Exit code` | 退出码 |
| `ERROR` | 错误信息 |
| `SKYNET_TASK_INPUT` | 节点输入参数 |

### 日志分析示例

```
# 查看参数是否正确替换
INFO variable replacement details: access_token=t-xxx

# 查看执行命令
INFO Full Command: /bin/sh main.sql KEY=VALUE

# 查看错误原因
ERROR code:99991663,msg:Invalid access token
```

## 调试技巧

### 本地测试

```bash
# 模拟 DataWorks 执行环境
/bin/sh your_script.sh "PARAM1=value1" "PARAM2=value2"
```

### 添加调试日志

```sh
# 输出到 stderr，不影响 outputs
echo "DEBUG: var=$var" >&2

# 正常 outputs
echo "$result"
```

### 分步验证

1. 先单独运行上游赋值节点
2. 查看日志确认 outputs 值
3. 再运行下游节点
4. 查看参数是否正确传递

### API 调试

```bash
# 先用 curl 测试 API
curl -X POST "https://api.example.com/endpoint" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```
