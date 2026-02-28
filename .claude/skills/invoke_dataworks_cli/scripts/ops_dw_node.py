#!/usr/bin/env python3
"""DataWorks 运维管理 - 运行、停止、重跑、查看实例状态与日志"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ID = "530486"
PROJECT_ENV = "PROD"
REGION = "cn-hangzhou"
CLI_SCRIPT = str(Path(__file__).parent / "invoke_dataworks.py")

STATUS_MAP = {
    "NOT_RUN": "未运行",
    "WAIT_TIME": "等待时间",
    "WAIT_RESOURCE": "等待资源",
    "RUNNING": "运行中",
    "SUCCESS": "成功",
    "FAILURE": "失败",
    "TIMEOUT": "超时",
}

STATUS_ICON = {
    "NOT_RUN": "⏸",
    "WAIT_TIME": "⏳",
    "WAIT_RESOURCE": "⏳",
    "RUNNING": "🔄",
    "SUCCESS": "✅",
    "FAILURE": "❌",
    "TIMEOUT": "⏰",
}


def call_api(api, include_project=True, **params):
    """调用 DataWorks API"""
    cmd = ["python3", CLI_SCRIPT, "dataworks-public", api, "--region", REGION]
    if include_project:
        cmd.extend(["--ProjectId", PROJECT_ID])
    for k, v in params.items():
        cmd.extend([f"--{k}", str(v)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"API 错误: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def find_node_id(workflow_name, node_name):
    """通过工作流名+节点名找到节点 ID"""
    data = call_api("ListNodes")
    nodes = data.get("PagingInfo", {}).get("Nodes", [])
    path = f"{workflow_name}/{node_name}"
    for n in nodes:
        if n.get("Script", {}).get("Path", "") == path:
            return n["Id"]
    # 尝试模糊匹配节点名
    for n in nodes:
        if n.get("Name") == node_name:
            return n["Id"]
    print(f"未找到节点: {path}", file=sys.stderr)
    sys.exit(1)


def resolve_node_id(args):
    """从 args 解析节点 ID（支持直接 ID 或 workflow+node）"""
    if hasattr(args, "node_id") and args.node_id:
        return int(args.node_id)
    return find_node_id(args.workflow, args.node)


def default_biz_date():
    """默认业务日期 = T-1"""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def cmd_run(args):
    """运行周期任务"""
    node_id = resolve_node_id(args)
    biz_date = args.biz_date or default_biz_date()

    print(f">>> 触发运行 NodeId={node_id} BizDate={biz_date}")

    data = call_api(
        "RunCycleDagNodes",
        include_project=False,
        ProjectEnv=PROJECT_ENV,
        NodeId=node_id,
        BizDate=biz_date,
    )
    print(f">>> 触发成功 ✓")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_smoke(args):
    """冒烟测试"""
    node_id = resolve_node_id(args)
    biz_date = args.biz_date or default_biz_date()

    print(f">>> 冒烟测试 NodeId={node_id} BizDate={biz_date}")

    data = call_api(
        "RunSmokeTest",
        include_project=False,
        ProjectEnv=PROJECT_ENV,
        NodeId=node_id,
        Bizdate=biz_date,
    )
    print(f">>> 触发成功 ✓")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_stop(args):
    """停止实例"""
    print(f">>> 停止实例 InstanceId={args.instance_id}")

    data = call_api(
        "StopInstance",
        include_project=False,
        ProjectEnv=PROJECT_ENV,
        InstanceId=args.instance_id,
    )
    print(f">>> 停止成功 ✓")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_rerun(args):
    """重跑实例"""
    print(f">>> 重跑实例 InstanceId={args.instance_id}")

    data = call_api(
        "RerunInstance",
        include_project=False,
        ProjectEnv=PROJECT_ENV,
        InstanceId=args.instance_id,
    )
    print(f">>> 重跑成功 ✓")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_status(args):
    """查看节点实例列表"""
    node_id = resolve_node_id(args)
    limit = args.limit or 10

    print(f">>> 查询实例 NodeId={node_id} 最近{limit}条\n")

    data = call_api(
        "ListInstances",
        ProjectEnv=PROJECT_ENV,
        NodeId=node_id,
        PageNumber=1,
        PageSize=limit,
    )

    instances = data.get("Data", {}).get("Instances", [])
    if not instances:
        print("无实例记录")
        return

    print(f"  {'状态':<6s} {'实例ID':<18s} {'业务日期':<14s} {'开始时间':<22s} {'结束时间':<22s}")
    print(f"  {'─'*6} {'─'*18} {'─'*14} {'─'*22} {'─'*22}")

    for inst in instances:
        status = inst.get("Status", "UNKNOWN")
        icon = STATUS_ICON.get(status, "?")
        status_cn = STATUS_MAP.get(status, status)
        inst_id = inst.get("InstanceId", "")
        biz_date = inst.get("BizDate", "")
        begin = inst.get("BeginRunningTime", "-")
        end = inst.get("FinishTime", "-")
        print(f"  {icon} {status_cn:<4s} {inst_id:<18s} {biz_date:<14s} {begin:<22s} {end:<22s}")


def cmd_log(args):
    """获取实例日志"""
    print(f">>> 获取日志 InstanceId={args.instance_id}\n")

    data = call_api(
        "GetInstanceLog",
        include_project=False,
        ProjectEnv=PROJECT_ENV,
        InstanceId=args.instance_id,
    )
    log = data.get("Data", "")
    if log:
        print(log)
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_detail(args):
    """获取实例详情"""
    print(f">>> 查询实例详情 InstanceId={args.instance_id}\n")

    data = call_api(
        "GetInstance",
        include_project=False,
        ProjectEnv=PROJECT_ENV,
        InstanceId=args.instance_id,
    )
    print(json.dumps(data, indent=2, ensure_ascii=False))


def add_node_args(parser):
    """添加节点定位参数（支持 workflow+node 或直接 node_id）"""
    parser.add_argument("workflow", help="工作流名称")
    parser.add_argument("node", help="节点名称")


def main():
    parser = argparse.ArgumentParser(description="DataWorks 运维管理")
    sub = parser.add_subparsers(dest="command")

    # run
    p_run = sub.add_parser("run", help="运行周期任务")
    add_node_args(p_run)
    p_run.add_argument("--biz-date", help="业务日期 (YYYY-MM-DD)，默认 T-1")

    # smoke
    p_smoke = sub.add_parser("smoke", help="冒烟测试")
    add_node_args(p_smoke)
    p_smoke.add_argument("--biz-date", help="业务日期 (YYYY-MM-DD)，默认 T-1")

    # stop
    p_stop = sub.add_parser("stop", help="停止实例")
    p_stop.add_argument("instance_id", help="实例 ID")

    # rerun
    p_rerun = sub.add_parser("rerun", help="重跑实例")
    p_rerun.add_argument("instance_id", help="实例 ID")

    # status
    p_status = sub.add_parser("status", help="查看节点实例列表")
    add_node_args(p_status)
    p_status.add_argument("--limit", type=int, default=10, help="显示条数 (默认 10)")

    # log
    p_log = sub.add_parser("log", help="获取实例日志")
    p_log.add_argument("instance_id", help="实例 ID")

    # detail
    p_detail = sub.add_parser("detail", help="获取实例详情")
    p_detail.add_argument("instance_id", help="实例 ID")

    args = parser.parse_args()

    handlers = {
        "run": cmd_run,
        "smoke": cmd_smoke,
        "stop": cmd_stop,
        "rerun": cmd_rerun,
        "status": cmd_status,
        "log": cmd_log,
        "detail": cmd_detail,
    }

    handler = handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
