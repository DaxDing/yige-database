"""
拉取聚光离线创意报表 → 写入 MaxCompute ODS → 重跑 DWD（10并发）

用法:
  export $(cat .env | xargs)
  python3 load_creative_hi.py \
    --start 2025-11-28 \
    --end 2026-01-25 \
    --advertiser-id 6209396 \
    --token <access_token>
"""
import argparse, os, json, time, sys, requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from odps import ODPS

# ── 常量 ──
API_URL = "https://adapi.xiaohongshu.com/api/open/jg/data/report/offline/creative"
ODS_TABLE = "ods_xhs_creative_report_hi"
DWD_TABLE = "dwd_xhs_creative_hi"
PAGE_SIZE = 100
WORKERS = 10
SPLIT_COLUMNS = [
    "marketingTarget", "deliveryMode", "placement",
    "biddingStrategy", "promotionTarget"
]


def get_odps():
    return ODPS(
        access_id=os.environ["ALIYUN_ACCESS_KEY_ID"],
        secret_access_key=os.environ["ALIYUN_ACCESS_KEY_SECRET"],
        project="df_ch_530486",
        endpoint="http://service.cn-hangzhou.maxcompute.aliyun.com/api",
    )


def fetch_day(date_str, advertiser_id, session):
    """拉取单日全量数据（自动翻页，指数退避重试）"""
    records = []
    page = 1
    while True:
        for attempt in range(3):
            try:
                resp = session.post(API_URL, json={
                    "advertiser_id": advertiser_id,
                    "start_date": date_str,
                    "end_date": date_str,
                    "time_unit": "HOUR",
                    "split_columns": SPLIT_COLUMNS,
                    "page_num": page,
                    "page_size": PAGE_SIZE
                }, timeout=30)
                data = resp.json()
                break
            except Exception as e:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                print(f"  网络错误: {e}", file=sys.stderr)
                return records

        if data.get("code") != 0:
            print(f"  API error (page {page}): {data.get('msg')}", file=sys.stderr)
            break

        items = data.get("data", {}).get("data_list", [])
        records.extend(items)
        total = data["data"].get("total_count", 0)
        if page * PAGE_SIZE >= total:
            break
        page += 1
        time.sleep(1)
    return records


def transform_to_ods(record):
    """API 记录 → ODS 表行（creativity_id, dt, raw_data, etl_time）"""
    return [
        record.get("creativity_id", ""),
        record.get("time", ""),
        json.dumps(record, ensure_ascii=False),
        datetime.now(),
    ]


DWD_SQL = """
INSERT OVERWRITE TABLE dwd_xhs_creative_hi PARTITION (ds='{ds}')
SELECT
    a.creativity_id,
    GET_JSON_OBJECT(a.raw_data, '$.note_id')                          AS note_id,
    GET_JSON_OBJECT(a.raw_data, '$.unit_id')                          AS unit_id,
    GET_JSON_OBJECT(a.raw_data, '$.campaign_id')                      AS campaign_id,
    CAST(GET_JSON_OBJECT(a.raw_data, '$.placement') AS INT)           AS placement,
    CAST(GET_JSON_OBJECT(a.raw_data, '$.marketing_target') AS INT)    AS marketing_target,
    CAST(GET_JSON_OBJECT(a.raw_data, '$.promotion_target') AS INT)    AS promotion_target,
    CAST(GET_JSON_OBJECT(a.raw_data, '$.optimize_target') AS INT)     AS optimize_target,
    CAST(GET_JSON_OBJECT(a.raw_data, '$.bidding_strategy') AS INT)    AS bidding_strategy,
    a.dt,
    CAST(GET_JSON_OBJECT(a.raw_data, '$.fee') AS DECIMAL(18,2))       AS fee,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.impression') AS BIGINT), 0)       AS impression,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.click') AS BIGINT), 0)            AS click,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.like') AS BIGINT), 0)             AS `like`,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.comment') AS BIGINT), 0)          AS `comment`,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.collect') AS BIGINT), 0)          AS collect,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.follow') AS BIGINT), 0)           AS follow,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.share') AS BIGINT), 0)            AS share,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.interaction') AS BIGINT), 0)      AS interaction,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.action_button_click') AS BIGINT), 0) AS action_button_click,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.screenshot') AS BIGINT), 0)       AS screenshot,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.pic_save') AS BIGINT), 0)         AS pic_save,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.reserve_pv') AS BIGINT), 0)       AS reserve_pv,
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.video_play_5s_cnt') AS BIGINT), 0) AS video_play_5s_cnt,
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{{',
            '"search_cmt_click":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_cmt_click'), '0'), ',',
            '"search_cmt_after_read":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_cmt_after_read'), '0'), ',',
            '"i_user_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.i_user_num'), '0'), ',',
            '"ti_user_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.ti_user_num'), '0'),
        '}}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}}', '}}'),
        '\\{{,', '{{')
    AS product_seeding_metrics,
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{{',
            '"leads":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.leads'), '0'), ',',
            '"landing_page_visit":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.landing_page_visit'), '0'), ',',
            '"leads_button_impression":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.leads_button_impression'), '0'), ',',
            '"message_user":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message_user'), '0'), ',',
            '"message":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message'), '0'), ',',
            '"message_consult":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message_consult'), '0'), ',',
            '"initiative_message":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.initiative_message'), '0'), ',',
            '"msg_leads_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.msg_leads_num'), '0'),
        '}}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}}', '}}'),
        '\\{{,', '{{')
    AS lead_collection_metrics,
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{{',
            '"invoke_app_open_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_open_cnt'), '0'), ',',
            '"invoke_app_enter_store_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_enter_store_cnt'), '0'), ',',
            '"invoke_app_engagement_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_engagement_cnt'), '0'), ',',
            '"invoke_app_payment_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_payment_cnt'), '0'), ',',
            '"search_invoke_button_click_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_invoke_button_click_cnt'), '0'), ',',
            '"invoke_app_payment_amount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_payment_amount'), '0'), ',',
            '"app_activate_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_activate_cnt'), '0'), ',',
            '"app_register_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_register_cnt'), '0'), ',',
            '"first_app_pay_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.first_app_pay_cnt'), '0'), ',',
            '"current_app_pay_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.current_app_pay_cnt'), '0'), ',',
            '"app_key_action_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_key_action_cnt'), '0'), ',',
            '"app_pay_cnt_7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_pay_cnt_7d'), '0'), ',',
            '"app_pay_amount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_pay_amount'), '0'), ',',
            '"app_activate_amount_1d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_activate_amount_1d'), '0'), ',',
            '"app_activate_amount_3d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_activate_amount_3d'), '0'), ',',
            '"app_activate_amount_7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_activate_amount_7d'), '0'), ',',
            '"retention_1d_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention_1d_cnt'), '0'), ',',
            '"retention_3d_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention_3d_cnt'), '0'), ',',
            '"retention_7d_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention_7d_cnt'), '0'),
        '}}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}}', '}}'),
        '\\{{,', '{{')
    AS app_promotion_metrics,
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{{',
            '"external_goods_visit_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_visit_7'), '0'), ',',
            '"external_goods_order_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_7'), '0'), ',',
            '"external_rgmv_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_7'), '0'), ',',
            '"external_goods_order_15":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_15'), '0'), ',',
            '"external_rgmv_15":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_15'), '0'), ',',
            '"external_goods_order_30":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_30'), '0'), ',',
            '"external_rgmv_30":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_30'), '0'),
        '}}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}}', '}}'),
        '\\{{,', '{{')
    AS direct_seeding_metrics,
    GETDATE() AS etl_time
FROM ods_xhs_creative_report_hi a
WHERE a.ds = '{ds}'
"""


