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
    d.content_theme,                                      -- 来源于 dim_xhs_note_df
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
    n.read_uv AS click,                                   -- 来源于 read_uv
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
    -- 转化数据按 note_id+dt+ds 聚合，行转列（15d/30d）
    SELECT
        note_id,
        dt,
        ds,
        -- 15d 归因
        MAX(CASE WHEN attribution_period = '15' THEN read_uv END)                      AS 15d_read_uv,
        MAX(CASE WHEN attribution_period = '15' THEN enter_shop_uv END)                AS 15d_enter_shop_uv,
        MAX(CASE WHEN attribution_period = '15' THEN shop_new_visitor_uv END)          AS 15d_shop_new_visitor_uv,
        MAX(CASE WHEN attribution_period = '15' THEN shop_collect_uv END)              AS 15d_shop_collect_uv,
        MAX(CASE WHEN attribution_period = '15' THEN add_cart_uv END)                      AS 15d_add_cart_uv,
        MAX(CASE WHEN attribution_period = '15' THEN shop_follow_uv END)               AS 15d_shop_follow_uv,
        MAX(CASE WHEN attribution_period = '15' THEN shop_member_uv END)               AS 15d_shop_member_uv,
        MAX(CASE WHEN attribution_period = '15' THEN shop_order_uv END)                AS 15d_shop_order_uv,
        MAX(CASE WHEN attribution_period = '15' THEN shop_order_gmv END)               AS 15d_shop_order_gmv,
        MAX(CASE WHEN attribution_period = '15' THEN task_product_gmv END)             AS 15d_task_product_gmv,
        MAX(CASE WHEN attribution_period = '15' THEN task_product_new_customer_gmv END) AS 15d_task_product_new_customer_gmv,
        MAX(CASE WHEN attribution_period = '15' THEN non_task_product_gmv END)         AS 15d_non_task_product_gmv,
        MAX(CASE WHEN attribution_period = '15' THEN shop_new_customer_uv END)         AS 15d_shop_new_customer_uv,
        MAX(CASE WHEN attribution_period = '15' THEN presale_deposit_gmv END)          AS 15d_presale_deposit_gmv,
        MAX(CASE WHEN attribution_period = '15' THEN presale_estimated_gmv END)        AS 15d_presale_estimated_gmv,
        MAX(CASE WHEN attribution_period = '15' THEN presale_deposit_uv END)           AS 15d_presale_deposit_uv,
        -- 30d 归因
        MAX(CASE WHEN attribution_period = '30' THEN read_uv END)                      AS 30d_read_uv,
        MAX(CASE WHEN attribution_period = '30' THEN enter_shop_uv END)                AS 30d_enter_shop_uv,
        MAX(CASE WHEN attribution_period = '30' THEN shop_new_visitor_uv END)          AS 30d_shop_new_visitor_uv,
        MAX(CASE WHEN attribution_period = '30' THEN shop_collect_uv END)              AS 30d_shop_collect_uv,
        MAX(CASE WHEN attribution_period = '30' THEN add_cart_uv END)                      AS 30d_add_cart_uv,
        MAX(CASE WHEN attribution_period = '30' THEN shop_follow_uv END)               AS 30d_shop_follow_uv,
        MAX(CASE WHEN attribution_period = '30' THEN shop_member_uv END)               AS 30d_shop_member_uv,
        MAX(CASE WHEN attribution_period = '30' THEN shop_order_uv END)                AS 30d_shop_order_uv,
        MAX(CASE WHEN attribution_period = '30' THEN shop_order_gmv END)               AS 30d_shop_order_gmv,
        MAX(CASE WHEN attribution_period = '30' THEN task_product_gmv END)             AS 30d_task_product_gmv,
        MAX(CASE WHEN attribution_period = '30' THEN task_product_new_customer_gmv END) AS 30d_task_product_new_customer_gmv,
        MAX(CASE WHEN attribution_period = '30' THEN non_task_product_gmv END)         AS 30d_non_task_product_gmv,
        MAX(CASE WHEN attribution_period = '30' THEN shop_new_customer_uv END)         AS 30d_shop_new_customer_uv,
        MAX(CASE WHEN attribution_period = '30' THEN presale_deposit_gmv END)          AS 30d_presale_deposit_gmv,
        MAX(CASE WHEN attribution_period = '30' THEN presale_estimated_gmv END)        AS 30d_presale_estimated_gmv,
        MAX(CASE WHEN attribution_period = '30' THEN presale_deposit_uv END)           AS 30d_presale_deposit_uv
    FROM dwd_xhs_conversion_bycontent_di
    WHERE ds >= TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -29, 'dd'), 'yyyymmdd')
      AND ds <= '${bizdate}'
    GROUP BY note_id, dt, ds
) c
    ON n.note_id = c.note_id
    AND n.dt = c.dt
    AND n.ds = c.ds
WHERE n.ds >= TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -29, 'dd'), 'yyyymmdd')
  AND n.ds <= '${bizdate}'
;
