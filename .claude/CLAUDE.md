# 小红书营销数据仓库

整合投流、种草、转化全链路数据的 DataWorks 数据仓库项目。

## Quick Reference

| Key | Value |
|-----|-------|
| Project | 伊阁数据仓库 |
| ProjectId | `530486` |
| MaxCompute | `df_ch_530486` |
| Region | `cn-hangzhou` |

## Directory Structure

```
dataworks/
├── design/          # 设计资产
│   ├── specs/xhs/   # API OpenAPI 规范
│   └── workflows/   # 工作流
├── platform/        # DataWorks 平台
│   ├── import/      # 导入 Excel
│   ├── scripts/     # 工具脚本
│   ├── sql/         # SQL 脚本 (ods/dwd/dws/ads)
│   └── sync/        # 同步任务
└── portal/          # 前端可视化工具
    └── models/      # 数据模型定义
        ├── layers.js    # 分层架构 (ODS/DWD/DIM/DWS/ADS)
        ├── tables.js    # 表字段定义
        ├── fields.js    # 字段标准
        ├── metrics.js   # 原子指标 + 复合指标
        └── codes.js     # 标准代码
```

## Architecture

### Layer

| Layer | Name | Description |
|-------|------|-------------|
| ODS | Operational Data Store | 原始数据层 |
| DWD | Data Warehouse Detail | 明细数据层 |
| DIM | Dimension | 维度数据层 |
| DWS | Data Warehouse Summary | 汇总数据层 |
| ADS | Application Data Store | 应用数据层 |

### Data Source

| Source | Description |
|--------|-------------|
| 聚光平台 | 广告投流效果数据 |
| 蒲公英平台 | 内容种草效果数据 |
| 种草联盟 | 站外转化归因数据 |
| 项目管理中心 | 预算、维度、成本等业务数据 |

### Data Flow

```
Excel (platform/import/) → DataWorks 平台 → MaxCompute
                                ↓
               JS (portal/models/) → 前端 (portal/)
```

## Naming Convention

### Table

```
{layer}_{domain}_{subject}_{strategy}
```

### Update Strategy

| Suffix | Meaning | Description |
|--------|---------|-------------|
| `_hi` | Hourly Increment | 每小时增量 |
| `_df` | Daily Full | 每日全量 |
| `_di` | Daily Increment | 每日增量 |
| `_agg` | Aggregation | 汇总聚合 |

### Required Fields

每张表必须包含以下字段：

| Field | Type | Description | Position |
|-------|------|-------------|----------|
| `ds` | STRING | 分区日期 (YYYYMMDD) | 分区键 |
| `dt` | STRING | 数据时间段 | 业务字段后 |
| `etl_time` | DATETIME | ETL 处理时间 | 表末尾 |

## Environment

凭证存储在 `.env` 文件，执行脚本前加载：

```bash
export $(cat .env | xargs) && python3 script.py
```

| Variable | Description |
|----------|-------------|
| `FEISHU_APP_ID` | 飞书应用 ID |
| `FEISHU_APP_SECRET` | 飞书应用密钥 |
| `ALIYUN_ACCESS_KEY_ID` | 阿里云 AccessKey ID |
| `ALIYUN_ACCESS_KEY_SECRET` | 阿里云 AccessKey Secret |
| `DB_HOST/PORT/NAME/USER/PASSWORD` | PostgreSQL 连接信息 |

## Constraints

- **CRITICAL**: 查表、查数据量等数据查询操作，默认使用 `/operate_maxcompute` 查询 MaxCompute
- **CRITICAL**: 执行 DataWorks 操作前，必须先调用 `/invoke_dataworks_cli`
- 表结构变更需同步更新 `portal/models/tables.js`
- SQL 脚本按分层存放于 `platform/sql/{layer}/`
- API 规范遵循 `xhs_{platform}_{module}_{action}.openapi.yml`
- **MaxCompute 建表必须添加 COMMENT**：表和字段都需要中文描述

## Skills

| Skill | Description |
|-------|-------------|
| `/invoke_dataworks_cli` | **必查** DataWorks CLI（任务、调度、数据集成） |
| `/operate_maxcompute` | MaxCompute 表操作（建表、SQL、分区） |
| `/operate_database` | PostgreSQL/MySQL 操作（连接、查询、DDL） |
| `/operate_feishu_bitable` | 飞书多维表格操作（读写记录） |
| `/name_dw_object` | 生成数仓对象命名（表、字段、指标） |
| `/deploy_site` | 部署 `portal/` 前端到 GitHub Pages |
