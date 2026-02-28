---
name: check_dim_push_status
type: tool
description: Checks PostgreSQL dimension table push status and freshness. Use when verifying dim table sync timing or diagnosing missing data.
allowed-tools: ["Bash", "Read"]
---

# Check Dim Push Status

Queries `sync_dim` PostgreSQL database to report latest push status for all 10 dimension/bridge tables. Auto-executes on invocation.

## Prerequisites

- `pip install psycopg2-binary python-dotenv`

## Commands

```bash
export $(cat .env | xargs) && python3 scripts/check_dim_push_status.py
```

No parameters required. Queries all tables automatically.

## Tables

| Table | Description |
|-------|-------------|
| dim_xhs_task_group_df | Task group dimension |
| dim_xhs_project_df | Project dimension |
| dim_xhs_ad_product_df | Ad product dimension |
| dim_xhs_note_df | Note dimension |
| brg_xhs_note_project_df | Note-project bridge |
| dim_xhs_creative_df | Creative dimension |
| dim_xhs_keyword_df | Keyword dimension |
| dim_xhs_target_df | Target dimension |
| dim_xhs_audience_segment_df | Audience segment dimension |
| dim_xhs_advertiser_df | Advertiser dimension |

## Push Rules

| Rule | Value |
|------|-------|
| Schedule | Daily 14:00, 22:00 |
| dt | T-1 business date |
| Update method | Daily snapshot |
| Retention | 30 days |

## Output

```
=== Dim Push Status (2026-02-26 15:00) ===

| Table                          | Latest dt  | Rows  | T-1 |
|--------------------------------|------------|-------|-----|
| dim_xhs_task_group_df          | 20260225   |   128 |  ✅ |
| dim_xhs_project_df             | 20260225   |    45 |  ✅ |
| dim_xhs_ad_product_df          | 20260224   |    32 |  ❌ |
| ...                            |            |       |     |

Summary: 8/10 tables up-to-date (T-1 = 20260225)
```

## Constraints

- Read-only queries; no data modification
- Connection uses hardcoded `sync_dim` database credentials
- Timeout: 10s per table query
