#!/usr/bin/env python3
"""Sync grass alliance conversion data: PG -> MC ODS -> DWD (bycontent + bytask)."""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from odps import ODPS

load_dotenv()

# --- Config ---

PG_CONFIG = {
    "host": "pgm-bp17nt187ku2460hho.rwlb.rds.aliyuncs.com",
    "port": "5432",
    "database": "xhs_conversion",
    "user": "crawler",
    "password": "F3UnAU3WPj69PY",
}

MC_PROJECT = "df_ch_530486"
MC_ENDPOINT = "http://service.cn-hangzhou.maxcompute.aliyun.com/api"
WORKERS = 10

TABLES = {
    "bycontent": {
        "ods": "ods_xhs_grass_bycontent_conversion_di",
        "dwd": "dwd_xhs_conversion_bycontent_di",
        "pg_cols": "task_id, note_id, dt, attribution_period, grass_alliance, raw_data",
    },
    "bytask": {
        "ods": "ods_xhs_grass_bytask_conversion_di",
        "dwd": "dwd_xhs_conversion_bytask_di",
        "pg_cols": "task_id, dt, attribution_period, grass_alliance, raw_data",
    },
}

DWD_SQL_BYCONTENT = """
INSERT OVERWRITE TABLE dwd_xhs_conversion_bycontent_di PARTITION (ds='{ds}')
SELECT
    b.task_id,
    GET_JSON_OBJECT(b.raw_data, '$.advertiser_id')    AS advertiser_id,
    GET_JSON_OBJECT(b.raw_data, '$.creativity_id')     AS creativity_id,
    b.note_id,
    b.grass_alliance,
    b.attribution_period,
    b.dt,
    -1 AS ad_offsite_active_uv,
    -1 AS ad_offsite_task_cost,
    -1 AS ad_offsite_task_read_uv,
    -1 AS ad_offsite_active_uv_dedup,
    -1 AS ad_offsite_task_cost_dedup,
    -1 AS ad_offsite_task_read_uv_dedup,
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.read_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.enter_shop_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_new_visitor_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_collect_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.add_cart_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_follow_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_member_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_order_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_order_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.task_product_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.task_product_new_customer_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.non_task_product_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_new_customer_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.presale_deposit_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.presale_estimated_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.presale_deposit_uv') AS BIGINT), 0),
    GETDATE()
FROM ods_xhs_grass_bycontent_conversion_di b
WHERE b.ds = '{ds}'
    AND NOT (
        GET_JSON_OBJECT(b.raw_data, '$.read_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.enter_shop_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_new_visitor_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_collect_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.add_cart_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_follow_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_member_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_order_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_order_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.task_product_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.task_product_new_customer_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.non_task_product_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_new_customer_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.presale_deposit_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.presale_estimated_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.presale_deposit_uv') IS NULL
    )
"""

DWD_SQL_BYTASK = """
INSERT OVERWRITE TABLE dwd_xhs_conversion_bytask_di PARTITION (ds='{ds}')
SELECT
    task_id, grass_alliance, attribution_period, dt,
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.read_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.enter_shop_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_new_visitor_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_collect_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.add_cart_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_follow_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_member_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_order_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_order_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.task_product_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.task_product_new_customer_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.non_task_product_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_new_customer_uv') AS BIGINT), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.presale_deposit_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.presale_estimated_gmv') AS DECIMAL(18,2)), 0),
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.presale_deposit_uv') AS BIGINT), 0),
    GETDATE()
FROM ods_xhs_grass_bytask_conversion_di
WHERE ds = '{ds}'
    AND NOT (
        GET_JSON_OBJECT(raw_data, '$.read_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.enter_shop_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_new_visitor_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_collect_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.add_cart_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_follow_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_member_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_order_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_order_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.task_product_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.task_product_new_customer_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.non_task_product_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_new_customer_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.presale_deposit_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.presale_estimated_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.presale_deposit_uv') IS NULL
    )
"""

DWD_SQL = {"bycontent": DWD_SQL_BYCONTENT, "bytask": DWD_SQL_BYTASK}


def get_odps():
    return ODPS(
        access_id=os.environ["ALIYUN_ACCESS_KEY_ID"],
        secret_access_key=os.environ["ALIYUN_ACCESS_KEY_SECRET"],
        project=MC_PROJECT,
        endpoint=MC_ENDPOINT,
    )


