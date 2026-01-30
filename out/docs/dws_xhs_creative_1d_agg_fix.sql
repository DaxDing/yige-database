-- ============================================================
-- ETL: DWD → DWS 创意日汇总（30天滚动累计）- 修复版
-- 源表: dwd_xhs_creative_hi, brg_xhs_note_project_df, dwd_xhs_conversion_bycontent_di
-- 目标表: dws_xhs_creative_1d_agg
-- 修复:
--   1. 窗口函数增加 ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
--   2. WHERE 条件改为取 59 天数据，外层过滤输出最近 30 天
--   3. 客单价字段改为除法计算，不再累计
-- ============================================================

INSERT OVERWRITE TABLE dws_xhs_creative_1d_agg PARTITION (ds)
SELECT
    -- ============ 维度字段 ============
    creativity_id,
    advertiser_id,
    note_id,
    unit_id,
    campaign_id,
    dt,

    -- ============ 展现指标（30天滚动累计） ============
    SUM(fee) OVER w AS fee,
    SUM(impression) OVER w AS impression,
    SUM(click) OVER w AS click,

    -- ============ 笔记指标（30天滚动累计） ============
    SUM(`like`) OVER w AS `like`,
    SUM(comment) OVER w AS comment,
    SUM(collect) OVER w AS collect,
    SUM(follow) OVER w AS follow,
    SUM(share) OVER w AS share,
    SUM(interaction) OVER w AS interaction,
    SUM(action_button_click) OVER w AS action_button_click,
    SUM(screenshot) OVER w AS screenshot,
    SUM(pic_save) OVER w AS pic_save,
    SUM(reserve_pv) OVER w AS reserve_pv,

    -- ============ 视频指标（30天滚动累计） ============
    SUM(video_play_5s_cnt) OVER w AS video_play_5s_cnt,

    -- ============ 产品种草指标（30天滚动累计） ============
    SUM(search_cmt_click) OVER w AS search_cmt_click,
    SUM(search_cmt_after_read) OVER w AS search_cmt_after_read,
    SUM(i_user_num) OVER w AS i_user_num,
    SUM(ti_user_num) OVER w AS ti_user_num,

    -- ============ 客资收集指标（30天滚动累计） ============
    SUM(leads) OVER w AS leads,
    SUM(landing_page_visit) OVER w AS landing_page_visit,
    SUM(leads_button_impression) OVER w AS leads_button_impression,
    SUM(message_user) OVER w AS message_user,
    SUM(message) OVER w AS message,
    SUM(message_consult) OVER w AS message_consult,
    SUM(initiative_message) OVER w AS initiative_message,
    SUM(msg_leads_num) OVER w AS msg_leads_num,

    -- ============ 应用推广指标（30天滚动累计） ============
    SUM(invoke_app_open_cnt) OVER w AS invoke_app_open_cnt,
    SUM(invoke_app_enter_store_cnt) OVER w AS invoke_app_enter_store_cnt,
    SUM(invoke_app_engagement_cnt) OVER w AS invoke_app_engagement_cnt,
    SUM(invoke_app_payment_cnt) OVER w AS invoke_app_payment_cnt,
    SUM(search_invoke_button_click_cnt) OVER w AS search_invoke_button_click_cnt,
    SUM(invoke_app_payment_amount) OVER w AS invoke_app_payment_amount,
    SUM(app_activate_cnt) OVER w AS app_activate_cnt,
    SUM(app_register_cnt) OVER w AS app_register_cnt,
    SUM(first_app_pay_cnt) OVER w AS first_app_pay_cnt,
    SUM(current_app_pay_cnt) OVER w AS current_app_pay_cnt,
    SUM(app_key_action_cnt) OVER w AS app_key_action_cnt,
    SUM(app_pay_cnt_7d) OVER w AS app_pay_cnt_7d,
    SUM(app_pay_amount) OVER w AS app_pay_amount,
    SUM(app_activate_amount_1d) OVER w AS app_activate_amount_1d,
    SUM(app_activate_amount_3d) OVER w AS app_activate_amount_3d,
    SUM(app_activate_amount_7d) OVER w AS app_activate_amount_7d,
    SUM(retention_1d_cnt) OVER w AS retention_1d_cnt,
    SUM(retention_3d_cnt) OVER w AS retention_3d_cnt,
    SUM(retention_7d_cnt) OVER w AS retention_7d_cnt,

    -- ============ 种草直达指标（30天滚动累计） ============
    SUM(external_goods_visit_7) OVER w AS external_goods_visit_7,
    SUM(external_goods_order_7) OVER w AS external_goods_order_7,
    SUM(external_rgmv_7) OVER w AS external_rgmv_7,
    SUM(external_goods_order_15) OVER w AS external_goods_order_15,
    SUM(external_rgmv_15) OVER w AS external_rgmv_15,
    -- 修复：客单价 = GMV / 订单数
    SUM(external_rgmv_15) OVER w / NULLIF(SUM(external_goods_order_15) OVER w, 0) AS external_goods_order_price_15,
    SUM(external_goods_order_30) OVER w AS external_goods_order_30,
    SUM(external_rgmv_30) OVER w AS external_rgmv_30,
    -- 修复：客单价 = GMV / 订单数
    SUM(external_rgmv_30) OVER w / NULLIF(SUM(external_goods_order_30) OVER w, 0) AS external_goods_order_price_30,

    -- ============ 站外行为指标 15天归因（30天滚动累计） ============
    SUM(15d_ad_offsite_active_uv) OVER w AS 15d_ad_offsite_active_uv,
    SUM(15d_ad_offsite_task_cost) OVER w AS 15d_ad_offsite_task_cost,
    SUM(15d_ad_offsite_task_read_uv) OVER w AS 15d_ad_offsite_task_read_uv,
    SUM(15d_ad_offsite_active_uv_dedup) OVER w AS 15d_ad_offsite_active_uv_dedup,
    SUM(15d_ad_offsite_task_cost_dedup) OVER w AS 15d_ad_offsite_task_cost_dedup,
    SUM(15d_ad_offsite_task_read_uv_dedup) OVER w AS 15d_ad_offsite_task_read_uv_dedup,

    -- ============ 站外行为指标 30天归因（30天滚动累计） ============
    SUM(30d_ad_offsite_active_uv) OVER w AS 30d_ad_offsite_active_uv,
    SUM(30d_ad_offsite_task_cost) OVER w AS 30d_ad_offsite_task_cost,
    SUM(30d_ad_offsite_task_read_uv) OVER w AS 30d_ad_offsite_task_read_uv,
    SUM(30d_ad_offsite_active_uv_dedup) OVER w AS 30d_ad_offsite_active_uv_dedup,
    SUM(30d_ad_offsite_task_cost_dedup) OVER w AS 30d_ad_offsite_task_cost_dedup,
    SUM(30d_ad_offsite_task_read_uv_dedup) OVER w AS 30d_ad_offsite_task_read_uv_dedup,

    -- ============ 系统字段 ============
    GETDATE() AS etl_time,
    ds
