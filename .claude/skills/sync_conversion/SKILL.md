---
name: sync_conversion
type: tool
description: Syncs grass alliance conversion data from PostgreSQL to MaxCompute ODS and reruns DWD ETL. Use when refreshing conversion tables for bycontent and bytask dimensions.
allowed-tools: ["Bash", "Read"]
---

# Sync Conversion Data

Syncs two conversion table pairs (bycontent + bytask) from PostgreSQL ODS to MaxCompute ODS, then reruns DWD ETL with 10-worker concurrency. Auto-executes on invocation.

## Prerequisites

- `.env` with `ALIYUN_ACCESS_KEY_ID`, `ALIYUN_ACCESS_KEY_SECRET`
- `pip install pyodps psycopg2-binary python-dotenv`
- PostgreSQL `xhs_conversion` database accessible

## Commands

```bash
export $(cat .env | xargs) && python3 scripts/sync_conversion.py
```

No parameters required. Runs full pipeline automatically.

## Pipeline

| Step | Source | Target | Method |
|------|--------|--------|--------|
| 1 | PG `ods_xhs_grass_bycontent_conversion_di` | MC `ods_xhs_grass_bycontent_conversion_di` | Partition overwrite |
| 2 | PG `ods_xhs_grass_bytask_conversion_di` | MC `ods_xhs_grass_bytask_conversion_di` | Partition overwrite |
| 3 | MC ODS bycontent | MC `dwd_xhs_conversion_bycontent_di` | SQL INSERT OVERWRITE (10 workers) |
| 4 | MC ODS bytask | MC `dwd_xhs_conversion_bytask_di` | SQL INSERT OVERWRITE (10 workers) |

## Table Schema

### bycontent (PG columns -> MC columns)

| PG Column | MC Column | Type |
|-----------|-----------|------|
| task_id | task_id | STRING |
| note_id | note_id | STRING |
| dt | dt | STRING |
| attribution_period | attribution_period | STRING |
| grass_alliance | grass_alliance | STRING |
| raw_data | raw_data | STRING (JSON) |
| -- | etl_time | DATETIME |
| -- | ds | STRING (PT) |

### bytask (PG columns -> MC columns)

| PG Column | MC Column | Type |
|-----------|-----------|------|
| task_id | task_id | STRING |
| dt | dt | STRING |
| attribution_period | attribution_period | STRING |
| grass_alliance | grass_alliance | STRING |
| raw_data | raw_data | STRING (JSON) |
| -- | etl_time | DATETIME |
| -- | ds | STRING (PT) |

## Output

Prints per-partition progress and final summary:

```
=== Step 1/4: PG -> ODS bycontent ===
45 partitions to sync
[20260101] 120 rows OK
[20260102] 115 rows OK
...
Subtotal: 5,400 rows

=== Step 3/4: ODS -> DWD bycontent (10 workers) ===
45 partitions to rerun
[20260101] OK
[20260102] OK
...
Done: 45 OK, 0 FAIL

=== Summary ===
| Table | ODS Rows | DWD Partitions | DWD Failures |
|-------|----------|----------------|--------------|
| bycontent | 5,400 | 45 | 0 |
| bytask | 3,200 | 45 | 0 |
```

## Workflow

**CRITICAL**: Execute via single command. Script handles all steps sequentially.

1. Load environment variables
2. Connect to PostgreSQL, fetch distinct dates
3. Sync bycontent ODS partitions (sequential)
4. Sync bytask ODS partitions (sequential)
5. Rerun bycontent DWD via SQL (10-worker parallel)
6. Rerun bytask DWD via SQL (10-worker parallel)
7. Print summary

## Examples

```bash
# Standard execution (auto-runs full pipeline)
export $(cat .env | xargs) && python3 scripts/sync_conversion.py
```

## Error Handling

| Error | Behavior |
|-------|----------|
| PG connection failure | Exits with error message |
| MC partition write failure | Logs error, continues to next partition |
| DWD SQL failure | Logs error, counts as failure in summary |
| Empty partition | Skips, logs warning |

## Constraints

- Do NOT run partial steps manually; always execute the full script
- Ensure `.env` is loaded before execution; missing keys cause immediate exit
- Avoid running concurrent instances; partition overwrites may conflict
