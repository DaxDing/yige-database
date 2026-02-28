-- ============================================================
-- ETL: DWS → DWS 任务组累计表
-- 源表: dws_xhs_note_cum（笔记指标按任务组聚合）
--       dwd_xhs_conversion_bytask_di（任务维度转化数据）
--       dim_xhs_task_group_df, brg_xhs_note_project_df
-- 目标表: dws_xhs_task_group_cum
-- 说明: 笔记指标从 dws_xhs_note_cum 按 task_group_id 聚合；
--       转化指标从 dwd_xhs_conversion_bytask_di 按 task_id→task_group_id 聚合；
--       pgy_actual_amt/fee 仅计 is_proxy=FALSE 的笔记（与 project_cum 一致）
-- ============================================================

INSERT OVERWRITE TABLE dws_xhs_task_group_cum PARTITION (ds='${bizdate}')
SELECT
    n.task_group_id,
    n.task_group_name,
    n.ad_product_name,
    n.grass_alliance,
    n.dt,

    -- ============ 笔记指标（聚合） ============
    n.note_cnt,
    n.kol_price,
    n.pgy_actual_amt,
    n.ad_fee,
    n.fee,
    n.impression,
    n.click,
    n.interaction,
    n.collect,
    n.follow,
    n.search_cmt_impression,
    n.search_cmt_click,

    -- ============ 转化 15d ============
    COALESCE(c.15d_read_uv, 0)                      AS 15d_read_uv,
    COALESCE(c.15d_enter_shop_uv, 0)                AS 15d_enter_shop_uv,
    COALESCE(c.15d_shop_new_visitor_uv, 0)          AS 15d_shop_new_visitor_uv,
    COALESCE(c.15d_shop_collect_uv, 0)              AS 15d_shop_collect_uv,
    COALESCE(c.15d_add_cart_uv, 0)                  AS 15d_add_cart_uv,
    COALESCE(c.15d_shop_follow_uv, 0)               AS 15d_shop_follow_uv,
    COALESCE(c.15d_shop_member_uv, 0)               AS 15d_shop_member_uv,
    COALESCE(c.15d_shop_order_uv, 0)                AS 15d_shop_order_uv,
    COALESCE(c.15d_shop_order_gmv, 0)               AS 15d_shop_order_gmv,
    COALESCE(c.15d_task_product_gmv, 0)             AS 15d_task_product_gmv,
    COALESCE(c.15d_task_product_new_customer_gmv, 0) AS 15d_task_product_new_customer_gmv,
    COALESCE(c.15d_non_task_product_gmv, 0)         AS 15d_non_task_product_gmv,
    COALESCE(c.15d_shop_new_customer_uv, 0)         AS 15d_shop_new_customer_uv,

    -- ============ 转化 30d ============
    COALESCE(c.30d_read_uv, 0)                      AS 30d_read_uv,
    COALESCE(c.30d_enter_shop_uv, 0)                AS 30d_enter_shop_uv,
    COALESCE(c.30d_shop_new_visitor_uv, 0)          AS 30d_shop_new_visitor_uv,
    COALESCE(c.30d_shop_collect_uv, 0)              AS 30d_shop_collect_uv,
    COALESCE(c.30d_add_cart_uv, 0)                  AS 30d_add_cart_uv,
    COALESCE(c.30d_shop_follow_uv, 0)               AS 30d_shop_follow_uv,
    COALESCE(c.30d_shop_member_uv, 0)               AS 30d_shop_member_uv,
    COALESCE(c.30d_shop_order_uv, 0)                AS 30d_shop_order_uv,
    COALESCE(c.30d_shop_order_gmv, 0)               AS 30d_shop_order_gmv,
    COALESCE(c.30d_task_product_gmv, 0)             AS 30d_task_product_gmv,
    COALESCE(c.30d_task_product_new_customer_gmv, 0) AS 30d_task_product_new_customer_gmv,
    COALESCE(c.30d_non_task_product_gmv, 0)         AS 30d_non_task_product_gmv,
    COALESCE(c.30d_shop_new_customer_uv, 0)         AS 30d_shop_new_customer_uv,

    GETDATE() AS etl_time