def run_dwd(ds):
    """重跑单个 DWD 分区"""
    o2 = get_odps()
    sql = DWD_SQL.format(ds=ds)
    try:
        inst = o2.execute_sql(sql)
        inst.wait_for_success()
        return ds, True, None
    except Exception as e:
        return ds, False, str(e)


def main():
    parser = argparse.ArgumentParser(description="拉取聚光离线创意报表 → ODS → DWD")
    parser.add_argument("--start", required=True, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--advertiser-id", type=int, required=True, help="投放账号ID")
    parser.add_argument("--token", required=True, help="API Access-Token")
    args = parser.parse_args()

    o = get_odps()
    table = o.get_table(ODS_TABLE)

    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Access-Token": args.token
    })

    # ========== Step 1: API → ODS ==========
    print("=" * 50)
    print("Step 1: API → ODS")
    print("=" * 50)

    cur = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")
    total_written = 0
    ds_list = []

    while cur <= end:
        date_str = cur.strftime("%Y-%m-%d")
        ds = cur.strftime("%Y%m%d")
        print(f"[{ds}] 拉取中...", end=" ", flush=True)

        items = fetch_day(date_str, args.advertiser_id, session)
        print(f"{len(items)} 条", end=" ", flush=True)

        if items:
            partition = f"ds='{ds}'"
            with table.open_writer(partition=partition, create_partition=True, overwrite=True) as writer:
                writer.write([transform_to_ods(r) for r in items])
            total_written += len(items)
            ds_list.append(ds)
            print("✓")
        else:
            print("跳过(无数据)")

        cur += timedelta(days=1)
        time.sleep(2)

    print(f"\nODS 写入完成: {total_written} 条 → {ODS_TABLE}")

    if not ds_list:
        print("无数据，跳过 DWD")
        return

    # ========== Step 2: ODS → DWD (10并发) ==========
    print(f"\n{'=' * 50}")
    print(f"Step 2: ODS → DWD ({WORKERS}并发)")
    print("=" * 50)
    print(f"共 {len(ds_list)} 个分区待重跑")

    ok = 0
    fail = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(run_dwd, ds): ds for ds in ds_list}
        for future in as_completed(futures):
            ds, success, err = future.result()
            if success:
                ok += 1
                print(f"[{ok + fail}/{len(ds_list)}] {ds} ✓")
            else:
                fail += 1
                print(f"[{ok + fail}/{len(ds_list)}] {ds} ✗ {err}")

    print(f"\nDWD 重跑完成: {ok}/{len(ds_list)} 成功, {fail} 失败")
    print(f"\n汇总: ODS {total_written} 条, DWD {ok}/{len(ds_list)} 分区")


if __name__ == "__main__":
    main()
