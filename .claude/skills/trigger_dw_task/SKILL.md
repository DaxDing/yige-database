---
name: trigger_dw_task
type: tool
description: "通过 DataWorks 冒烟测试触发补数据任务，支持 14 种预定义任务（聚光/蒲公英/维度/转化/DWS/ADS/检查等）。Trigger on 触发任务、跑任务、重跑、补数据、backfill、check data, or when user wants to trigger DataWorks pipeline tasks by name."
allowed-tools: ["Bash", "Read"]
---

# 触发 DataWorks 任务

通过 RunSmokeTest API 触发预定义的补数据任务。

## 无参数时先问

1. 要触发哪个任务？
2. 日期范围？
3. 需要 advertiser_ids / user_ids 吗？

## Task Registry

| Task | Name | Node ID | Params |
|------|------|---------|--------|
| `creative` | 创意层小时离线报表 | 1033548404 | JG_MANUAL_IDS |
| `keyword` | 关键词日离线报表 | 1033548415 | JG_MANUAL_IDS |
| `searchword` | 搜索词日离线报表 | 1033548437 | JG_MANUAL_IDS |
| `audience` | 人群包日离线报表 | 1033548337 | JG_MANUAL_IDS |
| `account_flow` | 投流账户每日流水 | 1033548311 | JG_MANUAL_IDS |
| `dws_ads` | 重跑 DWS/ADS + Check | 1033677885 | — |
| `jg` | 补聚光数据 | 1033547989 | JG_MANUAL_IDS |
| `pgy` | 补蒲公英投后数据 | 1033549220 | PGY_MANUAL_IDS |
| `dim` | 补维度数据 | 1033548153 | — |
| `conversion` | 补后链路转化数据 | 1033548164 | — |
| `kpi` | 补规划数据（KPI+预算） | 1033602431 | — |
| `all` | 全部执行 | 1033549414 | JG_MANUAL_IDS, PGY_MANUAL_IDS |
| `check_rt` | 实时数据检查 | 1033707884 | — |
| `check` | 离线数据检查 | 1033548129 | — |

## Usage

```bash
SKILL_DIR=".claude/skills/trigger_dw_task"

export $(cat .env | xargs) && python3 $SKILL_DIR/scripts/backfill.py <task> \
    --start YYYY-MM-DD --end YYYY-MM-DD \
    [--jg-ids IDS] [--pgy-ids IDS] [--dry-run]
```

## Examples

```bash
# 补聚光创意层 3 天
python3 $SKILL_DIR/scripts/backfill.py creative \
    --start 2026-03-01 --end 2026-03-03 --jg-ids 7152346

# 补蒲公英投后数据
python3 $SKILL_DIR/scripts/backfill.py pgy \
    --start 2026-03-01 --end 2026-03-01 --pgy-ids 5cf89d080000000018003029

# 补维度数据（无需 IDs）
python3 $SKILL_DIR/scripts/backfill.py dim --start 2026-03-01 --end 2026-03-01

# 全部执行
python3 $SKILL_DIR/scripts/backfill.py all \
    --start 2026-03-01 --end 2026-03-03 \
    --jg-ids 7152346 --pgy-ids 5cf89d080000000018003029

# 离线数据检查
python3 $SKILL_DIR/scripts/backfill.py check --start 2026-03-01 --end 2026-03-01

# 仅预览不执行
python3 $SKILL_DIR/scripts/backfill.py creative \
    --start 2026-03-01 --end 2026-03-03 --jg-ids 7152346 --dry-run
```

## Common Workflows

| Scenario | Steps |
|----------|-------|
| 日常补全量 | `all --jg-ids ... --pgy-ids ...` |
| 仅补离线报表 | `creative` / `keyword` / `searchword` / `audience` |
| 补完后刷汇总层 | 先 `jg` / `pgy`，再 `dws_ads` |
| 补完后验证 | `check`（离线）/ `check_rt`（实时）|
| 维度+转化 | `dim` → `conversion` |

## Prerequisites

- `.env` with `ALIYUN_ACCESS_KEY_ID`, `ALIYUN_ACCESS_KEY_SECRET`
- `pip install alibabacloud-dataworks-public20200518`

## 查看 DAG 状态

触发任务后返回 dag_id，用 `check_dag.py` 查看执行状态：

```bash
export $(cat .env | xargs) && python3 $SKILL_DIR/scripts/check_dag.py <dag_id>
```

输出示例：
```
DAG: 123456  状态: ✅ SUCCESS
名称: backfill_1033548404_2026-03-01
类型: SMOKE_TEST
业务日期: 2026-03-01 00:00:00
创建时间: 2026-03-09 15:30:00
开始时间: 2026-03-09 15:30:05
结束时间: 2026-03-09 15:35:20
```

## Constraints

- 执行前用 `--dry-run` 预览
- 避免并发执行同一任务
