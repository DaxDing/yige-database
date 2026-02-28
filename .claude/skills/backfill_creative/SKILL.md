---
name: backfill_creative
description: Backfills creative layer and dimension data to MaxCompute. Use when replenishing dwd_xhs_creative_hi or syncing dim tables.
allowed-tools: ["Bash", "Read"]
arguments: "<advertiser_id> <start_date> <end_date>"
---

# Backfill Creative Layer

API → ODS → DWD 两阶段补数据，自动获取 token，10并发重跑 DWD。

## Prerequisites

- `.env` with `ALIYUN_ACCESS_KEY_ID`, `ALIYUN_ACCESS_KEY_SECRET`, `DB_*` (for PG sync)
- `pip install pyodps requests psycopg2-binary`
- Token API (`http://121.41.12.184`) accessible

## Invocation

```
/backfill_creative <advertiser_id> <start_date> <end_date>
```

| Argument | Format | Example |
|----------|--------|---------|
| `advertiser_id` | integer | `6209396` |
| `start_date` | YYYY-MM-DD | `2026-01-01` |
| `end_date` | YYYY-MM-DD | `2026-01-31` |

## Auto-Execute

On invocation, immediately run:

```bash
bash .claude/skills/backfill_creative/scripts/backfill.sh <advertiser_id> <start_date> <end_date>
```

**Data Flow**: API → `ods_xhs_creative_report_hi` → `dwd_xhs_creative_hi` (10并发)

## Additional Scripts

### sync_pg_to_mc.py — PostgreSQL → MaxCompute 维表同步

```bash
python3 scripts/sync_pg_to_mc.py --table <table_name> --partitions <ds_list>
```

| Parameter | Description |
|-----------|-------------|
| `--table` | `dim_xhs_ad_product_df`, `dim_xhs_note_df`, `dim_xhs_project_df`, `dim_xhs_task_group_df`, `brg_xhs_note_project_df` |
| `--partitions` | Comma-separated YYYYMMDD, e.g. `20260126,20260127` |

### backfill_mc_partitions.py — MaxCompute 分区回填

```bash
python3 scripts/backfill_mc_partitions.py --table <name> --source-partition <ds> --target-partitions <ds_list>
```

## Examples

```
/backfill_creative 6209396 2026-01-01 2026-01-31
/backfill_creative 6209396 2026-02-10 2026-02-25
```
