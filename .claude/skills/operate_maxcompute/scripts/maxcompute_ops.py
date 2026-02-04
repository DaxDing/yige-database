#!/usr/bin/env python3
"""MaxCompute operations via PyODPS."""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from odps import ODPS


def get_odps(project: str, endpoint: str) -> ODPS:
    """Create ODPS connection."""
    load_dotenv()
    return ODPS(
        access_id=os.environ["ALIYUN_ACCESS_KEY_ID"],
        secret_access_key=os.environ["ALIYUN_ACCESS_KEY_SECRET"],
        project=project,
        endpoint=f"http://service.{endpoint}.maxcompute.aliyun.com/api",
    )


def list_tables(odps: ODPS) -> None:
    """List all tables in project."""
    tables = list(odps.list_tables())
    print(f"Tables ({len(tables)}):\n")
    for t in sorted(tables, key=lambda x: x.name):
        comment = t.comment or ""
        print(f"  {t.name:<50} {comment}")


def get_table(odps: ODPS, name: str) -> None:
    """Show table schema."""
    t = odps.get_table(name)
    print(f"Table: {t.name}")
    print(f"Comment: {t.comment or '-'}")
    print(f"Created: {t.creation_time}")
    print(f"\nColumns ({len(t.table_schema.columns)}):")
    for col in t.table_schema.columns:
        print(f"  {col.name:<30} {str(col.type):<15} {col.comment or ''}")
    if t.table_schema.partitions:
        print(f"\nPartitions ({len(t.table_schema.partitions)}):")
        for p in t.table_schema.partitions:
            print(f"  {p.name:<30} {str(p.type):<15} {p.comment or ''}")


def create_table(odps: ODPS, json_path: str) -> None:
    """Create table from JSON definition."""
    with open(json_path) as f:
        spec = json.load(f)

    columns = []
    partitions = []

    for field in spec["fields"]:
        col_def = f"`{field['name']}` {field['type']}"
        if field.get("nameCn"):
            col_def += f" COMMENT '{field['nameCn']}'"

        if field.get("key") == "PT":
            partitions.append(col_def)
        else:
            columns.append(col_def)

    sql = f"CREATE TABLE IF NOT EXISTS `{spec['name']}` (\n  "
    sql += ",\n  ".join(columns)
    sql += "\n)"

    if spec.get("nameCn"):
        sql += f"\nCOMMENT '{spec['nameCn']}'"

    if partitions:
        sql += f"\nPARTITIONED BY ({', '.join(partitions)})"

    sql += ";"

    print(f"Executing:\n{sql}\n")
    odps.execute_sql(sql)
    print(f"Created table: {spec['name']}")


def drop_table(odps: ODPS, name: str) -> None:
    """Drop a table."""
    odps.delete_table(name, if_exists=True)
    print(f"Dropped table: {name}")


def execute_sql(odps: ODPS, sql: str, hints: dict = None) -> None:
    """Execute SQL statement with optional hints."""
    print(f"Executing: {sql}\n")

    sql_lower = sql.strip().lower()
    if sql_lower.startswith("select"):
        with odps.execute_sql(sql, hints=hints).open_reader() as reader:
            for record in reader:
                print(dict(record))
    else:
        odps.execute_sql(sql, hints=hints)
        print("Executed successfully.")


def count_rows(odps: ODPS, name: str) -> None:
    """Count rows for a table or all tables. Enables fullscan hint."""
    hints = {"odps.sql.allow.fullscan": "true"}

    if name == "--all":
        tables = sorted(odps.list_tables(), key=lambda x: x.name)
        print(f"{'Table':<55} {'Partitions':>10} {'Rows':>10}")
        print("-" * 77)
        for t in tables:
            part_count = len(list(t.partitions))
            sql = f"SELECT COUNT(*) AS cnt FROM {t.name}"
            try:
                with odps.execute_sql(sql, hints=hints).open_reader() as reader:
                    row_count = next(iter(reader))[0]
            except Exception as e:
                row_count = f"ERROR"
            print(f"  {t.name:<53} {part_count:>10} {row_count:>10}")
    else:
        t = odps.get_table(name)
        part_count = len(list(t.partitions))
        sql = f"SELECT COUNT(*) AS cnt FROM {name}"
        with odps.execute_sql(sql, hints=hints).open_reader() as reader:
            row_count = next(iter(reader))[0]
        print(f"Table: {name}")
        print(f"Partitions: {part_count}")
        print(f"Rows: {row_count}")


def list_partitions(odps: ODPS, name: str) -> None:
    """List table partitions."""
    t = odps.get_table(name)
    partitions = list(t.partitions)
    print(f"Partitions for {name} ({len(partitions)}):\n")
    for p in sorted(partitions, key=lambda x: str(x.partition_spec)):
        print(f"  {p.partition_spec}")


def add_partition(odps: ODPS, name: str, partition_spec: str) -> None:
    """Add partition to table."""
    t = odps.get_table(name)
    t.create_partition(partition_spec, if_not_exists=True)
    print(f"Added partition {partition_spec} to {name}")


def main():
    parser = argparse.ArgumentParser(description="MaxCompute operations")
    parser.add_argument("-p", "--project", default="df_ch_530486", help="Project name")
    parser.add_argument("-e", "--endpoint", default="cn-hangzhou", help="Endpoint region")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-tables", help="List all tables")

    p = subparsers.add_parser("get-table", help="Show table schema")
    p.add_argument("name", help="Table name")

    p = subparsers.add_parser("create-table", help="Create table from JSON")
    p.add_argument("json_path", help="Path to JSON definition")

    p = subparsers.add_parser("drop-table", help="Drop a table")
    p.add_argument("name", help="Table name")

    p = subparsers.add_parser("execute-sql", help="Execute SQL")
    p.add_argument("sql", help="SQL statement")
    p.add_argument("--fullscan", action="store_true", help="Allow full table scan")

    p = subparsers.add_parser("count-rows", help="Count table rows")
    p.add_argument("name", nargs="?", default=None, help="Table name")
    p.add_argument("--all", dest="all_tables", action="store_true", help="Count all tables")

    p = subparsers.add_parser("list-partitions", help="List partitions")
    p.add_argument("name", help="Table name")

    p = subparsers.add_parser("add-partition", help="Add partition")
    p.add_argument("name", help="Table name")
    p.add_argument("partition_spec", help="Partition spec (e.g., ds=20260110)")

    args = parser.parse_args()
    odps = get_odps(args.project, args.endpoint)

    if args.command == "list-tables":
        list_tables(odps)
    elif args.command == "get-table":
        get_table(odps, args.name)
    elif args.command == "create-table":
        create_table(odps, args.json_path)
    elif args.command == "drop-table":
        drop_table(odps, args.name)
    elif args.command == "execute-sql":
        hints = {"odps.sql.allow.fullscan": "true"} if args.fullscan else None
        execute_sql(odps, args.sql, hints=hints)
    elif args.command == "count-rows":
        name = "--all" if args.all_tables else args.name
        if not name:
            parser.error("count-rows requires a table name or --all")
        count_rows(odps, name)
    elif args.command == "list-partitions":
        list_partitions(odps, args.name)
    elif args.command == "add-partition":
        add_partition(odps, args.name, args.partition_spec)


if __name__ == "__main__":
    main()
