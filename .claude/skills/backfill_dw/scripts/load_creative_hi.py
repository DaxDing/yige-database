"""
拉取聚光离线创意报表 → 核对 ODS → 合并写入 → 重跑 DWD（10并发）

用法:
  export $(cat .env | xargs)
  python3 load_creative_hi.py \
    --start 2026-02-14 \
    --end 2026-03-12 \
    --advertiser-ids 9590195,8936364,8517830 \
    --tokens token1,token2,token3
"""
import argparse, os, json, time, sys, requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from odps import ODPS

# ── 常量 ──
API_URL = "https://adapi.xiaohongshu.com/api/open/jg/data/report/offline/creative"
ODS_TABLE = "ods_xhs_creative_report_hi"
DWD_TABLE = "dwd_xhs_creative_hi"
PAGE_SIZE = 500
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


def fetch_range(start_date, end_date, advertiser_id, session):
    """拉取日期范围全量数据（自动翻页，指数退避重试）"""
    records = []
    page = 1
    while True:
        for attempt in range(3):
            try:
                resp = session.post(API_URL, json={
                    "advertiser_id": advertiser_id,
                    "start_date": start_date,
                    "end_date": end_date,
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
        print(f"\r  已拉取 {len(records)}/{total} 条", end="", flush=True)
        if page * PAGE_SIZE >= total:
            break
        page += 1
        time.sleep(0.3)
    print()
    return records


def group_by_ds(records):
    """按 time 字段的日期部分分组，返回 {ds: [records]}"""
    groups = {}
    for r in records:
        dt = r.get("time", "")
        ds = dt[:10].replace("-", "") if len(dt) >= 10 else "unknown"
        groups.setdefault(ds, []).append(r)
    return groups


def check_ods_existing(ds_list):
    """批量查询 ODS 中已有的 (creativity_id, dt) 集合，按 ds 分组"""
    o = get_odps()
    existing = {}
    # 分批查询，每批 10 个分区
    for i in range(0, len(ds_list), 10):
        batch = ds_list[i:i + 10]
        ds_in = ",".join(f"'{ds}'" for ds in batch)
        sql = f"SELECT ds, creativity_id, dt FROM {ODS_TABLE} WHERE ds IN ({ds_in})"
        try:
            with o.execute_sql(sql).open_reader() as reader:
                for row in reader:
                    ds = row['ds']
                    existing.setdefault(ds, set()).add((row['creativity_id'], row['dt']))
        except Exception as e:
            print(f"  查询分区 {batch} 失败: {e}", file=sys.stderr)
    return existing


def transform_to_ods(record):
    """API 记录 → ODS 表行（creativity_id, dt, raw_data, etl_time）"""
    return [
        record.get("creativity_id", ""),
        record.get("time", ""),
        json.dumps(record, ensure_ascii=False),
        datetime.now(),
    ]


def merge_write_ods(table_name, ds, new_items):
    """合并写入 ODS 分区：读已有 + 合并新数据 + 覆写（保留其他广告主数据）"""
    o = get_odps()
    table = o.get_table(table_name)
    partition = f"ds='{ds}'"

    # 读取已有数据，以 (creativity_id, dt) 为 key
    merged = {}
    try:
        sql = f"SELECT creativity_id, dt, raw_data, etl_time FROM {table_name} WHERE ds = '{ds}'"
        with o.execute_sql(sql).open_reader() as reader:
            for row in reader:
                key = (row['creativity_id'], row['dt'])
                merged[key] = [row['creativity_id'], row['dt'], row['raw_data'], row['etl_time']]
    except Exception:
        pass

    old_count = len(merged)

    # 新数据覆盖同 key 的已有数据
    for item in new_items:
        key = (item.get("creativity_id", ""), item.get("time", ""))
        merged[key] = transform_to_ods(item)

    rows = list(merged.values())
    with table.open_writer(partition=partition, create_partition=True, overwrite=True) as writer:
        writer.write(rows)

    added = len(rows) - old_count
    return ds, added, len(rows)


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
    parser = argparse.ArgumentParser(description="拉取聚光离线创意报表 → 核对 → ODS → DWD")
    parser.add_argument("--start", required=True, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--advertiser-ids", required=True, help="投放账号ID，逗号分隔")
    parser.add_argument("--tokens", required=True, help="Access-Token，逗号分隔，与 advertiser-ids 对应")
    args = parser.parse_args()

    # 日期校验：end 不超过昨天
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if args.end > yesterday:
        print(f"end={args.end} 超过昨天({yesterday})，自动截断")
        args.end = yesterday

    adv_ids = [int(x.strip()) for x in args.advertiser_ids.split(",")]
    tokens = [t.strip() for t in args.tokens.split(",")]
    if len(adv_ids) != len(tokens):
        print(f"advertiser-ids({len(adv_ids)}) 与 tokens({len(tokens)}) 数量不匹配", file=sys.stderr)
        sys.exit(1)

    # ========== Step 1: API 并发拉取全量数据 ==========
    print("=" * 50)
    print(f"Step 1: API 并发拉取 ({len(adv_ids)} 个账号)")
    print("=" * 50)

    def _fetch_one(adv_id, token):
        s = requests.Session()
        s.headers.update({"Content-Type": "application/json", "Access-Token": token})
        print(f"[advertiser={adv_id}] 开始拉取...")
        records = fetch_range(args.start, args.end, adv_id, s)
        print(f"[advertiser={adv_id}] 完成: {len(records)} 条")
        return records

    all_records = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(_fetch_one, aid, tok): aid for aid, tok in zip(adv_ids, tokens)}
        for future in as_completed(futures):
            all_records.extend(future.result())

    print(f"共拉取 {len(all_records)} 条")
    if not all_records:
        print("无数据，退出")
        return

    groups = group_by_ds(all_records)
    ds_list = sorted(groups.keys())
    print(f"覆盖 {len(ds_list)} 个分区: {ds_list[0]} ~ {ds_list[-1]}")

    # ========== Step 2: 核对 ODS 已有数据 ==========
    print(f"\n{'=' * 50}")
    print("Step 2: 核对 ODS 已有数据")
    print("=" * 50)

    existing = check_ods_existing(ds_list)

    need_write = []
    skip_count = 0
    for ds in ds_list:
        api_keys = {(r.get("creativity_id", ""), r.get("time", "")) for r in groups[ds]}
        ods_keys = existing.get(ds, set())
        missing = api_keys - ods_keys
        if missing:
            need_write.append(ds)
            print(f"  {ds}: API {len(api_keys)}, ODS {len(api_keys) - len(missing)}, 缺 {len(missing)} → 需补")
        else:
            skip_count += 1
            print(f"  {ds}: API {len(api_keys)}, ODS {len(ods_keys)} → 跳过")

    print(f"\n需补 {len(need_write)} 个分区，跳过 {skip_count} 个")

    if not need_write:
        print("全部已有数据，无需补数据")
        return

    # ========== Step 3: 合并写入 ODS ==========
    print(f"\n{'=' * 50}")
    print(f"Step 3: ODS 合并写入 ({WORKERS}并发)")
    print("=" * 50)

    total_added = 0
    ok_ds = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {
            pool.submit(merge_write_ods, ODS_TABLE, ds, groups[ds]): ds
            for ds in need_write
        }
        for future in as_completed(futures):
            ds = futures[future]
            try:
                _, added, total = future.result()
                total_added += added
                ok_ds.append(ds)
                print(f"  [{len(ok_ds)}/{len(need_write)}] {ds} +{added} (共{total})")
            except Exception as e:
                print(f"  {ds} ✗ {e}")

    ok_ds.sort()
    print(f"\nODS 写入完成: 新增 {total_added} 条 → {ODS_TABLE}")

    if not ok_ds:
        print("ODS 全部失败，跳过 DWD")
        return

    # ========== Step 4: ODS → DWD (并发) ==========
    print(f"\n{'=' * 50}")
    print(f"Step 4: ODS → DWD ({WORKERS}并发)")
    print("=" * 50)
    print(f"共 {len(ok_ds)} 个分区待重跑")

    ok = 0
    fail = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(run_dwd, ds): ds for ds in ok_ds}
        for future in as_completed(futures):
            ds, success, err = future.result()
            if success:
                ok += 1
                print(f"  [{ok + fail}/{len(ok_ds)}] {ds} ✓")
            else:
                fail += 1
                print(f"  [{ok + fail}/{len(ok_ds)}] {ds} ✗ {err}")

    print(f"\nDWD 重跑完成: {ok}/{len(ok_ds)} 成功, {fail} 失败")
    print(f"\n汇总: API {len(all_records)} 条, ODS +{total_added}, DWD {ok}/{len(ok_ds)} 分区")


if __name__ == "__main__":
    main()
