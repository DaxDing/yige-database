---
name: query_aliyun_billing
type: tool
description: Queries Alibaba Cloud billing via aliyun CLI. Use when checking account balance, bill overview, or instance-level cost breakdown. Trigger on any mention of 阿里云账单、费用、余额、云账单、billing、cost, or when the user wants to know how much they're spending on cloud services.
allowed-tools: ["Bash", "Read"]
arguments: "balance or overview or detail, YYYY-MM, --product code, --date YYYY-MM-DD"
---

# Query Aliyun Billing

Query Alibaba Cloud billing details using `aliyun` CLI. Auto-executes on invocation.

## Prerequisites

- `aliyun` CLI installed (`brew install aliyun-cli`)
- `jq` installed
- `.env` contains `ALIYUN_ACCESS_KEY_ID` and `ALIYUN_ACCESS_KEY_SECRET`

## Commands

```bash
# 账户余额
export $(cat .env | xargs) && bash .claude/skills/query_aliyun_billing/scripts/query_billing.sh balance

# 月度账单总览（默认当月）
export $(cat .env | xargs) && bash .claude/skills/query_aliyun_billing/scripts/query_billing.sh overview 2026-03

# 实例级账单明细（按日）
export $(cat .env | xargs) && bash .claude/skills/query_aliyun_billing/scripts/query_billing.sh detail 2026-03 --date 2026-03-09

# 按产品过滤明细
export $(cat .env | xargs) && bash .claude/skills/query_aliyun_billing/scripts/query_billing.sh detail 2026-03 --product odps
```

## Subcommands

| Command | Description | Default |
|---------|-------------|---------|
| `balance` | 查询账户可用余额 | - |
| `overview` | 按产品汇总的月度账单 | 当月 |
| `detail` | 实例级账单明细（自动分页） | 前一天 |

## Options

| Flag | Description | Used By |
|------|-------------|---------|
| `YYYY-MM` | 账期（第二个参数） | overview, detail |
| `--date YYYY-MM-DD` | 指定日期（DAILY 粒度） | detail |
| `--product <code>` | 按产品过滤（odps/ecs/rds/oss 等） | detail |

## Common Product Codes

| Code | Product |
|------|---------|
| `odps` | MaxCompute |
| `oss` | OSS 对象存储 |
| `ecs` | ECS 云服务器 |
| `rds` | RDS 云数据库 |
| `cdn` | CDN |
| `dataworks` | DataWorks |

## Default Workflow

未指定子命令时，并行执行 `balance` + `detail`（昨日），然后按下方模板输出。

## Output Template

ALWAYS use this exact template to present results. Merge balance and detail into one unified view，聚焦前一天消费。

```
**账户余额**: ¥{available_amount}

**{date} 消费**: ¥{day_total}

| 产品 | 金额 | 占比 |
|------|------|------|
| {product_1} | ¥{day_amt} | {pct}% |
| {product_2} | ¥{day_amt} | {pct}% |
| ... | | |
| **合计** | **¥{day_total}** | **100%** |
```

Rules:
- 金额保留 2 位小数
- 按金额降序排列
- 占比 = 该产品昨日消费 / 昨日总消费 × 100，保留 1 位小数
- 同产品多条明细（如 DataWorks 的多个计费项）合并为一行

## Constraints

- Read-only, no modifications
- Data delayed ~24h, current month data is preliminary until next month 3rd
- Rate limit: 10 QPS
- Max 18 months history
