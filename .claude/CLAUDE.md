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
│   ├── sql/         # SQL 脚本
│   │   ├── realtime/  # 实时链路 (dedup/ods/dwd/util)
│   │   └── offline/   # 离线链路 (dedup/ods/dim/dwd/dws/ads/util)
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
- **CRITICAL**: 请求聚光/蒲公英 API 前，先执行对应脚本获取 token：
  - 聚光: `bash dataworks_design/token/get_xhs_jg_token.sh`
  - 蒲公英: `bash dataworks_design/token/get_xhs_pgy_token.sh`
- 表结构变更需同步更新 `portal/models/tables.js`
- SQL 脚本按 `platform/sql/{realtime|offline}/{layer}/` 存放
- API 规范遵循 `xhs_{platform}_{module}_{action}.openapi.yml`
- **MaxCompute 建表必须添加 COMMENT**：表和字段都需要中文描述

## Output Format

### 全表查询规范

**默认查询最近 4 天**，按分层分组，ds 作为列头，查询全部 40 张表：

```
| 表 | 02.08 | 02.09 | 02.10 | 02.11 |
|-----|-------|-------|-------|-------|
| **ODS** | | | | |
| ods_xhs_post_note_report_di | 12,527 | 12,531 | 12,541 | - |
| ods_xhs_creative_report_hi | 11,102 | 699 | 12,250 | - |
| ... | | | | |
| **DWD** | | | | |
| dwd_xhs_note_di | 12,527 | 12,531 | 12,541 | - |
| ... | | | | |
| **DIM** | | | | |
| dim_xhs_note_df | 736 | - | 113 | - |
| ... | | | | |
| **BRG** | | | | |
| brg_xhs_note_project_df | 736 | - | 113 | - |
| **DWS** | | | | |
| dws_xhs_note_cum | 736 | - | 113 | - |
| ... | | | | |
| **ADS** | | | | |
| ads_xhs_note_bycontent_daily_agg | 1,472 | - | 226 | - |
| ... | | | | |
```

### 实时表查询规范

查询实时表时输出 8 张表数据量 + ETL 时间：

```
| Layer | creative | campaign | target | keyword |
|-------|----------|----------|--------|---------|
| ODS | 8,545 | 6,739 | 49,419 | 118,352 |
| DWD | 11,167 | 6,351 | 16,392 | 28,424 |
```

### 单日查询规范

表名 | ds | 数量 | 日同比

```
| 表名 | ds | 数量 | 日同比 |
|------|----------|------|--------|
| ods_xhs_creative_realtime_hi | 20260206 | 565 | +12.3% |
```

## Tables

全量查表时需查询以下 40 张表：

### ODS (15)

| 表名 | 描述 |
|------|------|
| ods_xhs_post_note_report_di | 投后数据笔记层每日报表 |
| ods_xhs_creative_report_hi | 创意层小时离线报表 |
| ods_xhs_campaign_report_hi | 聚光计划小时离线报表 |
| ods_xhs_creative_realtime_hi | 聚光创意实时报表 |
| ods_xhs_campaign_realtime_hi | 聚光计划实时报表 |
| ods_xhs_target_realtime_hi | 聚光定向实时报表 |
| ods_xhs_keyword_realtime_hi | 聚光关键词实时报表 |
| ods_xhs_keyword_report_di | 关键词日离线报表 |
| ods_xhs_searchword_report_di | 搜索词日离线报表 |
| ods_xhs_audience_report_di | 人群包日离线报表 |
| ods_xhs_account_flow_di | 投流账户每日流水 |
| ods_xhs_bus_data_df | 小红书业务数据日全量表 |
| ods_xhs_grass_ad_conversion_di | 种草联盟投流转化每日数据 |
| ods_xhs_grass_bycontent_conversion_di | 种草联盟转化每日数据-内容组 |
| ods_xhs_grass_bytask_conversion_di | 种草联盟转化每日数据-任务组 |

### DWD (14)

| 表名 | 描述 |
|------|------|
| dwd_xhs_note_di | 笔记层日增量表 |
| dwd_xhs_note_cum | 笔记层日累计表 |
| dwd_xhs_creative_hi | 创意层小时明细表 |
| dwd_xhs_campaign_hi | 计划层小时离线明细表 |
| dwd_xhs_creative_realtime_hi | 聚光创意实时明细表 |
| dwd_xhs_campaign_realtime_hi | 聚光计划实时明细表 |
| dwd_xhs_target_realtime_hi | 聚光定向实时明细表 |
| dwd_xhs_keyword_realtime_hi | 聚光关键词实时明细表 |
| dwd_xhs_keyword_report_di | 关键词日离线明细表 |
| dwd_xhs_searchword_report_di | 搜索词日离线明细表 |
| dwd_xhs_audience_report_di | 人群包日离线明细表 |
| dwd_xhs_account_flow_di | 投流账户消费明细表 |
| dwd_xhs_conversion_bycontent_di | 内容层转化效果每日明细表 |
| dwd_xhs_conversion_bytask_di | 任务层转化效果每日明细表 |

### DIM (4)

| 表名 | 描述 |
|------|------|
| dim_xhs_note_df | 小红书笔记维度表 |
| dim_xhs_project_df | 小红书项目维度表 |
| dim_xhs_task_group_df | 小红书任务组维度表 |
| dim_xhs_ad_product_df | 小红书投流产品维度表 |

### BRG (1)

| 表名 | 描述 |
|------|------|
| brg_xhs_note_project_df | 笔记与项目桥表 |

### DWS (3)

| 表名 | 描述 |
|------|------|
| dws_xhs_note_cum | 笔记累计宽表 |
| dws_xhs_creative_cum | 创意累计表 |
| dws_xhs_project_cum | 项目累计表 |

### ADS (3)

| 表名 | 描述 |
|------|------|
| ads_xhs_note_bycontent_daily_agg | 笔记维度内容种草日聚合表 |
| ads_xhs_project_bycontent_daily_agg | 项目维度内容种草日聚合表 |
| ads_xhs_content_theme_bycontent_daily_agg | 内容方向维度内容种草日聚合表 |

### 实时表查询

查询实时表时，需同时输出以下 8 张表：

| Layer | Tables |
|-------|--------|
| ODS | ods_xhs_creative_realtime_hi, ods_xhs_campaign_realtime_hi, ods_xhs_target_realtime_hi, ods_xhs_keyword_realtime_hi |
| DWD | dwd_xhs_creative_realtime_hi, dwd_xhs_campaign_realtime_hi, dwd_xhs_target_realtime_hi, dwd_xhs_keyword_realtime_hi |

## Skills

| Skill | Description |
|-------|-------------|
| `/invoke_dataworks_cli` | **必查** DataWorks CLI（任务、调度、数据集成） |
| `/operate_maxcompute` | MaxCompute 表操作（建表、SQL、分区） |
| `/operate_database` | PostgreSQL/MySQL 操作（连接、查询、DDL） |
| `/operate_feishu_bitable` | 飞书多维表格操作（读写记录） |
| `/name_dw_object` | 生成数仓对象命名（表、字段、指标） |
| `/backfill_creative` | 创意层补数据（API → ODS → DWD，10并发） |
| `/sync_conversion` | 种草联盟转化数据同步（PG → ODS → DWD，bycontent + bytask） |
| `/check_dim_push_status` | 查看 PG 维度表推送状态（T-1 分区数据量） |
| `/deploy_site` | 部署 `portal/` 前端到 GitHub Pages |
