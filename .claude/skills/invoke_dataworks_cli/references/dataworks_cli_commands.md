# DataWorks CLI Commands Reference

阿里云 DataWorks CLI 常用命令参考。

## 项目管理 (Project Management)

### 列出项目

```bash
aliyun dataworks-public ListProjects --region cn-hangzhou
```

### 获取项目详情

```bash
aliyun dataworks-public GetProject --ProjectId <project_id> --region cn-hangzhou
```

### 创建项目

```bash
aliyun dataworks-public CreateProject \
  --ProjectName "MyProject" \
  --ProjectDescription "Project description" \
  --region cn-hangzhou
```

## 任务管理 (Node Management)

### 列出任务

```bash
aliyun dataworks-public ListNodes \
  --ProjectId <project_id> \
  --PageNumber 1 \
  --PageSize 20 \
  --region cn-hangzhou
```

### 获取任务详情

```bash
aliyun dataworks-public GetNode --NodeId <node_id> --region cn-hangzhou
```

### 运行任务

```bash
aliyun dataworks-public RunNode \
  --NodeId <node_id> \
  --BizDate "2025-12-31" \
  --region cn-hangzhou
```

### 停止任务

```bash
aliyun dataworks-public StopNode --NodeId <node_id> --region cn-hangzhou
```

## 任务实例管理 (Instance Management)

### 查询任务实例

```bash
aliyun dataworks-public ListNodeInstances \
  --ProjectId <project_id> \
  --NodeId <node_id> \
  --PageNumber 1 \
  --PageSize 20 \
  --region cn-hangzhou
```

### 获取任务实例详情

```bash
aliyun dataworks-public GetNodeInstance \
  --NodeInstanceId <instance_id> \
  --region cn-hangzhou
```

### 重跑任务实例

```bash
aliyun dataworks-public RerunNodeInstance \
  --NodeInstanceId <instance_id> \
  --region cn-hangzhou
```

## 数据集成 (Data Integration)

### 列出数据源

```bash
aliyun dataworks-public ListDataSources \
  --ProjectId <project_id> \
  --region cn-hangzhou
```

### 获取数据源详情

```bash
aliyun dataworks-public GetDataSource \
  --DataSourceId <datasource_id> \
  --region cn-hangzhou
```

### 测试数据源连接

```bash
aliyun dataworks-public TestDataSource \
  --DataSourceId <datasource_id> \
  --region cn-hangzhou
```

## 资源管理 (Resource Management)

### 列出资源

```bash
aliyun dataworks-public ListResources \
  --ProjectId <project_id> \
  --region cn-hangzhou
```

### 上传资源

```bash
aliyun dataworks-public CreateResource \
  --ProjectId <project_id> \
  --ResourceName "my_resource.jar" \
  --ResourceType "jar" \
  --FilePath "/path/to/resource.jar" \
  --region cn-hangzhou
```

### 删除资源

```bash
aliyun dataworks-public DeleteResource \
  --ResourceId <resource_id> \
  --region cn-hangzhou
```

## 调度配置 (Scheduler)

### 获取调度配置

```bash
aliyun dataworks-public GetScheduler --NodeId <node_id> --region cn-hangzhou
```

### 更新调度配置

```bash
aliyun dataworks-public UpdateScheduler \
  --NodeId <node_id> \
  --CronExpression "0 0 2 * * ?" \
  --SchedulerType "cron" \
  --region cn-hangzhou
```

## 通用参数 (Common Parameters)

| 参数 | 说明 | 示例 |
|------|------|------|
| `--region` | 地域 | `cn-hangzhou`, `cn-beijing` |
| `--ProjectId` | 项目ID | `123456` |
| `--NodeId` | 任务ID | `789012` |
| `--PageNumber` | 页码 | `1` |
| `--PageSize` | 每页数量 | `20` (最大100) |
| `--output` | 输出格式 | `json`, `table` |

## 输出格式 (Output Format)

### JSON格式

```bash
aliyun dataworks-public ListProjects --region cn-hangzhou --output json
```

### 表格格式

```bash
aliyun dataworks-public ListProjects --region cn-hangzhou --output table
```

## 错误码 (Error Codes)

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `InvalidAccessKeyId.NotFound` | AccessKey不存在 | 检查 `.env` 凭证 |
| `Throttling` | API限流 | 等待后重试 |
| `InvalidParameter` | 参数错误 | 检查参数格式 |
| `ProjectNotFound` | 项目不存在 | 确认 ProjectId |
| `NodeNotFound` | 任务不存在 | 确认 NodeId |

## 最佳实践 (Best Practices)

1. **分页查询**: 使用 `PageNumber` 和 `PageSize` 避免一次性加载大量数据
2. **指定地域**: 始终使用 `--region` 参数提高性能
3. **JSON输出**: 用于程序化处理，解析更方便
4. **错误处理**: 检查返回码，处理异常情况

## 安装指南 (Installation)

### macOS

```bash
brew install aliyun-cli
```

### Linux

```bash
wget https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz
tar -xzf aliyun-cli-linux-latest-amd64.tgz
sudo mv aliyun /usr/local/bin/
```

### Windows

下载安装包：https://aliyuncli.alicdn.com/aliyun-cli-windows-latest-amd64.zip

## 认证配置 (Authentication)

### 方式1: 环境变量 (推荐)

```bash
export ALIBABA_CLOUD_ACCESS_KEY_ID=your_key_id
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=your_key_secret
```

### 方式2: 配置文件

```bash
aliyun configure
```

## 参考链接 (References)

- [Aliyun CLI官方文档](https://www.alibabacloud.com/help/en/alibaba-cloud-cli)
- [DataWorks API文档](https://www.alibabacloud.com/help/en/dataworks/developer-reference/api-overview)
- [错误码查询](https://error-center.alibabacloud.com/status/product/dataworks-public)
