---
name: invoke_dataworks_cli
description: Invokes Alibaba Cloud DataWorks CLI with authentication, error handling, and retry logic. Use when working with DataWorks nodes, data integration, scheduling, or MaxCompute operations.
allowed-tools: ["*"]
---

# DataWorks CLI

Invoke Alibaba Cloud DataWorks CLI with authentication, error handling, and retry logic.

## Documentation Index

> **Important**: Read relevant docs in `references/` before developing DataWorks tasks.

| Document | Content | Use Case |
|----------|---------|----------|
| [nodes.md](./references/nodes.md) | Node types | Choose appropriate node |
| [shell_node.md](./references/shell_node.md) | Shell development | Write shell scripts |
| [python_node.md](./references/python_node.md) | Python development | PyODPS/Assignment/Notebook |
| [context_parameters.md](./references/context_parameters.md) | Parameter passing | Pass params between nodes |
| [data_integration.md](./references/data_integration.md) | Data integration | API/Database sync |
| [data_quality.md](./references/data_quality.md) | Data quality | Rules, monitoring, alerts |
| [data_security.md](./references/data_security.md) | Data security | Permissions, masking, audit |
| [scheduling.md](./references/scheduling.md) | Scheduling | Cron, dependencies |
| [resources.md](./references/resources.md) | Resource management | Resource groups, data sources |
| [openapi.md](./references/openapi.md) | OpenAPI | CLI/SDK invocation |
| [troubleshooting.md](./references/troubleshooting.md) | Troubleshooting | Error resolution |

## Quick Reference

### Shell Node Key Points

| Point | Description |
|-------|-------------|
| Runtime | `/bin/sh` (POSIX), not bash |
| Param format | `$1`=`KEY=VALUE`, use `eval "$1"` to parse |
| No jq | Use `grep -o` + `sed` for JSON parsing |
| Param passing | Must use Assignment Node, `echo` on last line |

### Assignment Node Config

```
Upstream (Assignment Node): echo "$token"  →  outputs (auto)
Downstream (Input Param): select outputs  →  use ${param_name} in code
```

### Common Error Quick Reference

| Error | Document |
|-------|----------|
| `command not found` | [shell_node.md](./references/shell_node.md#runtime) |
| `${outputs.xxx}` not replaced | [context_parameters.md](./references/context_parameters.md#common-issues) |
| Invalid token | [troubleshooting.md](./references/troubleshooting.md#api-auth-errors) |

## CLI Usage

### Installation

```bash
# macOS
brew install aliyun-cli

# Linux
wget https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz
tar -xzf aliyun-cli-linux-latest-amd64.tgz && sudo mv aliyun /usr/local/bin/
```

### Configuration

Add to `.env`:
```bash
ALIYUN_ACCESS_KEY_ID=your_access_key_id
ALIYUN_ACCESS_KEY_SECRET=your_access_key_secret
```

### Invocation

```bash
python3 scripts/invoke_dataworks.py dataworks-public ListProjects --region cn-hangzhou
```

### Common Commands

| Operation | Command |
|-----------|---------|
| List projects | `ListProjects --region cn-hangzhou` |
| Project details | `GetProject --ProjectId 123` |
| List data sources | `ListDataSources --ProjectId 123` |
| List nodes | `ListNodes --ProjectId 123` |

Full commands: [dataworks_cli_commands.md](./references/dataworks_cli_commands.md)

## MaxCompute Table Management

Manage MaxCompute tables via `scripts/maxcompute_ops.py`.

### Install Dependencies

```bash
pip install pyodps
```

### Commands

| Operation | Command |
|-----------|---------|
| List tables | `python3 scripts/maxcompute_ops.py list-tables` |
| Table details | `python3 scripts/maxcompute_ops.py get-table <table_name>` |
| Create from JSON | `python3 scripts/maxcompute_ops.py create-table <json_file>` |
| Drop table | `python3 scripts/maxcompute_ops.py drop-table <table_name>` |
| Execute SQL | `python3 scripts/maxcompute_ops.py execute-sql "<sql>"` |
| List partitions | `python3 scripts/maxcompute_ops.py list-partitions <table_name>` |
| Add partition | `python3 scripts/maxcompute_ops.py add-partition <table_name> ds=20260108` |

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-p, --project` | MaxCompute project name | `df_ch_530486` |
| `-e, --endpoint` | MaxCompute endpoint | `cn-hangzhou` |

### Examples

```bash
# List all tables
python3 scripts/maxcompute_ops.py list-tables

# Create table from JSON definition
python3 scripts/maxcompute_ops.py create-table project/database_plan/tables/ods/ods_xhs_creative_report_hi.json

# View table schema
python3 scripts/maxcompute_ops.py get-table dwd_xhs_creative_hourly_di

# Execute DDL
python3 scripts/maxcompute_ops.py execute-sql "ALTER TABLE my_table ADD COLUMN new_col STRING"
```

### JSON Table Definition Format

```json
{
  "name": "table_name",
  "nameCn": "Table Chinese Name",
  "fields": [
    {"name": "col1", "type": "STRING", "nameCn": "Column description"},
    {"name": "ds", "type": "STRING", "nameCn": "Partition date", "key": "PT"}
  ]
}
```

| Field | Description |
|-------|-------------|
| `key: "PT"` | Mark as partition column |
| `key: "PK"` | Mark as primary key (docs only) |

## Error Handling

| Type | Strategy |
|------|----------|
| Network timeout | 3 retries, exponential backoff |
| API rate limit | 5 retries, 60s interval |
| Credential error | Fail immediately |

## Official Documentation

- [DataWorks Docs](https://help.aliyun.com/zh/dataworks/)
- [Alibaba Cloud CLI](https://www.alibabacloud.com/help/en/alibaba-cloud-cli)
- [DataWorks API Reference](https://www.alibabacloud.com/help/en/dataworks/developer-reference/api-overview)
- [MaxCompute Docs](https://help.aliyun.com/zh/maxcompute/)
- [PyODPS Docs](https://pyodps.readthedocs.io/)
