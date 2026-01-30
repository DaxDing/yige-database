#!/usr/bin/env python3
"""
Feishu Bitable API Client

Operates Feishu Bitable records: list, get, create, update, delete.

Usage:
    bitable.py list <app_token> <table_id> [--limit N] [--filter JSON]
    bitable.py get <app_token> <table_id> <record_id>
    bitable.py create <app_token> <table_id> --fields JSON
    bitable.py batch-create <app_token> <table_id> --file FILE
    bitable.py update <app_token> <table_id> <record_id> --fields JSON
    bitable.py delete <app_token> <table_id> <record_id>

Environment:
    FEISHU_USER_ACCESS_TOKEN - User access token (priority)
    FEISHU_APP_ID            - Application ID (fallback)
    FEISHU_APP_SECRET        - Application Secret (fallback)
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

BASE_URL = "https://open.feishu.cn/open-apis"


def get_access_token():
    """Get access token. Prefers user token, falls back to tenant token."""
    # Priority: user_access_token > tenant_access_token
    user_token = os.environ.get("FEISHU_USER_ACCESS_TOKEN")
    if user_token:
        return user_token

    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")

    if not app_id or not app_secret:
        print("Error: FEISHU_USER_ACCESS_TOKEN or FEISHU_APP_ID+SECRET required", file=sys.stderr)
        sys.exit(1)

    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.load(resp)
            if result.get("code") != 0:
                print(f"Error: {result.get('msg')}", file=sys.stderr)
                sys.exit(1)
            return result["tenant_access_token"]
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)


def api_request(method, endpoint, token, data=None, params=None):
    """Make API request to Feishu."""
    url = f"{BASE_URL}{endpoint}"

    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        if query:
            url = f"{url}?{query}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            error_json = json.loads(error_body)
            print(f"API Error: {error_json.get('msg', error_body)}", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"HTTP Error: {e.code} {error_body}", file=sys.stderr)
        sys.exit(1)


def list_records(app_token, table_id, token, limit=20, page_token=None, filter_str=None):
    """List records in a table."""
    params = {"page_size": limit}
    if page_token:
        params["page_token"] = page_token
    if filter_str:
        params["filter"] = filter_str

    endpoint = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    result = api_request("GET", endpoint, token, params=params)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", {})
    output = {
        "total": data.get("total", 0),
        "has_more": data.get("has_more", False),
        "page_token": data.get("page_token"),
        "records": [
            {
                "record_id": r.get("record_id"),
                "fields": r.get("fields", {})
            }
            for r in data.get("items", [])
        ]
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def get_record(app_token, table_id, record_id, token):
    """Get a single record."""
    endpoint = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    result = api_request("GET", endpoint, token)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    record = result.get("data", {}).get("record", {})
    output = {
        "record_id": record.get("record_id"),
        "fields": record.get("fields", {})
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def create_record(app_token, table_id, fields, token):
    """Create a single record."""
    endpoint = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    result = api_request("POST", endpoint, token, data={"fields": fields})

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    record = result.get("data", {}).get("record", {})
    output = {
        "record_id": record.get("record_id"),
        "fields": record.get("fields", {})
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def batch_create_records(app_token, table_id, records, token):
    """Batch create records (max 1000 per request)."""
    endpoint = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"

    # Split into chunks of 500
    chunk_size = 500
    all_results = []

    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        data = {"records": [{"fields": r} for r in chunk]}
        result = api_request("POST", endpoint, token, data=data)

        if result.get("code") != 0:
            print(f"Error: {result.get('msg')}", file=sys.stderr)
            sys.exit(1)

        items = result.get("data", {}).get("records", [])
        all_results.extend([
            {"record_id": r.get("record_id"), "fields": r.get("fields", {})}
            for r in items
        ])

    output = {"created": len(all_results), "records": all_results}
    print(json.dumps(output, ensure_ascii=False, indent=2))


def update_record(app_token, table_id, record_id, fields, token):
    """Update a single record."""
    endpoint = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    result = api_request("PUT", endpoint, token, data={"fields": fields})

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    record = result.get("data", {}).get("record", {})
    output = {
        "record_id": record.get("record_id"),
        "fields": record.get("fields", {})
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def delete_record(app_token, table_id, record_id, token):
    """Delete a single record."""
    endpoint = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    result = api_request("DELETE", endpoint, token)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"deleted": True, "record_id": record_id}))


def get_wiki_app_token(wiki_token, token):
    """Get Bitable app_token from wiki page."""
    endpoint = f"/wiki/v2/spaces/get_node?token={wiki_token}"
    result = api_request("GET", endpoint, token)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    node = result.get("data", {}).get("node", {})
    obj_token = node.get("obj_token")
    if not obj_token:
        print("Error: No obj_token found in wiki node", file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"app_token": obj_token, "title": node.get("title", "")}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Feishu Bitable API Client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    list_parser = subparsers.add_parser("list", help="List records")
    list_parser.add_argument("app_token", help="Bitable app token")
    list_parser.add_argument("table_id", help="Table ID")
    list_parser.add_argument("--limit", type=int, default=20, help="Max records")
    list_parser.add_argument("--page-token", help="Pagination token")
    list_parser.add_argument("--filter", dest="filter_str", help="Filter expression")

    # get
    get_parser = subparsers.add_parser("get", help="Get single record")
    get_parser.add_argument("app_token", help="Bitable app token")
    get_parser.add_argument("table_id", help="Table ID")
    get_parser.add_argument("record_id", help="Record ID")

    # create
    create_parser = subparsers.add_parser("create", help="Create record")
    create_parser.add_argument("app_token", help="Bitable app token")
    create_parser.add_argument("table_id", help="Table ID")
    create_parser.add_argument("--fields", required=True, help="Fields as JSON")

    # batch-create
    batch_parser = subparsers.add_parser("batch-create", help="Batch create records")
    batch_parser.add_argument("app_token", help="Bitable app token")
    batch_parser.add_argument("table_id", help="Table ID")
    batch_parser.add_argument("--file", required=True, help="JSON file with records")

    # update
    update_parser = subparsers.add_parser("update", help="Update record")
    update_parser.add_argument("app_token", help="Bitable app token")
    update_parser.add_argument("table_id", help="Table ID")
    update_parser.add_argument("record_id", help="Record ID")
    update_parser.add_argument("--fields", required=True, help="Fields as JSON")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete record")
    delete_parser.add_argument("app_token", help="Bitable app token")
    delete_parser.add_argument("table_id", help="Table ID")
    delete_parser.add_argument("record_id", help="Record ID")

    # wiki-token
    wiki_parser = subparsers.add_parser("wiki-token", help="Get app_token from wiki page")
    wiki_parser.add_argument("wiki_token", help="Wiki page token")

    args = parser.parse_args()
    token = get_access_token()

    if args.command == "list":
        list_records(args.app_token, args.table_id, token,
                     limit=args.limit, page_token=args.page_token,
                     filter_str=args.filter_str)
    elif args.command == "get":
        get_record(args.app_token, args.table_id, args.record_id, token)
    elif args.command == "create":
        fields = json.loads(args.fields)
        create_record(args.app_token, args.table_id, fields, token)
    elif args.command == "batch-create":
        with open(args.file, "r", encoding="utf-8") as f:
            records = json.load(f)
        batch_create_records(args.app_token, args.table_id, records, token)
    elif args.command == "update":
        fields = json.loads(args.fields)
        update_record(args.app_token, args.table_id, args.record_id, fields, token)
    elif args.command == "delete":
        delete_record(args.app_token, args.table_id, args.record_id, token)
    elif args.command == "wiki-token":
        get_wiki_app_token(args.wiki_token, token)


if __name__ == "__main__":
    main()
