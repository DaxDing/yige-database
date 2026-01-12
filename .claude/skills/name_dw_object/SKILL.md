---
name: name_dw_object
description: Generates standardized data warehouse object names. Use when naming tables, fields, or metrics in DataWorks.
allowed-tools: ["Read"]
---

# Data Warehouse Naming

Generate compliant names for tables, fields, and metrics following project standards.

## Table Naming

### Format
```
{layer}_{domain}_{subject}_{strategy}
```

### Layers

| Prefix | Layer | Purpose |
|--------|-------|---------|
| `ods_` | ODS | Raw data from API |
| `dwd_` | DWD | Cleaned detail facts |
| `dim_` | DIM | Dimension attributes |
| `dws_` | DWS | Aggregated summaries |
| `ads_` | ADS | Application reports |
| `brg_` | Bridge | Many-to-many relations |

### Domain
- `xhs` - 小红书 (Xiaohongshu)

### Strategy Suffix

| Suffix | Meaning | When |
|--------|---------|------|
| `_hi` | Hourly Increment | Hourly append |
| `_df` | Daily Full | Daily overwrite |
| `_di` | Daily Increment | Daily append |
| `_agg` | Aggregation | Summary tables |

### Examples
```
ods_xhs_creative_report_hi    # ODS hourly creative report
dwd_xhs_creative_hourly_di    # DWD hourly creative detail
dim_xhs_advertiser_df         # DIM advertiser dimension
dws_xhs_campaign_daily_agg    # DWS daily campaign summary
ads_xhs_roi_analysis_df       # ADS ROI analysis report
brg_xhs_note_project_df       # Bridge note-project relation
```

## Field Naming

### Format
```
{scope}_{object}_{attribute}
```

### Common Patterns

| Pattern | Example | Usage |
|---------|---------|-------|
| `{entity}_id` | `advertiser_id` | Primary/foreign key |
| `{entity}_name` | `campaign_name` | Display name |
| `{metric}_cnt` | `click_cnt` | Count metric |
| `{metric}_amt` | `order_amt` | Amount metric |
| `stat_date` | - | Statistics date |
| `stat_hour` | - | Statistics hour |
| `etl_time` | - | ETL timestamp |
| `ds` | - | Partition date |

### Reserved Fields

| Field | Type | Key | Description |
|-------|------|-----|-------------|
| `ds` | STRING | PT | Partition YYYYMMDD |
| `etl_time` | DATETIME | - | ETL timestamp |
| `dt` | STRING | - | Data date/hour range |

## Metric Naming

### Atomic Metrics
```
{action}_{object}
```
Examples: `click`, `impression`, `cost`, `order_cnt`

### Composite Metrics
```
{calc}_{base_metric}
```
Examples: `avg_cost`, `total_click`, `rate_cvr`

### Business Prefix

| Prefix | Source | Example |
|--------|--------|---------|
| `ad_` | 聚光投流 | `ad_click` |
| `kol_` | 蒲公英 | `kol_fee` |
| `jd_` | 小红盟 | `jd_order_cnt` |
| `tb_` | 小红星 | `tb_gmv` |

## Workflow

1. Identify object type (table/field/metric)
2. Determine layer and domain
3. Apply naming pattern
4. Verify against existing names in `models/`
5. Output formatted name with description
