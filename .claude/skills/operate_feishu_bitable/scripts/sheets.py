#!/usr/bin/env python3
"""
Feishu Sheets API Client

Operates Feishu Spreadsheets: read, write, append, update, delete-rows, info.

Usage:
    sheets.py read <spreadsheet_token> <sheet_id> [--range RANGE]
    sheets.py write <spreadsheet_token> <sheet_id> --range RANGE --values JSON
    sheets.py append <spreadsheet_token> <sheet_id> --values JSON
    sheets.py update <spreadsheet_token> <sheet_id> --range RANGE --values JSON
    sheets.py delete-rows <spreadsheet_token> <sheet_id> --start ROW --count N
    sheets.py info <spreadsheet_token>

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


def read_range(spreadsheet_token, sheet_id, token, range_str=None):
    """Read cell values from a range."""
    if range_str:
        full_range = f"{sheet_id}!{range_str}"
    else:
        full_range = sheet_id

    endpoint = f"/sheets/v2/spreadsheets/{spreadsheet_token}/values/{full_range}"
    result = api_request("GET", endpoint, token)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", {}).get("valueRange", {})
    output = {
        "range": data.get("range"),
        "values": data.get("values", [])
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def write_range(spreadsheet_token, sheet_id, range_str, values, token):
    """Write values to a range (overwrites existing)."""
    full_range = f"{sheet_id}!{range_str}"
    endpoint = f"/sheets/v2/spreadsheets/{spreadsheet_token}/values"

    data = {
        "valueRange": {
            "range": full_range,
            "values": values
        }
    }
    result = api_request("PUT", endpoint, token, data=data)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    resp_data = result.get("data", {})
    output = {
        "spreadsheet_token": resp_data.get("spreadsheetToken"),
        "updated_range": resp_data.get("updatedRange"),
        "updated_rows": resp_data.get("updatedRows"),
        "updated_columns": resp_data.get("updatedColumns"),
        "updated_cells": resp_data.get("updatedCells")
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def append_rows(spreadsheet_token, sheet_id, values, token):
    """Append rows to the end of the sheet."""
    endpoint = f"/sheets/v2/spreadsheets/{spreadsheet_token}/values_append"
    params = {"insertDataOption": "INSERT_ROWS"}

    data = {
        "valueRange": {
            "range": sheet_id,
            "values": values
        }
    }
    result = api_request("POST", endpoint, token, data=data, params=params)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    resp_data = result.get("data", {}).get("tableRange", "")
    output = {
        "appended": True,
        "table_range": resp_data,
        "rows_appended": len(values)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def update_range(spreadsheet_token, sheet_id, range_str, values, token):
    """Update cells in a range."""
    full_range = f"{sheet_id}!{range_str}"
    endpoint = f"/sheets/v2/spreadsheets/{spreadsheet_token}/values"

    data = {
        "valueRange": {
            "range": full_range,
            "values": values
        }
    }
    result = api_request("PUT", endpoint, token, data=data)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    resp_data = result.get("data", {})
    output = {
        "updated": True,
        "range": resp_data.get("updatedRange"),
        "cells": resp_data.get("updatedCells")
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def delete_rows(spreadsheet_token, sheet_id, start_row, count, token):
    """Delete rows from the sheet."""
    endpoint = f"/sheets/v2/spreadsheets/{spreadsheet_token}/dimension_range"

    data = {
        "dimension": {
            "sheetId": sheet_id,
            "majorDimension": "ROWS",
            "startIndex": start_row,
            "endIndex": start_row + count
        }
    }
    result = api_request("DELETE", endpoint, token, data=data)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    output = {
        "deleted": True,
        "start_row": start_row,
        "count": count
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def get_info(spreadsheet_token, token):
    """Get spreadsheet metadata."""
    endpoint = f"/sheets/v3/spreadsheets/{spreadsheet_token}"
    result = api_request("GET", endpoint, token)

    if result.get("code") != 0:
        print(f"Error: {result.get('msg')}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", {}).get("spreadsheet", {})
    output = {
        "title": data.get("title"),
        "owner_id": data.get("owner_id"),
        "url": data.get("url"),
        "sheets": []
    }

    # Get sheets list
    sheets_endpoint = f"/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/query"
    sheets_result = api_request("GET", sheets_endpoint, token)

    if sheets_result.get("code") == 0:
        sheets = sheets_result.get("data", {}).get("sheets", [])
        output["sheets"] = [
            {
                "sheet_id": s.get("sheet_id"),
                "title": s.get("title"),
                "index": s.get("index"),
                "row_count": s.get("grid_properties", {}).get("row_count"),
                "column_count": s.get("grid_properties", {}).get("column_count")
            }
            for s in sheets
        ]

    print(json.dumps(output, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Feishu Sheets API Client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # read
    read_parser = subparsers.add_parser("read", help="Read cell values")
    read_parser.add_argument("spreadsheet_token", help="Spreadsheet token")
    read_parser.add_argument("sheet_id", help="Sheet ID")
    read_parser.add_argument("--range", dest="range_str", help="Range (e.g., A1:D10)")

    # write
    write_parser = subparsers.add_parser("write", help="Write values to range")
    write_parser.add_argument("spreadsheet_token", help="Spreadsheet token")
    write_parser.add_argument("sheet_id", help="Sheet ID")
    write_parser.add_argument("--range", required=True, dest="range_str", help="Start range")
    write_parser.add_argument("--values", required=True, help="2D array as JSON")

    # append
    append_parser = subparsers.add_parser("append", help="Append rows")
    append_parser.add_argument("spreadsheet_token", help="Spreadsheet token")
    append_parser.add_argument("sheet_id", help="Sheet ID")
    append_parser.add_argument("--values", required=True, help="2D array as JSON")

    # update
    update_parser = subparsers.add_parser("update", help="Update cells")
    update_parser.add_argument("spreadsheet_token", help="Spreadsheet token")
    update_parser.add_argument("sheet_id", help="Sheet ID")
    update_parser.add_argument("--range", required=True, dest="range_str", help="Range")
    update_parser.add_argument("--values", required=True, help="2D array as JSON")

    # delete-rows
    delete_parser = subparsers.add_parser("delete-rows", help="Delete rows")
    delete_parser.add_argument("spreadsheet_token", help="Spreadsheet token")
    delete_parser.add_argument("sheet_id", help="Sheet ID")
    delete_parser.add_argument("--start", type=int, required=True, help="Start row (1-based)")
    delete_parser.add_argument("--count", type=int, required=True, help="Number of rows")

    # info
    info_parser = subparsers.add_parser("info", help="Get spreadsheet info")
    info_parser.add_argument("spreadsheet_token", help="Spreadsheet token")

    args = parser.parse_args()
    token = get_access_token()

    if args.command == "read":
        read_range(args.spreadsheet_token, args.sheet_id, token, args.range_str)
    elif args.command == "write":
        values = json.loads(args.values)
        write_range(args.spreadsheet_token, args.sheet_id, args.range_str, values, token)
    elif args.command == "append":
        values = json.loads(args.values)
        append_rows(args.spreadsheet_token, args.sheet_id, values, token)
    elif args.command == "update":
        values = json.loads(args.values)
        update_range(args.spreadsheet_token, args.sheet_id, args.range_str, values, token)
    elif args.command == "delete-rows":
        delete_rows(args.spreadsheet_token, args.sheet_id, args.start, args.count, token)
    elif args.command == "info":
        get_info(args.spreadsheet_token, token)


if __name__ == "__main__":
    main()
