#!/usr/bin/env python3
"""Check PostgreSQL dimension table push status and freshness."""

import os
import sys
from datetime import datetime, timedelta

import psycopg2
from dotenv import load_dotenv

load_dotenv()

PG_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": os.environ.get("DB_PORT", "5432"),
    "database": "sync_dim",
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
}

TABLES = [
    ("dim_xhs_task_group_df", "Task group"),
    ("dim_xhs_project_df", "Project"),
    ("dim_xhs_ad_product_df", "Ad product"),
    ("dim_xhs_note_df", "Note"),
    ("brg_xhs_note_project_df", "Note-project bridge"),
    ("dim_xhs_creativity_df", "Creative"),
    ("dim_xhs_keyword_df", "Keyword"),
    ("dim_xhs_target_df", "Target"),
    ("dim_xhs_audience_segment_df", "Audience segment"),
    ("dim_xhs_advertiser_df", "Advertiser"),
]


def check_table_exists(cur, table_name):
    """Check if table exists in database."""
    cur.execute(
        "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)",
        (table_name,),
    )
    return cur.fetchone()[0]


def query_t1_status(cur, table_name, t1):
    """Query T-1 partition row count. Try both YYYY-MM-DD and YYYYMMDD formats."""
    if not check_table_exists(cur, table_name):
        return "NOT_FOUND", 0
    try:
        t1_dash = f"{t1[:4]}-{t1[4:6]}-{t1[6:]}"
        cur.execute(
            f"SELECT COUNT(*) FROM {table_name} WHERE dt IN (%s, %s)",
            (t1, t1_dash),
        )
        rows = cur.fetchone()[0]
        return "✅" if rows > 0 else "❌", rows
    except Exception as e:
        return "⚠️", 0


def main():
    now = datetime.now()
    t1 = (now - timedelta(days=1)).strftime("%Y%m%d")

    print(f"\n=== Dim Push Status ({now.strftime('%Y-%m-%d %H:%M')}) ===")
    print(f"T-1: {t1}\n")

    try:
        conn = psycopg2.connect(**PG_CONFIG, connect_timeout=10)
        conn.set_session(readonly=True)
        cur = conn.cursor()
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    header = f"| {'Table':<35} | {'T-1 Rows':>8} | {'Status':>3} |"
    sep = f"|{'-'*37}|{'-'*10}|{'-'*5}|"
    print(header)
    print(sep)

    ok_count = 0
    for table_name, desc in TABLES:
        status, rows = query_t1_status(cur, table_name, t1)
        if status == "✅":
            ok_count += 1
        print(f"| {table_name:<35} | {rows:>8,} | {status:>1} |")

    print(sep)
    print(f"\nSummary: {ok_count}/{len(TABLES)} pushed (T-1 = {t1})")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
