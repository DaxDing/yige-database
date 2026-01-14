# DataWorks 节点类型

## 节点分类

### 通用节点

| 节点 | 用途 | 参数传递 |
|------|------|---------|
| **Shell** | 执行 Shell 脚本 | 手动配置 |
| **赋值节点** | 脚本 + 参数传递 | 自动 outputs |
| **参数节点** | 定义工作流参数 | - |
| **虚拟节点** | 依赖占位 | - |
| **归并节点** | 多分支合并 | - |
| **分支节点** | 条件分支 | - |
| **for-each** | 循环执行 | - |

### 数据开发节点

| 节点 | 用途 | 数据源 |
|------|------|--------|
| **ODPS SQL** | MaxCompute SQL | MaxCompute |
| **ODPS Spark** | Spark 任务 | MaxCompute |
| **ODPS MR** | MapReduce | MaxCompute |
| **EMR Hive** | Hive SQL | EMR |
| **EMR Spark** | Spark SQL | EMR |
| **Hologres** | Hologres SQL | Hologres |
| **AnalyticDB** | ADB SQL | AnalyticDB |
| **ClickHouse** | ClickHouse SQL | ClickHouse |

### 数据集成节点

| 节点 | 用途 |
|------|------|
| **数据同步** | 离线数据同步 |
| **实时同步** | CDC 实时同步 |

## 节点详解

### Shell 节点

**创建**：新建 → 通用 → Shell

**特点**：
- 执行环境：`/bin/sh` (POSIX)
- 无自动参数传递
- 需手动配置输出参数

**使用场景**：
- 纯脚本执行
- 文件处理
- 系统命令调用

详见：[shell_node.md](./shell_node.md)

### 赋值节点

**创建**：新建 → 通用 → 赋值节点 → 选择语言

**支持语言**：
- Shell
- ODPS SQL
- Python (部分资源组)

**特点**：
- 最后一行输出自动赋值给 `outputs`
- 下游可直接引用

**使用场景**：
- 获取 Token
- 查询单值结果
- 节点间传参

详见：[context_parameters.md](./context_parameters.md)

### 参数节点

**创建**：新建 → 通用 → 参数节点

**用途**：
- 定义工作流级参数
- 集中管理配置
- 支持加密参数

**配置**：
```
key1=value1
key2=value2
```

**下游引用**：`${key1}`

### 虚拟节点

**创建**：新建 → 通用 → 虚拟节点

**用途**：
- 作为依赖锚点
- 组织工作流结构
- 不执行任何操作

### 分支节点

**创建**：新建 → 通用 → 分支节点

**配置**：
```python
# 条件表达式
if ${status} == "success":
    return "branch_a"
else:
    return "branch_b"
```

**下游配置**：
- 每个分支对应不同的下游节点
- 根据条件决定执行路径

### for-each 节点

**创建**：新建 → 通用 → for-each 节点

**用途**：循环遍历赋值节点的结果集

**配置**：
1. 上游必须是赋值节点
2. 赋值节点输出逗号分隔的值
3. for-each 节点内部用 `${dag.loopDataArray}` 获取当前值

### 数据同步节点

**创建**：新建 → 数据集成 → 离线同步

**组成**：
- Reader：数据源读取
- Writer：目标写入
- Transformer：数据转换（可选）

详见：[data_integration.md](./data_integration.md)

## 节点配置通用项

### 调度参数

| 参数类型 | 格式 | 示例 |
|---------|------|------|
| 系统参数 | `$bizdate` | 业务日期 |
| 自定义常量 | `key=value` | `env=prod` |
| 自定义变量 | `key=$[yyyymmdd]` | 动态日期 |

### 系统变量

| 变量 | 含义 | 格式 |
|------|------|------|
| `$bizdate` | 业务日期 | yyyymmdd |
| `$cyctime` | 定时时间 | yyyymmddhh24miss |
| `$gmtdate` | 当前日期 | yyyymmdd |
| `${bdp.system.bizdate}` | 同 $bizdate | yyyymmdd |

### 调度依赖

| 依赖类型 | 说明 |
|---------|------|
| 同周期依赖 | 等待上游同周期实例完成 |
| 跨周期依赖 | 等待上游上一周期实例完成 |
| 自依赖 | 等待自己上一周期实例完成 |

详见：[scheduling.md](./scheduling.md)
