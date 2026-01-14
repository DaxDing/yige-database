#!/usr/bin/env python3
"""
MaxCompute Operations
Provides table management for Alibaba Cloud MaxCompute via PyODPS.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any


class MaxComputeError(Exception):
    """Base exception for MaxCompute operations"""
    pass


class MaxComputeOps:
    """MaxCompute table management operations"""

    DEFAULT_ENDPOINT = "http://service.cn-hangzhou.maxcompute.aliyun.com/api"
    DEFAULT_LIFECYCLE = 90

    def __init__(self, project: str, env_file: str = ".env", endpoint: str = None):
        self.project = project
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self.env_file = Path(env_file)
        self._odps = None
        self._load_credentials()

    def _load_credentials(self):
        """Load credentials from .env file"""
        if not self.env_file.exists():
            raise MaxComputeError(f".env file not found: {self.env_file}")

        credentials = {}
        with open(self.env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    credentials[key.strip()] = value.strip().strip('"').strip("'")

        self.access_id = credentials.get('ALIYUN_ACCESS_KEY_ID')
        self.access_key = credentials.get('ALIYUN_ACCESS_KEY_SECRET')

        if not self.access_id or not self.access_key:
            raise MaxComputeError("Missing ALIYUN_ACCESS_KEY_ID or ALIYUN_ACCESS_KEY_SECRET in .env")

    @property
    def odps(self):
        """Lazy load ODPS connection"""
        if self._odps is None:
            try:
                from odps import ODPS
                self._odps = ODPS(
                    self.access_id,
                    self.access_key,
                    project=self.project,
                    endpoint=self.endpoint
                )
            except ImportError:
                raise MaxComputeError("pyodps not installed. Run: pip install pyodps")
        return self._odps

    def list_tables(self) -> List[Dict[str, Any]]:
        """List all tables in the project"""
        tables = []
        for t in self.odps.list_tables():
            tables.append({
                "name": t.name,
                "comment": t.comment,
                "owner": t.owner,
                "creation_time": str(t.creation_time) if t.creation_time else None
            })
        return tables

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed table information"""
        t = self.odps.get_table(table_name)
        return {
            "name": t.name,
            "comment": t.comment,
            "owner": t.owner,
            "creation_time": str(t.creation_time) if t.creation_time else None,
            "columns": [
                {"name": c.name, "type": str(c.type), "comment": c.comment}
                for c in t.table_schema.columns
            ],
            "partitions": [
                {"name": p.name, "type": str(p.type), "comment": p.comment}
                for p in t.table_schema.partitions
            ],
            "lifecycle": t.lifecycle
        }

    def execute_sql(self, sql: str, hints: Dict[str, str] = None) -> str:
        """Execute SQL statement"""
        default_hints = {
            "odps.sql.type.system.odps2": "true"
        }
        if hints:
            default_hints.update(hints)

        instance = self.odps.execute_sql(sql, hints=default_hints)
        instance.wait_for_success()
        return instance.id

    def create_table_from_json(self, json_path: str) -> Dict[str, Any]:
        """Create table from JSON definition file"""
        with open(json_path, 'r') as f:
            spec = json.load(f)

        table_name = spec['name']
        comment = spec.get('nameCn', spec.get('desc', ''))
        lifecycle = self.DEFAULT_LIFECYCLE

        # Build columns
        columns = []
        partition_col = None

        for field in spec.get('fields', []):
            col_name = field['name']
            col_type = self._map_type(field['type'])
            col_comment = field.get('nameCn', field.get('desc', ''))

            if field.get('key') == 'PT':
                partition_col = {"name": col_name, "type": col_type, "comment": col_comment}
            else:
                # Escape reserved words
                if col_name.lower() in ('like', 'comment', 'order', 'group', 'by'):
                    col_name = f"`{col_name}`"
                columns.append(f"  {col_name} {col_type} COMMENT '{col_comment}'")

        # Build DDL
        ddl_parts = [f"CREATE TABLE IF NOT EXISTS {table_name} ("]
        ddl_parts.append(",\n".join(columns))
        ddl_parts.append(")")
        ddl_parts.append(f"COMMENT '{comment}'")

        if partition_col:
            ddl_parts.append(f"PARTITIONED BY ({partition_col['name']} {partition_col['type']} COMMENT '{partition_col['comment']}')")

        ddl_parts.append(f"LIFECYCLE {lifecycle}")

        ddl = "\n".join(ddl_parts)

        # Execute
        self.execute_sql(ddl)

        return {
            "table_name": table_name,
            "ddl": ddl,
            "status": "created"
        }

    def drop_table(self, table_name: str, if_exists: bool = True) -> Dict[str, Any]:
        """Drop a table"""
        exists_clause = "IF EXISTS " if if_exists else ""
        sql = f"DROP TABLE {exists_clause}{table_name}"
        self.execute_sql(sql)
        return {"table_name": table_name, "status": "dropped"}

    def _map_type(self, type_str: str) -> str:
        """Map JSON type to MaxCompute type"""
        type_upper = type_str.upper()
        type_map = {
            "STRING": "STRING",
            "INT": "INT",
            "BIGINT": "BIGINT",
            "DECIMAL": "DECIMAL(18,2)",
            "DATETIME": "DATETIME",
            "TIMESTAMP": "TIMESTAMP",
            "BOOLEAN": "BOOLEAN",
            "DOUBLE": "DOUBLE",
            "FLOAT": "FLOAT"
        }
        return type_map.get(type_upper, type_upper)

    def list_partitions(self, table_name: str) -> List[str]:
        """List partitions of a table"""
        t = self.odps.get_table(table_name)
        return [str(p.name) for p in t.partitions]

    def add_partition(self, table_name: str, partition_spec: str) -> Dict[str, Any]:
        """Add partition to table (e.g., 'ds=20260108')"""
        sql = f"ALTER TABLE {table_name} ADD IF NOT EXISTS PARTITION ({partition_spec})"
        self.execute_sql(sql)
        return {"table_name": table_name, "partition": partition_spec, "status": "added"}

    def drop_partition(self, table_name: str, partition_spec: str) -> Dict[str, Any]:
        """Drop partition from table"""
        sql = f"ALTER TABLE {table_name} DROP IF EXISTS PARTITION ({partition_spec})"
        self.execute_sql(sql)
        return {"table_name": table_name, "partition": partition_spec, "status": "dropped"}


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="MaxCompute Table Operations")
    parser.add_argument("--project", "-p", default="df_ch_530486", help="MaxCompute project name")
    parser.add_argument("--endpoint", "-e", help="MaxCompute endpoint")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # list-tables
    subparsers.add_parser("list-tables", help="List all tables")

    # get-table
    get_parser = subparsers.add_parser("get-table", help="Get table info")
    get_parser.add_argument("table", help="Table name")

    # create-table
    create_parser = subparsers.add_parser("create-table", help="Create table from JSON")
    create_parser.add_argument("json_file", help="JSON definition file path")

    # drop-table
    drop_parser = subparsers.add_parser("drop-table", help="Drop table")
    drop_parser.add_argument("table", help="Table name")

    # execute-sql
    sql_parser = subparsers.add_parser("execute-sql", help="Execute SQL")
    sql_parser.add_argument("sql", help="SQL statement")

    # list-partitions
    part_list_parser = subparsers.add_parser("list-partitions", help="List partitions")
    part_list_parser.add_argument("table", help="Table name")

    # add-partition
    part_add_parser = subparsers.add_parser("add-partition", help="Add partition")
    part_add_parser.add_argument("table", help="Table name")
    part_add_parser.add_argument("partition", help="Partition spec (e.g., ds=20260108)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        ops = MaxComputeOps(project=args.project, endpoint=args.endpoint)

        if args.command == "list-tables":
            result = ops.list_tables()
        elif args.command == "get-table":
            result = ops.get_table_info(args.table)
        elif args.command == "create-table":
            result = ops.create_table_from_json(args.json_file)
        elif args.command == "drop-table":
            result = ops.drop_table(args.table)
        elif args.command == "execute-sql":
            instance_id = ops.execute_sql(args.sql)
            result = {"instance_id": instance_id, "status": "success"}
        elif args.command == "list-partitions":
            result = ops.list_partitions(args.table)
        elif args.command == "add-partition":
            result = ops.add_partition(args.table, args.partition)
        else:
            parser.print_help()
            sys.exit(1)

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except MaxComputeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