def sync_ods(kind, conn, odps):
    """Sync one ODS table from PG to MC, return row count."""
    cfg = TABLES[kind]
    table_name = cfg["ods"]
    cols = cfg["pg_cols"]
    col_list = [c.strip() for c in cols.split(",")]

    mc_table = odps.get_table(table_name)
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT dt FROM {table_name} ORDER BY dt")
    dates = [row[0] for row in cur.fetchall()]
    print(f"{len(dates)} partitions to sync")

    total = 0
    for dt in dates:
        ds = dt.replace("-", "")
        cur.execute(f"SELECT {cols} FROM {table_name} WHERE dt = %s", (dt,))
        rows = cur.fetchall()
        if not rows:
            print(f"  [{ds}] empty, skipped")
            continue

        now = datetime.now()
        records = []
        for r in rows:
            rec = []
            for i, val in enumerate(r):
                col = col_list[i]
                if col == "raw_data":
                    rec.append(
                        json.dumps(val, ensure_ascii=False) if val else "{}"
                    )
                else:
                    rec.append(val)
            rec.append(now)  # etl_time
            records.append(rec)

        partition = f"ds='{ds}'"
        with mc_table.open_writer(
            partition=partition, create_partition=True, overwrite=True
        ) as writer:
            writer.write(records)

        total += len(records)
        print(f"  [{ds}] {len(records)} rows OK")

    cur.close()
    return total


def run_dwd_partition(kind, ds):
    """Run DWD ETL for one partition, return (ds, success, error)."""
    o = get_odps()
    sql = DWD_SQL[kind].format(ds=ds)
    try:
        inst = o.execute_sql(sql)
        inst.wait_for_success()
        return ds, True, None
    except Exception as e:
        return ds, False, str(e)


def rerun_dwd(kind, odps):
    """Rerun all DWD partitions with concurrency, return (ok, fail)."""
    ods_table = odps.get_table(TABLES[kind]["ods"])
    partitions = sorted(
        p.name.split("=")[1].strip("'") for p in ods_table.partitions
    )
    print(f"{len(partitions)} partitions to rerun")

    ok, fail = 0, 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {
            pool.submit(run_dwd_partition, kind, ds): ds for ds in partitions
        }
        for future in as_completed(futures):
            ds, success, err = future.result()
            if success:
                ok += 1
                print(f"  [{ds}] OK")
            else:
                fail += 1
                print(f"  [{ds}] FAIL: {err}")

    return ok, fail


def main():
    for var in ("ALIYUN_ACCESS_KEY_ID", "ALIYUN_ACCESS_KEY_SECRET"):
        if var not in os.environ:
            print(f"ERROR: {var} not set")
            sys.exit(1)

    odps = get_odps()
    conn = psycopg2.connect(**PG_CONFIG)
    stats = {}

    # Step 1-2: PG -> ODS
    for step, kind in enumerate(("bycontent", "bytask"), 1):
        print(f"\n=== Step {step}/4: PG -> ODS {kind} ===")
        rows = sync_ods(kind, conn, odps)
        stats[kind] = {"ods_rows": rows}
        print(f"Subtotal: {rows:,} rows")

    conn.close()

    # Step 3-4: ODS -> DWD
    for step, kind in enumerate(("bycontent", "bytask"), 3):
        print(f"\n=== Step {step}/4: ODS -> DWD {kind} ({WORKERS} workers) ===")
        ok, fail = rerun_dwd(kind, odps)
        stats[kind]["dwd_ok"] = ok
        stats[kind]["dwd_fail"] = fail
        print(f"Done: {ok} OK, {fail} FAIL")

    # Summary
    print("\n=== Summary ===")
    print(f"{'Table':<12} {'ODS Rows':>10} {'DWD OK':>8} {'DWD FAIL':>10}")
    print("-" * 44)
    for kind in ("bycontent", "bytask"):
        s = stats[kind]
        print(
            f"{kind:<12} {s['ods_rows']:>10,} {s['dwd_ok']:>8} {s['dwd_fail']:>10}"
        )

    total_fail = sum(s["dwd_fail"] for s in stats.values())
    if total_fail > 0:
        print(f"\nWARNING: {total_fail} DWD partition(s) failed")
        sys.exit(1)
    else:
        print("\nAll done.")


if __name__ == "__main__":
    main()
