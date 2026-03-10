#!/usr/bin/env python3
"""DataWorks 补数据脚本

Usage:
    backfill.py <task> --start DATE --end DATE [--jg-ids IDS] [--pgy-ids IDS] [--dry-run]

Examples:
    # 补聚光创意层数据
    backfill.py creative --start 2026-03-01 --end 2026-03-03 --jg-ids 7152346

    # 补蒲公英投后数据
    backfill.py pgy --start 2026-03-01 --end 2026-03-01 --pgy-ids 5cf89d080000000018003029

    # 补维度数据
    backfill.py dim --start 2026-03-01 --end 2026-03-01

    # 全部执行
    backfill.py all --start 2026-03-01 --end 2026-03-03 --jg-ids 7152346 --pgy-ids xxx

    # 仅打印不执行
    backfill.py creative --start 2026-03-01 --end 2026-03-01 --dry-run
"""

import argparse
import os
import sys
from datetime import datetime, timedelta

# Task registry: name -> (node_id, params)
TASKS = {
    "creative":     (1033548404, ["JG_MANUAL_IDS"]),
    "keyword":      (1033548415, ["JG_MANUAL_IDS"]),
    "searchword":   (1033548437, ["JG_MANUAL_IDS"]),
    "audience":     (1033548337, ["JG_MANUAL_IDS"]),
    "account_flow": (1033548311, ["JG_MANUAL_IDS"]),
    "dws_ads":      (1033677885, []),
    "jg":           (1033547989, ["JG_MANUAL_IDS"]),
    "pgy":          (1033549220, ["PGY_MANUAL_IDS"]),
    "dim":          (1033548153, []),
    "conversion":   (1033548164, []),
    "kpi":          (1033602431, []),
    "all":          (1033549414, ["JG_MANUAL_IDS", "PGY_MANUAL_IDS"]),
    "check_rt":     (1033707884, []),
    "check":        (1033548129, []),
}

# Display names for output
TASK_NAMES = {
    "creative":     "创意层小时离线报表",
    "keyword":      "关键词日离线报表",
    "searchword":   "搜索词日离线报表",
    "audience":     "人群包日离线报表",
    "account_flow": "投流账户每日流水",
    "dws_ads":      "重跑 DWS/ADS + Check",
    "jg":           "补聚光数据",
    "pgy":          "补蒲公英投后数据",
    "dim":          "补维度数据",
    "conversion":   "补后链路转化数据",
    "kpi":          "补规划数据（KPI+预算）",
    "all":          "全部执行",
    "check_rt":     "实时数据检查",
    "check":        "离线数据检查",
}


def create_client():
    """Create DataWorks API client."""
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_dataworks_public20200518.client import Client

    ak = os.getenv("ALIYUN_ACCESS_KEY_ID")
    sk = os.getenv("ALIYUN_ACCESS_KEY_SECRET")
    if not ak or not sk:
        print("Error: ALIYUN_ACCESS_KEY_ID and ALIYUN_ACCESS_KEY_SECRET required", file=sys.stderr)
        sys.exit(1)

    return Client(Config(
        access_key_id=ak,
        access_key_secret=sk,
        endpoint="dataworks.cn-hangzhou.aliyuncs.com",
    ))


def run_backfill(client, node_id, date_str, node_params, dry_run=False):
    """Run smoke test for a single date."""
    from alibabacloud_dataworks_public20200518.models import RunSmokeTestRequest

    if dry_run:
        print(f"  [DRY-RUN] node={node_id} date={date_str} params={node_params}")
        return "dry-run"

    resp = client.run_smoke_test(RunSmokeTestRequest(
        project_env="PROD",
        bizdate=f"{date_str} 00:00:00",
        name=f"backfill_{node_id}_{date_str}",
        node_id=node_id,
        node_params=node_params,
    ))
    return resp.body.data


def main():
    parser = argparse.ArgumentParser(description="DataWorks 补数据")
    parser.add_argument("task", choices=list(TASKS.keys()), help="Task name")
    parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--jg-ids", default="", help="聚光 advertiser_ids (comma-separated)")
    parser.add_argument("--pgy-ids", default="", help="蒲公英 user_ids (comma-separated)")
    parser.add_argument("--dry-run", action="store_true", help="Print without executing")
    args = parser.parse_args()

    node_id, required_params = TASKS[args.task]
    task_name = TASK_NAMES[args.task]

    # Validate required params
    if "JG_MANUAL_IDS" in required_params and not args.jg_ids:
        print(f"Error: --jg-ids required for task '{args.task}'", file=sys.stderr)
        sys.exit(1)
    if "PGY_MANUAL_IDS" in required_params and not args.pgy_ids:
        print(f"Error: --pgy-ids required for task '{args.task}'", file=sys.stderr)
        sys.exit(1)

    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")
    days = (end - start).days + 1

    print(f"Task: {task_name} (node_id={node_id})")
    print(f"Date: {args.start} ~ {args.end} ({days} days)")
    if args.jg_ids:
        print(f"JG IDs: {args.jg_ids}")
    if args.pgy_ids:
        print(f"PGY IDs: {args.pgy_ids}")
    print()

    client = None if args.dry_run else create_client()

    current = start
    results = []
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        bizdate_str = date_str.replace("-", "")

        node_params = f"bizdate={bizdate_str}"
        if args.jg_ids:
            node_params += f" jg_manual_ids={args.jg_ids}"
        if args.pgy_ids:
            node_params += f" pgy_manual_ids={args.pgy_ids}"

        dag_id = run_backfill(client, node_id, date_str, node_params, args.dry_run)
        print(f"  [{date_str}] dag_id={dag_id}")
        results.append((date_str, dag_id))
        current += timedelta(days=1)

    print(f"\nDone: {len(results)} days submitted")


if __name__ == "__main__":
    main()
