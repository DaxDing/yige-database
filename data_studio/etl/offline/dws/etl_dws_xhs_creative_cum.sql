-- ============================================================
-- ETL: DWD → DWS 创意累计表
-- 源表: dwd_xhs_creative_hi, brg_xhs_note_project_df, dim_xhs_project_df, dwd_xhs_conversion_bycontent_di
-- 目标表: dws_xhs_creative_cum
-- 说明: 基于桥表笔记，分别计算目标日 t / t-1 的创意累计；
--       creative 与 conversion 均限定在项目有效期 [valid_from, min(kpi_fetch_time, target_ds)]
--       输出粒度: creativity_id + ds
-- ============================================================

SET odps.sql.allow.fullscan=true;
SET odps.sql.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE dws_xhs_creative_cum PARTITION (ds)
SELECT
    -- ============ 维度字段 ============
    a.creativity_id,
    a.note_id,
    a.unit_id,
    a.campaign_id,
    a.dt,

    -- ============ 展现指标 ============
    a.fee,
    a.impression,
    a.click,

    -- ============ 笔记指标 ============
    a.`like`,
    a.comment,
    a.collect,
    a.follow,
    a.share,
    a.interaction,
    a.action_button_click,
    a.screenshot,
    a.pic_save,
    a.reserve_pv,

    -- ============ 视频指标 ============
    a.video_play_5s_cnt,

    -- ============ 产品种草指标 ============
    a.search_cmt_click,
    a.search_cmt_after_read,
    a.i_user_num,
    a.ti_user_num,

    -- ============ 客资收集指标 ============
    a.leads,
    a.landing_page_visit,
    a.leads_button_impression,
    a.message_user,
    a.message,
    a.message_consult,
    a.initiative_message,
    a.msg_leads_num,

    -- ============ 应用推广指标 ============
    a.invoke_app_open_cnt,
    a.invoke_app_enter_store_cnt,
    a.invoke_app_engagement_cnt,
    a.invoke_app_payment_cnt,
    a.search_invoke_button_click_cnt,
    a.invoke_app_payment_amount,
    a.app_activate_cnt,
    a.app_register_cnt,
    a.first_app_pay_cnt,
    a.current_app_pay_cnt,
    a.app_key_action_cnt,
    a.app_pay_cnt_7d,
    a.app_pay_amount,
    a.app_activate_amount_1d,
    a.app_activate_amount_3d,
    a.app_activate_amount_7d,
    a.retention_1d_cnt,
    a.retention_3d_cnt,
    a.retention_7d_cnt,

    -- ============ 种草直达指标 ============
    a.external_goods_visit_7,
    a.external_goods_order_7,
    a.external_rgmv_7,
    a.external_goods_order_15,
    a.external_rgmv_15,
    a.external_goods_order_30,
    a.external_rgmv_30,

    -- ============ 站外行为指标 15天归因 ============
    c.15d_ad_offsite_active_uv,
    c.15d_ad_offsite_task_cost,
    c.15d_ad_offsite_task_read_uv,
    c.15d_ad_offsite_active_uv_dedup,
    c.15d_ad_offsite_task_cost_dedup,
    c.15d_ad_offsite_task_read_uv_dedup,

    -- ============ 站外行为指标 30天归因 ============
    c.30d_ad_offsite_active_uv,
    c.30d_ad_offsite_task_cost,
    c.30d_ad_offsite_task_read_uv,
    c.30d_ad_offsite_active_uv_dedup,
    c.30d_ad_offsite_task_cost_dedup,
    c.30d_ad_offsite_task_read_uv_dedup,

    -- ============ 系统字段 ============
    GETDATE() AS etl_time,
    a.target_ds AS ds