FROM (
    -- ========== 内层：小时 → 日汇总 ==========
    SELECT
        a.creativity_id,
        MAX(a.advertiser_id) AS advertiser_id,
        MAX(a.note_id) AS note_id,
        MAX(a.unit_id) AS unit_id,
        MAX(a.campaign_id) AS campaign_id,
        SUBSTR(a.dt, 1, 10) AS dt,

        SUM(a.fee) AS fee,
        SUM(a.impression) AS impression,
        SUM(a.click) AS click,
        SUM(a.`like`) AS `like`,
        SUM(a.comment) AS comment,
        SUM(a.collect) AS collect,
        SUM(a.follow) AS follow,
        SUM(a.share) AS share,
        SUM(a.interaction) AS interaction,
        SUM(a.action_button_click) AS action_button_click,
        SUM(a.screenshot) AS screenshot,
        SUM(a.pic_save) AS pic_save,
        SUM(a.reserve_pv) AS reserve_pv,
        SUM(a.video_play_5s_cnt) AS video_play_5s_cnt,

        SUM(CAST(GET_JSON_OBJECT(a.product_seeding_metrics, '$.search_cmt_click') AS BIGINT)) AS search_cmt_click,
        SUM(CAST(GET_JSON_OBJECT(a.product_seeding_metrics, '$.search_cmt_after_read') AS BIGINT)) AS search_cmt_after_read,
        SUM(CAST(GET_JSON_OBJECT(a.product_seeding_metrics, '$.i_user_num') AS BIGINT)) AS i_user_num,
        SUM(CAST(GET_JSON_OBJECT(a.product_seeding_metrics, '$.ti_user_num') AS BIGINT)) AS ti_user_num,

        SUM(CAST(GET_JSON_OBJECT(a.lead_collection_metrics, '$.leads') AS BIGINT)) AS leads,
        SUM(CAST(GET_JSON_OBJECT(a.lead_collection_metrics, '$.landing_page_visit') AS BIGINT)) AS landing_page_visit,
        SUM(CAST(GET_JSON_OBJECT(a.lead_collection_metrics, '$.leads_button_impression') AS BIGINT)) AS leads_button_impression,
        SUM(CAST(GET_JSON_OBJECT(a.lead_collection_metrics, '$.message_user') AS BIGINT)) AS message_user,
        SUM(CAST(GET_JSON_OBJECT(a.lead_collection_metrics, '$.message') AS BIGINT)) AS message,
        SUM(CAST(GET_JSON_OBJECT(a.lead_collection_metrics, '$.message_consult') AS BIGINT)) AS message_consult,
        SUM(CAST(GET_JSON_OBJECT(a.lead_collection_metrics, '$.initiative_message') AS BIGINT)) AS initiative_message,
        SUM(CAST(GET_JSON_OBJECT(a.lead_collection_metrics, '$.msg_leads_num') AS BIGINT)) AS msg_leads_num,

        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.invoke_app_open_cnt') AS BIGINT)) AS invoke_app_open_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.invoke_app_enter_store_cnt') AS BIGINT)) AS invoke_app_enter_store_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.invoke_app_engagement_cnt') AS BIGINT)) AS invoke_app_engagement_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.invoke_app_payment_cnt') AS BIGINT)) AS invoke_app_payment_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.search_invoke_button_click_cnt') AS BIGINT)) AS search_invoke_button_click_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.invoke_app_payment_amount') AS DECIMAL(18,2))) AS invoke_app_payment_amount,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.app_activate_cnt') AS BIGINT)) AS app_activate_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.app_register_cnt') AS BIGINT)) AS app_register_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.first_app_pay_cnt') AS BIGINT)) AS first_app_pay_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.current_app_pay_cnt') AS BIGINT)) AS current_app_pay_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.app_key_action_cnt') AS BIGINT)) AS app_key_action_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.app_pay_cnt_7d') AS BIGINT)) AS app_pay_cnt_7d,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.app_pay_amount') AS DECIMAL(18,2))) AS app_pay_amount,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.app_activate_amount_1d') AS DECIMAL(18,2))) AS app_activate_amount_1d,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.app_activate_amount_3d') AS DECIMAL(18,2))) AS app_activate_amount_3d,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.app_activate_amount_7d') AS DECIMAL(18,2))) AS app_activate_amount_7d,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.retention_1d_cnt') AS BIGINT)) AS retention_1d_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.retention_3d_cnt') AS BIGINT)) AS retention_3d_cnt,
        SUM(CAST(GET_JSON_OBJECT(a.app_promotion_metrics, '$.retention_7d_cnt') AS BIGINT)) AS retention_7d_cnt,

        SUM(CAST(GET_JSON_OBJECT(a.direct_seeding_metrics, '$.external_goods_visit_7') AS BIGINT)) AS external_goods_visit_7,
        SUM(CAST(GET_JSON_OBJECT(a.direct_seeding_metrics, '$.external_goods_order_7') AS BIGINT)) AS external_goods_order_7,
        SUM(CAST(GET_JSON_OBJECT(a.direct_seeding_metrics, '$.external_rgmv_7') AS DECIMAL(18,2))) AS external_rgmv_7,
        SUM(CAST(GET_JSON_OBJECT(a.direct_seeding_metrics, '$.external_goods_order_15') AS BIGINT)) AS external_goods_order_15,
        SUM(CAST(GET_JSON_OBJECT(a.direct_seeding_metrics, '$.external_rgmv_15') AS DECIMAL(18,2))) AS external_rgmv_15,
        -- 内层不再聚合客单价，在外层计算
        SUM(CAST(GET_JSON_OBJECT(a.direct_seeding_metrics, '$.external_goods_order_30') AS BIGINT)) AS external_goods_order_30,
        SUM(CAST(GET_JSON_OBJECT(a.direct_seeding_metrics, '$.external_rgmv_30') AS DECIMAL(18,2))) AS external_rgmv_30,

        SUM(CASE WHEN c.attribution_period = '15' THEN c.ad_offsite_active_uv END) AS 15d_ad_offsite_active_uv,
        SUM(CASE WHEN c.attribution_period = '15' THEN c.ad_offsite_task_cost END) AS 15d_ad_offsite_task_cost,
        SUM(CASE WHEN c.attribution_period = '15' THEN c.ad_offsite_task_read_uv END) AS 15d_ad_offsite_task_read_uv,
        SUM(CASE WHEN c.attribution_period = '15' THEN c.ad_offsite_active_uv_dedup END) AS 15d_ad_offsite_active_uv_dedup,
        SUM(CASE WHEN c.attribution_period = '15' THEN c.ad_offsite_task_cost_dedup END) AS 15d_ad_offsite_task_cost_dedup,
        SUM(CASE WHEN c.attribution_period = '15' THEN c.ad_offsite_task_read_uv_dedup END) AS 15d_ad_offsite_task_read_uv_dedup,

        SUM(CASE WHEN c.attribution_period = '30' THEN c.ad_offsite_active_uv END) AS 30d_ad_offsite_active_uv,
        SUM(CASE WHEN c.attribution_period = '30' THEN c.ad_offsite_task_cost END) AS 30d_ad_offsite_task_cost,
        SUM(CASE WHEN c.attribution_period = '30' THEN c.ad_offsite_task_read_uv END) AS 30d_ad_offsite_task_read_uv,
        SUM(CASE WHEN c.attribution_period = '30' THEN c.ad_offsite_active_uv_dedup END) AS 30d_ad_offsite_active_uv_dedup,
        SUM(CASE WHEN c.attribution_period = '30' THEN c.ad_offsite_task_cost_dedup END) AS 30d_ad_offsite_task_cost_dedup,
        SUM(CASE WHEN c.attribution_period = '30' THEN c.ad_offsite_task_read_uv_dedup END) AS 30d_ad_offsite_task_read_uv_dedup,

        a.ds
    FROM dwd_xhs_creative_hi a
    INNER JOIN brg_xhs_note_project_df b
        ON a.note_id = b.note_id
        AND b.ds = '${bizdate}'
    LEFT JOIN dwd_xhs_conversion_bycontent_di c
        ON a.creativity_id = c.creativity_id
        AND SUBSTR(a.dt, 1, 10) = c.dt
        AND c.ds = a.ds
    -- 修复：取 59 天数据以保证 30 天窗口完整
    WHERE a.ds >= TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -58, 'dd'), 'yyyymmdd')
      AND a.ds <= '${bizdate}'
    GROUP BY a.creativity_id, SUBSTR(a.dt, 1, 10), a.ds
) daily
-- 定义窗口：30 天滚动（包含当前行）
WINDOW w AS (
    PARTITION BY creativity_id
    ORDER BY ds
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
)
-- 修复：只输出最近 30 天的结果
WHERE ds >= TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -29, 'dd'), 'yyyymmdd')
;
