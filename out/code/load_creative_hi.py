"""
拉取聚光离线创意报表 → 写入 MaxCompute dwd_xhs_creative_hi
日期范围: 2025-11-28 ~ 2026-01-25, 按日分区 (ds)
"""
import os, json, time, requests
from datetime import datetime, timedelta
from decimal import Decimal
from odps import ODPS
from odps.models import Record

# ── 配置 ──
API_URL = "https://adapi.xiaohongshu.com/api/open/jg/data/report/offline/creative"
TOKEN = "ecdd4fc3d4da54f5fe51a4de7e86276c"
ADVERTISER_ID = 6209396
START_DATE = "2025-11-28"
END_DATE = "2026-01-25"
PAGE_SIZE = 100
TABLE_NAME = "dwd_xhs_creative_hi"

# ── JSON 指标字段分组 ──
PRODUCT_SEEDING_KEYS = [
    "search_cmt_click", "search_cmt_after_read", "i_user_num", "ti_user_num"
]
LEAD_COLLECTION_KEYS = [
    "leads", "landing_page_visit", "leads_button_impression",
    "message_user", "message", "message_consult", "initiative_message", "msg_leads_num"
]
APP_PROMOTION_KEYS = [
    "invoke_app_open_cnt", "invoke_app_enter_store_cnt", "invoke_app_engagement_cnt",
    "invoke_app_payment_cnt", "search_invoke_button_click_cnt", "invoke_app_payment_amount",
    "app_activate_cnt", "app_register_cnt", "first_app_pay_cnt", "current_app_pay_cnt",
    "app_key_action_cnt", "app_pay_cnt_7d", "app_pay_amount",
    "app_activate_amount_1d", "app_activate_amount_3d", "app_activate_amount_7d",
    "retention_1d_cnt", "retention_3d_cnt", "retention_7d_cnt"
]
DIRECT_SEEDING_KEYS = [
    "external_goods_visit_7", "external_goods_order_7", "external_rgmv_7",
    "external_goods_order_15", "external_rgmv_15", "external_goods_order_price_15",
    "external_goods_order_30", "external_rgmv_30", "external_goods_order_price_30"
]


def build_metrics_json(record, keys):
    """构建 JSON 指标字符串，剔除零值键"""
    metrics = {}
    for k in keys:
        v = record.get(k, "0")
        if v and v not in ("0", "0.0"):
            metrics[k] = v
    return json.dumps(metrics, ensure_ascii=False) if metrics else "{}"


def safe_int(val):
    try:
        return int(val) if val else 0
    except (ValueError, TypeError):
        return 0


def safe_decimal(val):
    try:
        return Decimal(val) if val else Decimal("0")
    except Exception:
        return Decimal("0")


def fetch_day(date_str, session):
    """拉取单日全量数据（自动翻页）"""
    records = []
    page = 1
    while True:
        resp = session.post(API_URL, json={
            "advertiser_id": ADVERTISER_ID,
            "start_date": date_str,
            "end_date": date_str,
            "time_unit": "HOUR",
            "split_columns": [
                "marketingTarget", "deliveryMode", "placement",
                "biddingStrategy", "promotionTarget"
            ],
            "page_num": page,
            "page_size": PAGE_SIZE
        })
        data = resp.json()
        if data.get("code") != 0:
            print(f"  API error: {data.get('msg')}")
            break
        items = data.get("data", {}).get("data_list", [])
        records.extend(items)
        total = data["data"].get("total_count", 0)
        if page * PAGE_SIZE >= total:
            break
        page += 1
        time.sleep(0.3)
    return records


def transform(record, ds):
    """API 记录 → DWD 表行"""
    return [
        str(ADVERTISER_ID),                             # advertiser_id
        record.get("note_id", ""),                      # note_id
        record.get("unit_id", ""),                      # unit_id
        record.get("campaign_id", ""),                  # campaign_id
        record.get("creativity_id", ""),                # creativity_id
        safe_int(record.get("placement")),              # placement
        safe_int(record.get("marketing_target")),       # marketing_target
        safe_int(record.get("promotion_target")),       # promotion_target
        safe_int(record.get("optimize_target")),        # optimize_target
        safe_int(record.get("bidding_strategy")),       # bidding_strategy
        record.get("time", ""),                         # dt
        safe_decimal(record.get("fee")),                # fee
        safe_int(record.get("impression")),             # impression
        safe_int(record.get("click")),                  # click
        safe_int(record.get("like")),                   # like
        safe_int(record.get("comment")),                # comment
        safe_int(record.get("collect")),                # collect
        safe_int(record.get("follow")),                 # follow
        safe_int(record.get("share")),                  # share
        safe_int(record.get("interaction")),            # interaction
        safe_int(record.get("action_button_click")),    # action_button_click
        safe_int(record.get("screenshot")),             # screenshot
        safe_int(record.get("pic_save")),               # pic_save
        safe_int(record.get("reserve_pv")),             # reserve_pv
        safe_int(record.get("video_play_5s_cnt")),      # video_play_5s_cnt
        build_metrics_json(record, PRODUCT_SEEDING_KEYS),
        build_metrics_json(record, LEAD_COLLECTION_KEYS),
        build_metrics_json(record, APP_PROMOTION_KEYS),
        build_metrics_json(record, DIRECT_SEEDING_KEYS),
        datetime.now(),                                 # etl_time
    ]


def main():
    o = ODPS(
        access_id=os.environ["ALIYUN_ACCESS_KEY_ID"],
        secret_access_key=os.environ["ALIYUN_ACCESS_KEY_SECRET"],
        project="df_ch_530486",
        endpoint="http://service.cn-hangzhou.maxcompute.aliyun.com/api"
    )
    table = o.get_table(TABLE_NAME)

    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Access-Token": TOKEN
    })

    cur = datetime.strptime(START_DATE, "%Y-%m-%d")
    end = datetime.strptime(END_DATE, "%Y-%m-%d")
    total_written = 0

    while cur <= end:
        date_str = cur.strftime("%Y-%m-%d")
        ds = cur.strftime("%Y%m%d")
        print(f"[{ds}] 拉取中...", end=" ", flush=True)

        items = fetch_day(date_str, session)
        print(f"{len(items)} 条", end=" ", flush=True)

        if items:
            # 创建分区
            partition = f"ds='{ds}'"
            if not table.exist_partition(partition):
                table.create_partition(partition)

            # 写入 MaxCompute
            with table.open_writer(partition=partition, create_partition=True, overwrite=True) as writer:
                rows = [transform(r, ds) for r in items]
                writer.write(rows)

            total_written += len(items)
            print(f"✓ 写入完成")
        else:
            print("跳过(无数据)")

        cur += timedelta(days=1)
        time.sleep(0.5)

    print(f"\n完成: {total_written} 条写入 {TABLE_NAME}")


if __name__ == "__main__":
    main()
