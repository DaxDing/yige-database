"""DataWorks 工作流调度时间修改脚本

通过 GetWorkflow → UpdateWorkflow 修改工作流调度时间（自动发布）

Usage:
    # 查看当前调度配置
    export $(cat .env | xargs) && python3.12 dataworks/code/update_node_schedule.py get

    # 修改为 CRON_EXPR 配置的时间
    export $(cat .env | xargs) && python3.12 dataworks/code/update_node_schedule.py set

    # 指定 cron 表达式
    export $(cat .env | xargs) && python3.12 dataworks/code/update_node_schedule.py set "00 35 22 * * ?"

    # 通过 hour/minute 快捷修改
    export $(cat .env | xargs) && python3.12 dataworks/code/update_node_schedule.py set --hour 22 --minute 35
"""

import argparse
import json
import os
import subprocess
import sys
import time

# ============ 配置 ============
WORKFLOW_ID = 1033549414
CRON_EXPR = "00 35 22 * * ?"
REGION = "cn-hangzhou"
# ==============================


def call_api(api, **params):
    """直接调用 aliyun CLI"""
    env = os.environ.copy()
    env["ALIBABA_CLOUD_ACCESS_KEY_ID"] = os.getenv("ALIYUN_ACCESS_KEY_ID", "")
    env["ALIBABA_CLOUD_ACCESS_KEY_SECRET"] = os.getenv("ALIYUN_ACCESS_KEY_SECRET", "")

    cmd = ["aliyun", "dataworks-public", api, "--region", REGION]
    for k, v in params.items():
        cmd.extend([f"--{k}", str(v)])

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"API 错误: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def get_workflow():
    """获取工作流配置"""
    data = call_api("GetWorkflow", Id=WORKFLOW_ID)
    return data["Workflow"]


def show_schedule():
    """展示当前调度配置"""
    wf = get_workflow()
    trigger = wf.get("Trigger", {})
    print(f"工作流:  {wf['Name']} (ID: {wf['Id']})")
    print(f"Cron:    {trigger.get('Cron', '未知')}")
    print(f"类型:    {trigger.get('Type', '未知')}")
    print(f"周期:    {trigger.get('Recurrence', '未知')}")
    print(f"生效:    {trigger.get('StartTime', '')} ~ {trigger.get('EndTime', '')}")
    print(f"参数:    {wf.get('Parameters', '')}")
    print(f"子任务:  {len(wf.get('Tasks', []))} 个")


def update_schedule(cron_expr):
    """修改工作流调度时间"""
    wf = get_workflow()
    trigger = wf.get("Trigger", {})
    old_cron = trigger.get("Cron", "")

    print(f"工作流: {wf['Name']} (ID: {wf['Id']})")
    print(f"原 cron: {old_cron}")
    print(f"新 cron: {cron_expr}")

    if old_cron == cron_expr:
        print("\ncron 未变化，跳过")
        return

    new_trigger = json.dumps({
        "Type": trigger.get("Type", "Scheduler"),
        "Cron": cron_expr,
        "Recurrence": trigger.get("Recurrence", "Normal"),
        "StartTime": trigger.get("StartTime", "1970-01-01 00:00:00"),
        "EndTime": trigger.get("EndTime", "9999-01-01 00:00:00"),
    }, ensure_ascii=False)

    print("\n更新工作流...")
    data = call_api(
        "UpdateWorkflow",
        Id=WORKFLOW_ID,
        Name=wf["Name"],
        Owner=wf["Owner"],
        Trigger=new_trigger,
    )
    if data.get("Success"):
        print("更新成功 ✓")
    else:
        print(f"更新失败: {json.dumps(data, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    print("\n验证...")
    time.sleep(2)
    wf_new = get_workflow()
    new_cron_actual = wf_new.get("Trigger", {}).get("Cron", "")
    print(f"当前 cron: {new_cron_actual}")
    if new_cron_actual == cron_expr:
        print("验证通过 ✓")
    else:
        print("⚠ 可能需要等待生效")


def main():
    parser = argparse.ArgumentParser(description="DataWorks 工作流调度时间管理")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("get", help="查看当前调度配置")

    p_set = sub.add_parser("set", help="修改调度时间")
    p_set.add_argument("cron", nargs="?", default=CRON_EXPR,
                        help=f"cron 表达式（默认: {CRON_EXPR}）")
    p_set.add_argument("--hour", type=int, help="小时 (0-23)")
    p_set.add_argument("--minute", type=int, help="分钟 (0-59)")

    args = parser.parse_args()

    if args.command == "get":
        show_schedule()
    elif args.command == "set":
        if args.hour is not None or args.minute is not None:
            h = args.hour if args.hour is not None else 0
            m = args.minute if args.minute is not None else 0
            cron_expr = f"00 {m:02d} {h:02d} * * ?"
        else:
            cron_expr = args.cron
        update_schedule(cron_expr)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