FROM (
    -- creative: 基于 brg 笔记 + 项目有效期，按 target_ds 分别累计
    SELECT /*+ MAPJOIN(dates) */
        dates.target_ds,
        h.creativity_id,
        MAX(h.note_id)                                    AS note_id,
        MAX(h.unit_id)                                    AS unit_id,
        MAX(h.campaign_id)                                AS campaign_id,
        MAX(SUBSTR(h.dt, 1, 10))                          AS dt,

        SUM(h.fee)                                        AS fee,
        SUM(h.impression)                                 AS impression,
        SUM(h.click)                                      AS click,
        SUM(h.`like`)                                     AS `like`,
        SUM(h.comment)                                    AS comment,
        SUM(h.collect)                                    AS collect,
        SUM(h.follow)                                     AS follow,
        SUM(h.share)                                      AS share,
        SUM(h.interaction)                                AS interaction,
        SUM(h.action_button_click)                        AS action_button_click,
        SUM(h.screenshot)                                 AS screenshot,
        SUM(h.pic_save)                                   AS pic_save,
        SUM(h.reserve_pv)                                 AS reserve_pv,
        SUM(h.video_play_5s_cnt)                          AS video_play_5s_cnt,

        SUM(CAST(GET_JSON_OBJECT(h.product_seeding_metrics, '$.search_cmt_click') AS BIGINT))       AS search_cmt_click,
        SUM(CAST(GET_JSON_OBJECT(h.product_seeding_metrics, '$.search_cmt_after_read') AS BIGINT))  AS search_cmt_after_read,
        SUM(CAST(GET_JSON_OBJECT(h.product_seeding_metrics, '$.i_user_num') AS BIGINT))             AS i_user_num,
        SUM(CAST(GET_JSON_OBJECT(h.product_seeding_metrics, '$.ti_user_num') AS BIGINT))            AS ti_user_num,

        SUM(CAST(GET_JSON_OBJECT(h.lead_collection_metrics, '$.leads') AS BIGINT))                  AS leads,
        SUM(CAST(GET_JSON_OBJECT(h.lead_collection_metrics, '$.landing_page_visit') AS BIGINT))     AS landing_page_visit,
        SUM(CAST(GET_JSON_OBJECT(h.lead_collection_metrics, '$.leads_button_impression') AS BIGINT)) AS leads_button_impression,
        SUM(CAST(GET_JSON_OBJECT(h.lead_collection_metrics, '$.message_user') AS BIGINT))           AS message_user,
        SUM(CAST(GET_JSON_OBJECT(h.lead_collection_metrics, '$.message') AS BIGINT))                AS message,
        SUM(CAST(GET_JSON_OBJECT(h.lead_collection_metrics, '$.message_consult') AS BIGINT))        AS message_consult,
        SUM(CAST(GET_JSON_OBJECT(h.lead_collection_metrics, '$.initiative_message') AS BIGINT))     AS initiative_message,
        SUM(CAST(GET_JSON_OBJECT(h.lead_collection_metrics, '$.msg_leads_num') AS BIGINT))          AS msg_leads_num,

        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.invoke_app_open_cnt') AS BIGINT))      AS invoke_app_open_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.invoke_app_enter_store_cnt') AS BIGINT)) AS invoke_app_enter_store_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.invoke_app_engagement_cnt') AS BIGINT)) AS invoke_app_engagement_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.invoke_app_payment_cnt') AS BIGINT))   AS invoke_app_payment_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.search_invoke_button_click_cnt') AS BIGINT)) AS search_invoke_button_click_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.invoke_app_payment_amount') AS DECIMAL(18,2))) AS invoke_app_payment_amount,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.app_activate_cnt') AS BIGINT))         AS app_activate_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.app_register_cnt') AS BIGINT))         AS app_register_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.first_app_pay_cnt') AS BIGINT))        AS first_app_pay_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.current_app_pay_cnt') AS BIGINT))      AS current_app_pay_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.app_key_action_cnt') AS BIGINT))       AS app_key_action_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.app_pay_cnt_7d') AS BIGINT))           AS app_pay_cnt_7d,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.app_pay_amount') AS DECIMAL(18,2)))    AS app_pay_amount,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.app_activate_amount_1d') AS DECIMAL(18,2))) AS app_activate_amount_1d,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.app_activate_amount_3d') AS DECIMAL(18,2))) AS app_activate_amount_3d,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.app_activate_amount_7d') AS DECIMAL(18,2))) AS app_activate_amount_7d,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.retention_1d_cnt') AS BIGINT))         AS retention_1d_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.retention_3d_cnt') AS BIGINT))         AS retention_3d_cnt,
        SUM(CAST(GET_JSON_OBJECT(h.app_promotion_metrics, '$.retention_7d_cnt') AS BIGINT))         AS retention_7d_cnt,

        SUM(CAST(GET_JSON_OBJECT(h.direct_seeding_metrics, '$.external_goods_visit_7') AS BIGINT))  AS external_goods_visit_7,
        SUM(CAST(GET_JSON_OBJECT(h.direct_seeding_metrics, '$.external_goods_order_7') AS BIGINT))  AS external_goods_order_7,
        SUM(CAST(GET_JSON_OBJECT(h.direct_seeding_metrics, '$.external_rgmv_7') AS DECIMAL(18,2)))  AS external_rgmv_7,
        SUM(CAST(GET_JSON_OBJECT(h.direct_seeding_metrics, '$.external_goods_order_15') AS BIGINT)) AS external_goods_order_15,
        SUM(CAST(GET_JSON_OBJECT(h.direct_seeding_metrics, '$.external_rgmv_15') AS DECIMAL(18,2))) AS external_rgmv_15,
        SUM(CAST(GET_JSON_OBJECT(h.direct_seeding_metrics, '$.external_goods_order_30') AS BIGINT)) AS external_goods_order_30,
        SUM(CAST(GET_JSON_OBJECT(h.direct_seeding_metrics, '$.external_rgmv_30') AS DECIMAL(18,2))) AS external_rgmv_30
    FROM dwd_xhs_creative_hi h
    CROSS JOIN (
        SELECT '${bizdate}' AS target_ds
        UNION ALL
        SELECT TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -1, 'dd'), 'yyyymmdd') AS target_ds
    ) dates
    INNER JOIN brg_xhs_note_project_df b
        ON h.note_id = b.note_id
        AND b.ds = dates.target_ds
    INNER JOIN dim_xhs_project_df p
        ON b.project_id = p.project_id
        AND p.ds = dates.target_ds
    WHERE h.ds >= REPLACE(p.valid_from, '-', '')
      AND h.ds <= REPLACE(LEAST(p.kpi_fetch_time, CONCAT(SUBSTR(dates.target_ds,1,4),'-',SUBSTR(dates.target_ds,5,2),'-',SUBSTR(dates.target_ds,7,2))), '-', '')
    GROUP BY dates.target_ds, h.creativity_id
) a
LEFT JOIN (
    -- conversion: 基于 brg 笔记 + 项目有效期，按 target_ds 分别累计
    SELECT /*+ MAPJOIN(dates) */
        cv.creativity_id,
        dates.target_ds,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.ad_offsite_active_uv ELSE 0 END)          AS 15d_ad_offsite_active_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.ad_offsite_task_cost ELSE 0 END)          AS 15d_ad_offsite_task_cost,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.ad_offsite_task_read_uv ELSE 0 END)       AS 15d_ad_offsite_task_read_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.ad_offsite_active_uv_dedup ELSE 0 END)    AS 15d_ad_offsite_active_uv_dedup,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.ad_offsite_task_cost_dedup ELSE 0 END)    AS 15d_ad_offsite_task_cost_dedup,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.ad_offsite_task_read_uv_dedup ELSE 0 END) AS 15d_ad_offsite_task_read_uv_dedup,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.ad_offsite_active_uv ELSE 0 END)          AS 30d_ad_offsite_active_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.ad_offsite_task_cost ELSE 0 END)          AS 30d_ad_offsite_task_cost,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.ad_offsite_task_read_uv ELSE 0 END)       AS 30d_ad_offsite_task_read_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.ad_offsite_active_uv_dedup ELSE 0 END)    AS 30d_ad_offsite_active_uv_dedup,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.ad_offsite_task_cost_dedup ELSE 0 END)    AS 30d_ad_offsite_task_cost_dedup,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.ad_offsite_task_read_uv_dedup ELSE 0 END) AS 30d_ad_offsite_task_read_uv_dedup
    FROM dwd_xhs_conversion_bycontent_di cv
    CROSS JOIN (
        SELECT '${bizdate}' AS target_ds
        UNION ALL
        SELECT TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -1, 'dd'), 'yyyymmdd') AS target_ds
    ) dates
    INNER JOIN brg_xhs_note_project_df b2
        ON cv.note_id = b2.note_id
        AND b2.ds = dates.target_ds
    INNER JOIN dim_xhs_project_df p2
        ON b2.project_id = p2.project_id
        AND p2.ds = dates.target_ds
    WHERE cv.ds >= REPLACE(p2.valid_from, '-', '')
      AND cv.ds <= REPLACE(LEAST(p2.kpi_fetch_time, CONCAT(SUBSTR(dates.target_ds,1,4),'-',SUBSTR(dates.target_ds,5,2),'-',SUBSTR(dates.target_ds,7,2))), '-', '')
    GROUP BY cv.creativity_id, dates.target_ds
) c
    ON a.creativity_id = c.creativity_id
    AND a.target_ds = c.target_ds
;