FROM (
    -- 笔记指标按任务组聚合（pgy_actual_amt/fee 仅计 is_proxy=FALSE）
    SELECT
        e.task_group_id,
        MAX(t.task_group_name)                       AS task_group_name,
        CONCAT_WS(',', SORT_ARRAY(COLLECT_SET(e.ad_product_name))) AS ad_product_name,
        MAX(e.grass_alliance)                        AS grass_alliance,
        MAX(e.dt)                                    AS dt,
        COUNT(DISTINCT e.note_id)                    AS note_cnt,
        SUM(COALESCE(e.kol_price, 0))               AS kol_price,
        CAST(SUM(CASE WHEN b.is_proxy = FALSE THEN COALESCE(e.pgy_actual_amt, 0) ELSE 0 END) AS DECIMAL(38,2)) AS pgy_actual_amt,
        SUM(COALESCE(e.ad_fee, 0))                   AS ad_fee,
        CAST(SUM(CASE WHEN b.is_proxy = FALSE THEN COALESCE(e.pgy_actual_amt, 0) ELSE 0 END) + SUM(COALESCE(e.ad_fee, 0)) AS DECIMAL(38,2)) AS fee,
        SUM(COALESCE(e.impression, 0))               AS impression,
        SUM(COALESCE(e.click, 0))                    AS click,
        SUM(COALESCE(e.interaction, 0))              AS interaction,
        SUM(COALESCE(e.collect, 0))                  AS collect,
        SUM(COALESCE(e.follow, 0))                   AS follow,
        SUM(COALESCE(e.search_cmt_impression, 0))    AS search_cmt_impression,
        SUM(COALESCE(e.search_cmt_click, 0))         AS search_cmt_click
    FROM dws_xhs_note_cum e
    INNER JOIN brg_xhs_note_project_df b
        ON e.note_id = b.note_id
        AND b.ds = '${bizdate}'
    LEFT JOIN dim_xhs_task_group_df t
        ON e.task_group_id = t.task_group_id
        AND t.ds = '${bizdate}'
    WHERE e.ds = '${bizdate}'
      AND e.task_group_id IS NOT NULL
    GROUP BY e.task_group_id
) n
LEFT JOIN (
    -- 转化数据按 task_id→task_group_id 聚合，行转列 15d/30d
    -- project_id 通过笔记路径获取（dim_xhs_task_group_df.project_id 可能为 NULL）
    -- 时间范围: valid_from ~ MIN(kpi_fetch_time, bizdate)
    SELECT
        t.task_group_id,
        -- 15d
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.read_uv ELSE 0 END)                      AS 15d_read_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.enter_shop_uv ELSE 0 END)                AS 15d_enter_shop_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.shop_new_visitor_uv ELSE 0 END)          AS 15d_shop_new_visitor_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.shop_collect_uv ELSE 0 END)              AS 15d_shop_collect_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.add_cart_uv ELSE 0 END)                  AS 15d_add_cart_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.shop_follow_uv ELSE 0 END)               AS 15d_shop_follow_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.shop_member_uv ELSE 0 END)               AS 15d_shop_member_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.shop_order_uv ELSE 0 END)                AS 15d_shop_order_uv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.shop_order_gmv ELSE 0 END)               AS 15d_shop_order_gmv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.task_product_gmv ELSE 0 END)             AS 15d_task_product_gmv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.task_product_new_customer_gmv ELSE 0 END) AS 15d_task_product_new_customer_gmv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.non_task_product_gmv ELSE 0 END)         AS 15d_non_task_product_gmv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.shop_new_customer_uv ELSE 0 END)         AS 15d_shop_new_customer_uv,
        -- 30d
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.read_uv ELSE 0 END)                      AS 30d_read_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.enter_shop_uv ELSE 0 END)                AS 30d_enter_shop_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.shop_new_visitor_uv ELSE 0 END)          AS 30d_shop_new_visitor_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.shop_collect_uv ELSE 0 END)              AS 30d_shop_collect_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.add_cart_uv ELSE 0 END)                  AS 30d_add_cart_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.shop_follow_uv ELSE 0 END)               AS 30d_shop_follow_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.shop_member_uv ELSE 0 END)               AS 30d_shop_member_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.shop_order_uv ELSE 0 END)                AS 30d_shop_order_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.shop_order_gmv ELSE 0 END)               AS 30d_shop_order_gmv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.task_product_gmv ELSE 0 END)             AS 30d_task_product_gmv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.task_product_new_customer_gmv ELSE 0 END) AS 30d_task_product_new_customer_gmv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.non_task_product_gmv ELSE 0 END)         AS 30d_non_task_product_gmv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.shop_new_customer_uv ELSE 0 END)         AS 30d_shop_new_customer_uv
    FROM dwd_xhs_conversion_bytask_di cv
    INNER JOIN dim_xhs_task_group_df t
        ON cv.task_id = t.task_id
        AND t.ds = '${bizdate}'
    INNER JOIN dim_xhs_project_df p
        ON t.project_id = p.project_id
        AND p.ds = '${bizdate}'
    WHERE cv.ds <= '${bizdate}'
      AND cv.ds >= REPLACE(p.valid_from, '-', '')
      AND cv.ds <= REPLACE(LEAST(p.kpi_fetch_time, TO_CHAR(TO_DATE('${bizdate}', 'yyyymmdd'), 'yyyy-mm-dd')), '-', '')
    GROUP BY t.task_group_id
) c
    ON n.task_group_id = c.task_group_id
;
