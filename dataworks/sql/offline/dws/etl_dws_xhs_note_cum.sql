-- ============================================================
-- ETL: DWD → DWS 笔记日汇总（种草+转化）
-- 源表: dwd_xhs_note_cum, brg_xhs_note_project_df, dim_xhs_note_df, dim_xhs_ad_product_df, dim_xhs_task_group_df, dwd_xhs_conversion_bycontent_di
-- 目标表: dws_xhs_note_cum
-- 说明: 仅对桥表存在的笔记进行累计，JOIN 维度和转化（转化数据按归因周期聚合）
-- ============================================================

INSERT OVERWRITE TABLE dws_xhs_note_cum PARTITION (ds)
SELECT
    n.note_id,
    n.kol_name,
    d.task_group_id,                                      -- 来源于 dim_xhs_note_df
    d.ad_product_id,                                      -- 来源于 dim_xhs_note_df
    p.ad_product_name,                                    -- 来源于 dim_xhs_ad_product_df
    TRIM(d.content_theme)           AS content_theme,     -- 来源于 dim_xhs_note_df，清除空格
    p.product_category,                                   -- 来源于 dim_xhs_ad_product_df
    p.brand_name,                                         -- 来源于 dim_xhs_ad_product_df
    t.grass_alliance,                                     -- 来源于 dim_xhs_task_group_df
    n.dt,
    -- 金额指标
    n.kol_price,
    n.total_platform_price,
    n.pgy_actual_amt,
    -- 展现指标
    n.impression,
    n.read_num AS click,                                   -- 来源于 read_num(阅读量PV)
    -- 互动指标
    n.comment,
    n.collect,
    n.share,
    n.`like`,
    n.follow,
    n.interaction,
    -- 搜索指标
    n.search_read,
    n.search_impression,
    -- 推广指标
    n.promotion_read,
    n.promotion_impression,
    -- 加热指标
    n.heat_read,
    n.heat_impression,
    -- 发现指标
    n.discovery_impression,
    -- 组件指标
    n.comment_comp_impression,
    n.comment_comp_click,
    n.comment_comp_click_uv,
    n.content_comp_impression,
    n.content_comp_click,
    n.content_comp_click_uv,
    n.engage_comp_impression,
    n.engage_comp_click,
    n.note_bottom_comp_impression,
    n.note_bottom_comp_click,
    n.note_bottom_comp_click_uv,
    -- 搜索评论组件
    CASE WHEN n.comment_comp_type = '3' THEN n.comment_comp_impression ELSE 0 END
        + CASE WHEN n.content_comp_type = '2' THEN n.content_comp_impression ELSE 0 END AS search_cmt_impression,
    CASE WHEN n.comment_comp_type = '3' THEN n.comment_comp_click ELSE 0 END
        + CASE WHEN n.content_comp_type = '2' THEN n.content_comp_click ELSE 0 END AS search_cmt_click,
    -- 兴趣指标
    n.interest,
    n.feed_interest,
    n.search_interest,
    n.other_interest,
    n.cp,
    -- 转化 15d（来源于聚合子查询）
    c.15d_read_uv,
    c.15d_enter_shop_uv,
    c.15d_shop_new_visitor_uv,
    c.15d_shop_collect_uv,
    c.15d_add_cart_uv,
    c.15d_shop_follow_uv,
    c.15d_shop_member_uv,
    c.15d_shop_order_uv,
    c.15d_shop_order_gmv,
    c.15d_task_product_gmv,
    c.15d_task_product_new_customer_gmv,
    c.15d_non_task_product_gmv,
    c.15d_shop_new_customer_uv,
    c.15d_presale_deposit_gmv,
    c.15d_presale_estimated_gmv,
    c.15d_presale_deposit_uv,
    -- 转化 30d（来源于聚合子查询）
    c.30d_read_uv,
    c.30d_enter_shop_uv,
    c.30d_shop_new_visitor_uv,
    c.30d_shop_collect_uv,
    c.30d_add_cart_uv,
    c.30d_shop_follow_uv,
    c.30d_shop_member_uv,
    c.30d_shop_order_uv,
    c.30d_shop_order_gmv,
    c.30d_task_product_gmv,
    c.30d_task_product_new_customer_gmv,
    c.30d_non_task_product_gmv,
    c.30d_shop_new_customer_uv,
    c.30d_presale_deposit_gmv,
    c.30d_presale_estimated_gmv,
    c.30d_presale_deposit_uv,
    GETDATE() AS etl_time,
    -- 金额汇总（来源于 dws_xhs_creative_cum）
    ad.ad_fee,
    CAST(COALESCE(n.pgy_actual_amt, 0) + COALESCE(ad.ad_fee, 0) AS DECIMAL(18,2)) AS fee,
    n.read_num,                                              -- 阅读量PV
    n.ds                                                  AS ds                     -- 动态分区字段
