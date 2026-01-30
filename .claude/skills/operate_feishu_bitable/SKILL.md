---
name: operate_feishu_bitable
type: tool
description: Operates Feishu Bitable and Sheets via API. Use when reading, writing, or managing table data. Defaults to Bitable.
---

# Operate Feishu Tables

Read and write records in Feishu Bitable (multi-dimensional tables) and Sheets (spreadsheets).

## Prerequisites

Environment variables required:

| Variable | Description |
|----------|-------------|
| `FEISHU_APP_ID` | Application ID from Feishu Open Platform |
| `FEISHU_APP_SECRET` | Application Secret |

## Bitable Commands (Default)

```bash
# List records
python3 scripts/bitable.py list <app_token> <table_id> [--limit N]

# Get single record
python3 scripts/bitable.py get <app_token> <table_id> <record_id>

# Create record
python3 scripts/bitable.py create <app_token> <table_id> --fields '{"Name": "value"}'

# Batch create records
python3 scripts/bitable.py batch-create <app_token> <table_id> --file records.json

# Update record
python3 scripts/bitable.py update <app_token> <table_id> <record_id> --fields '{"Name": "new"}'

# Delete record
python3 scripts/bitable.py delete <app_token> <table_id> <record_id>
```

## Sheets Commands

```bash
# Read range
python3 scripts/sheets.py read <spreadsheet_token> <sheet_id> --range "A1:D10"

# Read all data
python3 scripts/sheets.py read <spreadsheet_token> <sheet_id>

# Write range
python3 scripts/sheets.py write <spreadsheet_token> <sheet_id> --range "A1" --values '[["a","b"],["c","d"]]'

# Append rows
python3 scripts/sheets.py append <spreadsheet_token> <sheet_id> --values '[["new1"],["new2"]]'

# Update cells
python3 scripts/sheets.py update <spreadsheet_token> <sheet_id> --range "A1:B2" --values '[["x","y"],["z","w"]]'

# Delete rows
python3 scripts/sheets.py delete-rows <spreadsheet_token> <sheet_id> --start 2 --count 5

# Get sheet info
python3 scripts/sheets.py info <spreadsheet_token>
```

## Parameters

### Bitable

Get `app_token` and `table_id` from URL:

```
https://feishu.cn/base/{app_token}?table={table_id}
```

For Wiki-based Bitable (URL starts with `/wiki`), use `get-app-token` command.

### Sheets

Get `spreadsheet_token` and `sheet_id` from URL:

```
https://feishu.cn/sheets/{spreadsheet_token}?sheet={sheet_id}
```

## Bitable Examples

### List Records

```bash
python3 scripts/bitable.py list bascnXXXXXX tblXXXXXX --limit 10
```

Output:
```json
{
  "total": 100,
  "records": [
    {"record_id": "recXXX", "fields": {"Name": "Alice", "Age": 25}}
  ]
}
```

### Create Record

```bash
python3 scripts/bitable.py create bascnXXXXXX tblXXXXXX \
  --fields '{"Name": "Bob", "Email": "bob@example.com"}'
```

### Batch Create from JSON

```bash
# records.json: [{"Name": "A"}, {"Name": "B"}]
python3 scripts/bitable.py batch-create bascnXXXXXX tblXXXXXX --file records.json
```

## Sheets Examples

### Read Range

```bash
python3 scripts/sheets.py read shtcnXXXXXX 0 --range "A1:C10"
```

Output:
```json
{
  "values": [
    ["Name", "Age", "Email"],
    ["Alice", 25, "alice@example.com"]
  ]
}
```

### Write Data

```bash
python3 scripts/sheets.py write shtcnXXXXXX 0 --range "A1" \
  --values '[["Name","Age"],["Bob",30]]'
```

### Append Rows

```bash
python3 scripts/sheets.py append shtcnXXXXXX 0 \
  --values '[["Charlie",28],["Diana",32]]'
```

## Field Types (Bitable)

| Type | JSON Format | Example |
|------|-------------|---------|
| Text | `string` | `"Hello"` |
| Number | `number` | `123` |
| Select | `string` | `"Option1"` |
| Multi-select | `array` | `["A", "B"]` |
| Date | `number` (ms) | `1704067200000` |
| Checkbox | `boolean` | `true` |
| Person | `array` | `[{"id": "ou_xxx"}]` |
| Link | `object` | `{"link": "url", "text": "name"}` |

## Output

### Bitable Record

| Field | Description |
|-------|-------------|
| `record_id` | Unique identifier |
| `fields` | Key-value pairs |
| `created_time` | Creation timestamp |
| `last_modified_time` | Last update timestamp |

### Sheets Data

| Field | Description |
|-------|-------------|
| `values` | 2D array of cell values |
| `range` | Affected range (e.g., "A1:C10") |

## Reference

- [scripts/bitable.py](./scripts/bitable.py) - Bitable CLI script
- [scripts/sheets.py](./scripts/sheets.py) - Sheets CLI script
- [Feishu Bitable API](https://open.feishu.cn/document/server-docs/docs/bitable-v1/bitable-overview)
- [Feishu Sheets API](https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet/spreadsheet-overview)
