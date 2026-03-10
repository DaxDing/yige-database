---
name: backfill_dw
type: tool
description: "数仓直接补数据：创意层补数据（API→ODS→DWD）、维表同步（PG→MC）、转化数据同步（PG→ODS→DWD）。Use when directly replenishing creative data, syncing dim tables from PG, or refreshing conversion tables. Trigger on 补数据、回填、维表同步、转化同步, or when user wants to run data pipelines locally without DataWorks."
allowed-tools: ["Bash", "Read"]
---

# 数仓直接补数据

本地直连 API/PG/MC 执行数据补录，不经过 DataWorks 平台。

> 如需通过 DataWorks 平台触发任务，使用 `/invoke_dataworks_cli`

## 无参数时先问

1. 要执行哪种操作？（creative / dim / conversion）
2. 对应参数是什么？

## 操作类型

| 类型 | 脚本 | 说明 |
|------|------|------|
| 创意层补数据 | `backfill.sh` + `load_creative_hi.py` | API → ODS → DWD |
| 维表同步 | `sync_pg_to_mc.py` | PG → MaxCompute |
| 分区回填 | `backfill_mc_partitions.py` | MC 分区复制 |
| 转化数据同步 | `sync_conversion.py` | PG → ODS → DWD（bycontent + bytask）|

## 1. 创意层补数据

API → `ods_xhs_creative_report_hi` → `dwd_xhs_creative_hi`，10 并发。

```bash
bash .claude/skills/backfill_dw/scripts/backfill.sh <advertiser_id> <start_date> <end_date>
```

## 2. 维表同步（PG → MaxCompute）

```bash
export $(cat .env | xargs) && python3 .claude/skills/backfill_dw/scripts/sync_pg_to_mc.py \
    --table <table_name> --partitions <ds_list>
```

支持的表：`dim_xhs_ad_product_df`, `dim_xhs_note_df`, `dim_xhs_project_df`, `dim_xhs_task_group_df`, `brg_xhs_note_project_df`

### 分区回填

```bash
export $(cat .env | xargs) && python3 .claude/skills/backfill_dw/scripts/backfill_mc_partitions.py \
    --table <name> --source-partition <ds> --target-partitions <ds_list>
```

## 3. 转化数据同步（PG → ODS → DWD）

bycontent + bytask 两条链路，全量执行。

```bash
export $(cat .env | xargs) && python3 .claude/skills/backfill_dw/scripts/sync_conversion.py
```

## Prerequisites

- `.env` with `ALIYUN_ACCESS_KEY_ID`, `ALIYUN_ACCESS_KEY_SECRET`, `DB_*`
- `pip install pyodps requests psycopg2-binary python-dotenv`

## Constraints

- 转化同步必须运行完整脚本，禁止手动执行部分步骤
- 执行前确保 `.env` 已加载
- 避免并发执行，分区覆写可能冲突
