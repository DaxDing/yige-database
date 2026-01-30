# MaxCompute 表清单

项目：`df_ch_530486` | 区域：`cn-hangzhou` | 共 25 张表

## ODS 原始数据层（7 张）

| 表名 | 说明 | 更新策略 |
|------|------|----------|
| `ods_xhs_account_flow_df` | 投流账户每日流水 | 日全量 |
| `ods_xhs_bus_data_df` | 小红书业务数据日全量表 | 日全量 |
| `ods_xhs_creative_report_hi` | 创意层小时离线报表 | 小时增量 |
| `ods_xhs_grass_ad_conversion_di` | 种草联盟投流转化每日数据 | 日增量 |
| `ods_xhs_grass_bycontent_conversion_di` | 种草联盟转化每日数据-内容组 | 日增量 |
| `ods_xhs_grass_bytask_conversion_di` | 种草联盟转化每日数据-任务组 | 日增量 |
| `ods_xhs_post_note_report_di` | 投后数据笔记层每日报表 | 日增量 |

## DWD 明细数据层（6 张）

| 表名 | 说明 | 更新策略 |
|------|------|----------|
| `dwd_xhs_account_flow_di` | 投流账户消费明细表 | 日增量 |
| `dwd_xhs_conversion_bycontent_di` | 内容层转化效果每日明细表 | 日增量 |
| `dwd_xhs_conversion_bytask_di` | 任务层转化效果每日明细表 | 日增量 |
| `dwd_xhs_creative_hi` | 创意层小时明细表 | 小时增量 |
| `dwd_xhs_note_cum` | 笔记层日累计表 | 累计值 |
| `dwd_xhs_note_di` | 笔记层日增量表 | 日增量 |

## DIM 维度数据层（4 张）

| 表名 | 说明 | 更新策略 |
|------|------|----------|
| `dim_xhs_ad_product_df` | 小红书投流产品维度表 | 日全量 |
| `dim_xhs_note_df` | 小红书笔记维度表 | 日全量 |
| `dim_xhs_project_df` | 小红书项目维度表 | 日全量 |
| `dim_xhs_task_group_df` | 小红书任务组维度表 | 日全量 |

## BRG 桥接层（1 张）

| 表名 | 说明 | 更新策略 |
|------|------|----------|
| `brg_xhs_note_project_df` | 笔记与项目桥表 | 日全量 |

## DWS 汇总数据层（4 张）

| 表名 | 说明 | 更新策略 |
|------|------|----------|
| `dws_xhs_content_theme_cum` | 内容主题累计表 | 累计值 |
| `dws_xhs_creative_cum` | 创意累计表 | 累计值 |
| `dws_xhs_note_cum` | 笔记累计宽表 | 累计值 |
| `dws_xhs_project_cum` | 项目累计表 | 累计值 |

## ADS 应用数据层（3 张）

| 表名 | 说明 | 更新策略 |
|------|------|----------|
| `ads_xhs_content_theme_bycontent_daily_agg` | 内容方向维度内容种草日聚合表 | 聚合 |
| `ads_xhs_note_bycontent_daily_agg` | 笔记维度内容种草日聚合表 | 聚合 |
| `ads_xhs_project_bycontent_daily_agg` | 项目维度内容种草日聚合表 | 聚合 |