FROM dwd_xhs_note_cum n
INNER JOIN brg_xhs_note_project_df b
    ON n.note_id = b.note_id
    AND b.ds = '${bizdate}'
LEFT JOIN dim_xhs_note_df d
    ON n.note_id = d.note_id
    AND d.ds = '${bizdate}'
LEFT JOIN dim_xhs_ad_product_df p
    ON d.ad_product_id = p.ad_product_id
    AND p.ds = '${bizdate}'
LEFT JOIN dim_xhs_task_group_df t
    ON d.task_group_id = t.task_group_id
    AND t.ds = '${bizdate}'
LEFT JOIN (
    -- 广告费用按 note_id+ds 预聚合（creative dt 与 note dt 可能差1天）
    SELECT note_id, ds,
           CAST(SUM(fee) AS DECIMAL(18,2)) AS ad_fee
    FROM dws_xhs_creative_cum
    WHERE ds = '${bizdate}'
    GROUP BY note_id, ds
) ad
    ON n.note_id = ad.note_id
    AND n.ds = ad.ds
LEFT JOIN (
    -- 转化数据历史累计（按项目时间范围汇总所有 ds，行转列 15d/30d）
    SELECT
        cv.note_id,
        -- 15d 归因
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
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.presale_deposit_gmv ELSE 0 END)          AS 15d_presale_deposit_gmv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.presale_estimated_gmv ELSE 0 END)        AS 15d_presale_estimated_gmv,
        SUM(CASE WHEN cv.attribution_period = '15' THEN cv.presale_deposit_uv ELSE 0 END)           AS 15d_presale_deposit_uv,
        -- 30d 归因
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
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.shop_new_customer_uv ELSE 0 END)         AS 30d_shop_new_customer_uv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.presale_deposit_gmv ELSE 0 END)          AS 30d_presale_deposit_gmv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.presale_estimated_gmv ELSE 0 END)        AS 30d_presale_estimated_gmv,
        SUM(CASE WHEN cv.attribution_period = '30' THEN cv.presale_deposit_uv ELSE 0 END)           AS 30d_presale_deposit_uv
    FROM dwd_xhs_conversion_bycontent_di cv
    INNER JOIN brg_xhs_note_project_df b2
        ON cv.note_id = b2.note_id
        AND b2.ds = '${bizdate}'
    INNER JOIN dim_xhs_project_df p2
        ON b2.project_id = p2.project_id
        AND p2.ds = '${bizdate}'
    WHERE cv.ds <= '${bizdate}'
      AND cv.ds >= REPLACE(p2.valid_from, '-', '')
      AND cv.ds <= REPLACE(LEAST(p2.kpi_fetch_time, TO_CHAR(TO_DATE('${bizdate}', 'yyyymmdd'), 'yyyy-mm-dd')), '-', '')
    GROUP BY cv.note_id
) c
    ON n.note_id = c.note_id
WHERE n.ds = '${bizdate}'
;
