---
name: operate_maxcompute
description: Operates MaxCompute tables via PyODPS. Use when creating tables, executing SQL, or managing partitions.
allowed-tools: ["Bash", "Read", "Write"]
---

# MaxCompute Operations

Manage MaxCompute tables, partitions, and execute SQL via `scripts/maxcompute_ops.py`.

## Prerequisites

```bash
pip install pyodps
```

Environment variables in `.env`:
```bash
ALIYUN_ACCESS_KEY_ID=your_key
ALIYUN_ACCESS_KEY_SECRET=your_secret
```

## Commands

| Operation | Command |
|-----------|---------|
| List tables | `list-tables` |
| Table schema | `get-table <name>` |
| Create table | `create-table <json>` |
| Drop table | `drop-table <name>` |
| Execute SQL | `execute-sql "<sql>"` |
| List partitions | `list-partitions <name>` |
| Add partition | `add-partition <name> ds=YYYYMMDD` |

## Usage

```bash
python3 scripts/maxcompute_ops.py <command> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-p, --project` | Project name | `df_ch_530486` |
| `-e, --endpoint` | Endpoint region | `cn-hangzhou` |

## Examples

### List Tables
```bash
python3 scripts/maxcompute_ops.py list-tables
```

### View Schema
```bash
python3 scripts/maxcompute_ops.py get-table ods_xhs_creative_report_hi
```

### Create Table
```bash
python3 scripts/maxcompute_ops.py create-table tables/ods_xhs_creative_report_hi.json
```

### Execute SQL
```bash
# DDL
python3 scripts/maxcompute_ops.py execute-sql "ALTER TABLE t ADD COLUMN col STRING"

# Query
python3 scripts/maxcompute_ops.py execute-sql "SELECT * FROM t LIMIT 10"
```

### Partition Management
```bash
# List
python3 scripts/maxcompute_ops.py list-partitions ods_xhs_creative_report_hi

# Add
python3 scripts/maxcompute_ops.py add-partition ods_xhs_creative_report_hi ds=20260110
```

## JSON Table Definition

```json
{
  "name": "ods_xhs_creative_report_hi",
  "nameCn": "创意层小时报表",
  "fields": [
    {"name": "advertiser_id", "type": "STRING", "nameCn": "广告主ID"},
    {"name": "dt", "type": "STRING", "nameCn": "数据时间段"},
    {"name": "raw_data", "type": "STRING", "nameCn": "原始数据"},
    {"name": "etl_time", "type": "DATETIME", "nameCn": "ETL时间"},
    {"name": "ds", "type": "STRING", "nameCn": "分区日期", "key": "PT"}
  ]
}
```

### Field Markers

| Marker | Meaning |
|--------|---------|
| `"key": "PT"` | Partition column |
| `"key": "PK"` | Primary key (docs only) |

## Data Types

| Type | Description |
|------|-------------|
| `STRING` | Variable-length string |
| `BIGINT` | 64-bit integer |
| `DOUBLE` | Double precision float |
| `DECIMAL(p,s)` | Fixed precision decimal |
| `DATETIME` | Date and time |
| `BOOLEAN` | True/False |

## Workflow

1. Define table in JSON (follow `models/tables.js` structure)
2. Create table: `create-table <json>`
3. Verify: `get-table <name>`
4. Add partitions as needed
5. Execute SQL for data operations
