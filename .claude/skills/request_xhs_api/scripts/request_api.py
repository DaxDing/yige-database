#!/usr/bin/env python3
"""
小红书 API 请求工具

根据 OpenAPI 规范自动构造请求，支持分页。

Usage:
    request_api.py <spec_file> [--params KEY=VALUE ...] [--token TOKEN] [--all-pages] [--output FILE]

Examples:
    # 聚光创意离线报表
    request_api.py specs/jg/xhs_jg_report_offline_creativity_v1.openapi.yml \
        --token $TOKEN --params advertiser_id=7152346 start_date=2026-03-01 end_date=2026-03-08

    # 蒲公英投后数据（全量分页）
    request_api.py specs/pgy/xhs_pgy_note_post_invest_v1.openapi.yml \
        --token $TOKEN --params user_id=xxx start_time=2026-03-01 end_time=2026-03-08 --all-pages

    # 输出到文件
    request_api.py specs/jg/xhs_jg_note_list_v1.openapi.yml \
        --token $TOKEN --params advertiser_id=7152346 --output out.json
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error

import yaml


def load_spec(spec_path):
    """Load and parse OpenAPI spec."""
    with open(spec_path) as f:
        return yaml.safe_load(f)


def extract_api_info(spec):
    """Extract URL, method, pagination config from spec."""
    server = spec["servers"][0]["url"]
    path = list(spec["paths"].keys())[0]
    method_key = list(spec["paths"][path].keys())[0]
    operation = spec["paths"][path][method_key]

    url = server + path
    method = method_key.upper()

    # Extract pagination config
    pagination = operation.get("x-pagination")

    # Extract default body from example or schema defaults
    body_schema = {}
    req_body = operation.get("requestBody", {})
    content = req_body.get("content", {}).get("application/json", {})

    example = content.get("example", {})
    schema_props = content.get("schema", {}).get("properties", {})

    # Build defaults from schema
    defaults = {}
    for key, prop in schema_props.items():
        if "default" in prop:
            defaults[key] = prop["default"]

    # Example overrides schema defaults
    defaults.update(example)

    return {
        "url": url,
        "method": method,
        "defaults": defaults,
        "pagination": pagination,
        "title": spec.get("info", {}).get("title", ""),
        "operation_id": operation.get("operationId", ""),
    }


def parse_value(v):
    """Parse string value to appropriate type."""
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    # Try JSON (for arrays/objects)
    if v.startswith("[") or v.startswith("{"):
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            pass
    return v


def make_request(url, method, body, token):
    """Make HTTP request and return parsed response."""
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Token": token,
    }

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def get_nested(obj, path):
    """Get nested value by dot path like 'data.data_list'."""
    for key in path.split("."):
        if isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return None
    return obj


def paginate(url, method, body, token, pagination):
    """Fetch all pages and return combined results."""
    page_param = pagination["page_param"]
    size_param = pagination["size_param"]
    list_path = pagination["list_path"]
    start_page = pagination.get("start_page", 1)
    page_size = pagination.get("page_size", 20)

    body[size_param] = page_size
    body[page_param] = start_page

    all_items = []
    page = start_page

    while True:
        body[page_param] = page
        print(f"  Page {page}...", file=sys.stderr, end="", flush=True)

        result = make_request(url, method, body, token)

        if result.get("code") not in (0, None):
            print(f"\n  API Error: {result.get('msg', result)}", file=sys.stderr)
            break

        items = get_nested(result, list_path)
        if not items:
            print(" empty", file=sys.stderr)
            break

        all_items.extend(items)
        print(f" +{len(items)} (total: {len(all_items)})", file=sys.stderr)

        if len(items) < page_size:
            break

        page += 1
        time.sleep(0.3)

    return all_items


def main():
    parser = argparse.ArgumentParser(description="小红书 API 请求工具")
    parser.add_argument("spec", help="OpenAPI spec file path")
    parser.add_argument("--token", required=True, help="Access token")
    parser.add_argument("--params", nargs="*", default=[], help="KEY=VALUE pairs")
    parser.add_argument("--all-pages", action="store_true", help="Fetch all pages")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()

    spec = load_spec(args.spec)
    api = extract_api_info(spec)

    # Build request body: defaults + user params
    body = dict(api["defaults"])
    for param in args.params:
        if "=" not in param:
            print(f"Invalid param: {param} (expected KEY=VALUE)", file=sys.stderr)
            sys.exit(1)
        key, val = param.split("=", 1)
        body[key] = parse_value(val)

    print(f"API: {api['title']} ({api['operation_id']})", file=sys.stderr)
    print(f"URL: {api['url']}", file=sys.stderr)
    print(f"Body: {json.dumps(body, ensure_ascii=False)}", file=sys.stderr)

    if args.all_pages and api["pagination"]:
        result = paginate(api["url"], api["method"], body, args.token, api["pagination"])
        output = {"total": len(result), "items": result}
    else:
        result = make_request(api["url"], api["method"], body, args.token)
        output = result

    # Output
    out_str = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out_str)
        print(f"Saved: {args.output} ({len(out_str)} bytes)", file=sys.stderr)
    else:
        print(out_str)


if __name__ == "__main__":
    main()
