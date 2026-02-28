#!/usr/bin/env python3
"""DataWorks 工作流节点管理 - 列出、查看、部署节点脚本"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ID = "530486"
REGION = "cn-hangzhou"
CLI_SCRIPT = str(Path(__file__).parent / "invoke_dataworks.py")

NODE_TYPE_MAP = {
    "DIDE_SHELL": "Shell",
    "CONTROLLER_ASSIGNMENT": "赋值",
    "CONTROLLER_TRAVERSE": "遍历",
    "CONTROLLER_TRAVERSE_START": "遍历开始",
    "CONTROLLER_TRAVERSE_END": "遍历结束",
    "ODPS_SQL": "ODPS SQL",
    "PYODPS": "PyODPS",
}


def call_api(api, **params):
    """调用 DataWorks API"""
    cmd = ["python3", CLI_SCRIPT, "dataworks-public", api,
           "--ProjectId", PROJECT_ID, "--region", REGION]
    for k, v in params.items():
        cmd.extend([f"--{k}", str(v)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"API 错误: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def list_nodes(workflow_name):
    """列出工作流中的节点"""
    data = call_api("ListNodes")
    nodes = data.get("PagingInfo", {}).get("Nodes", [])
    matched = [n for n in nodes
                if n.get("Script", {}).get("Path", "").startswith(f"{workflow_name}/")]

    if not matched:
        print(f"未找到工作流: {workflow_name}")
        return

    print(f"\n{workflow_name} 工作流节点:\n")
    print(f"  {'名称':<35s} {'类型':<12s} {'节点ID'}")
    print(f"  {'─'*35} {'─'*12} {'─'*22}")
    for n in sorted(matched, key=lambda x: x["Script"]["Path"]):
        name = n["Name"]
        cmd = n.get("Script", {}).get("Runtime", {}).get("Command", "")
        type_cn = NODE_TYPE_MAP.get(cmd, cmd)
        nid = n["Id"]
        print(f"  {name:<35s} {type_cn:<12s} {nid}")


def find_node_id(workflow_name, node_name):
    """通过工作流名+节点名找到节点 ID"""
    data = call_api("ListNodes")
    nodes = data.get("PagingInfo", {}).get("Nodes", [])
    path = f"{workflow_name}/{node_name}"
    for n in nodes:
        if n.get("Script", {}).get("Path", "") == path:
            return n["Id"]
    print(f"未找到节点: {path}", file=sys.stderr)
    sys.exit(1)


def get_node_script(workflow_name, node_name):
    """查看节点脚本内容"""
    node_id = find_node_id(workflow_name, node_name)
    data = call_api("GetNode", Id=node_id)
    spec = json.loads(data["Node"]["Spec"])

    for node in spec["spec"]["workflows"][0]["nodes"]:
        if node["name"] == node_name:
            content = node.get("script", {}).get("content", "")
            print(content)
            return

    print(f"Spec 中未找到节点: {node_name}", file=sys.stderr)
    sys.exit(1)


def deploy_node(workflow_name, node_name, local_file):
    """将本地文件部署到 DataWorks 节点"""
    local_path = Path(local_file)
    if not local_path.exists():
        print(f"文件不存在: {local_file}", file=sys.stderr)
        sys.exit(1)

    new_content = local_path.read_text()
    node_id = find_node_id(workflow_name, node_name)

    print(f">>> 部署 {workflow_name}/{node_name}")
    print(f">>> 节点 ID: {node_id}")
    print(f">>> 源文件: {local_file}")
    print(f">>> 脚本大小: {len(new_content)} chars")

    # 获取当前 Spec
    data = call_api("GetNode", Id=node_id)
    spec = json.loads(data["Node"]["Spec"])

    # 替换脚本内容
    updated = False
    for node in spec["spec"]["workflows"][0]["nodes"]:
        if node["name"] == node_name:
            node["script"]["content"] = new_content
            updated = True
            break

    if not updated:
        print(f"Spec 中未找到节点: {node_name}", file=sys.stderr)
        sys.exit(1)

    # 写入临时文件（避免命令行转义问题）
    spec_str = json.dumps(spec, ensure_ascii=False)
    tmp_file = Path("/tmp/dw_deploy_spec.json")
    tmp_file.write_text(spec_str)

    # 调用 UpdateNode
    cmd = ["python3", CLI_SCRIPT, "dataworks-public", "UpdateNode",
           "--Id", str(node_id), "--ProjectId", PROJECT_ID,
           "--Spec", spec_str, "--region", REGION]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"更新失败: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    resp = json.loads(result.stdout)
    if resp.get("Success"):
        print(">>> 部署成功 ✓")
    else:
        print(f">>> 部署失败: {resp}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="DataWorks 节点管理")
    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="列出工作流节点")
    p_list.add_argument("workflow", help="工作流名称")

    # get
    p_get = sub.add_parser("get", help="查看节点脚本")
    p_get.add_argument("workflow", help="工作流名称")
    p_get.add_argument("node", help="节点名称")

    # deploy
    p_deploy = sub.add_parser("deploy", help="部署本地脚本到节点")
    p_deploy.add_argument("workflow", help="工作流名称")
    p_deploy.add_argument("node", help="节点名称")
    p_deploy.add_argument("file", help="本地脚本文件路径")

    args = parser.parse_args()

    if args.command == "list":
        list_nodes(args.workflow)
    elif args.command == "get":
        get_node_script(args.workflow, args.node)
    elif args.command == "deploy":
        deploy_node(args.workflow, args.node, args.file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
