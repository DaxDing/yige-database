-- ============================================================
-- ETL: DWS → DWS 内容主题日汇总
-- 源表: dws_xhs_note_1d_agg, dws_xhs_creative_1d_agg
-- 目标表: dws_xhs_content_theme_1d_agg
-- 说明: 按 content_theme + 产品维度 + dt 聚合，源表已过滤桥表存在的笔记
-- ============================================================

INSERT OVERWRITE TABLE dws_xhs_content_theme_1d_agg PARTITION (ds)
SELECT
    n.content_theme,
    n.ad_product_id,
    n.ad_product_name,
    n.product_category,
    n.brand_name,
    n.dt,
    -- 笔记数
    COUNT(DISTINCT n.note_id)                             AS note_cnt,
    -- 金额指标
    SUM(n.kol_price)                                      AS kol_price,
    SUM(n.total_platform_price)                           AS total_platform_price,
    CAST(SUM(n.pgy_actual_amt) AS DECIMAL(18,2))          AS pgy_actual_amt,
    SUM(c.fee)                                            AS ad_fee,
    SUM(COALESCE(n.pgy_actual_amt, 0) + COALESCE(c.fee, 0)) AS fee,
    -- 展现指标
    SUM(n.impression)                                     AS impression,
    SUM(n.click)                                          AS click,
    -- 互动指标
    SUM(n.comment)                                        AS comment,
    SUM(n.collect)                                        AS collect,
    SUM(n.share)                                          AS share,
    SUM(n.`like`)                                         AS `like`,
    SUM(n.follow)                                         AS follow,
    SUM(n.interaction)                                    AS interaction,
    -- 搜索指标
    SUM(n.search_read)                                    AS search_read,
    SUM(n.search_impression)                              AS search_impression,
    -- 推广指标
    SUM(n.promotion_read)                                 AS promotion_read,
    SUM(n.promotion_impression)                           AS promotion_impression,
    -- 加热指标
    SUM(n.heat_read)                                      AS heat_read,
    SUM(n.heat_impression)                                AS heat_impression,
    -- 发现指标
    SUM(n.discovery_impression)                           AS discovery_impression,
    -- 组件指标
    SUM(n.comment_comp_impression)                        AS comment_comp_impression,
    SUM(n.comment_comp_click)                             AS comment_comp_click,
    SUM(n.comment_comp_click_uv)                          AS comment_comp_click_uv,
    SUM(n.content_comp_impression)                        AS content_comp_impression,
    SUM(n.content_comp_click)                             AS content_comp_click,
    SUM(n.content_comp_click_uv)                          AS content_comp_click_uv,
    SUM(n.engage_comp_impression)                         AS engage_comp_impression,
    SUM(n.engage_comp_click)                              AS engage_comp_click,
    SUM(n.note_bottom_comp_impression)                    AS note_bottom_comp_impression,
    SUM(n.note_bottom_comp_click)                         AS note_bottom_comp_click,
    SUM(n.note_bottom_comp_click_uv)                      AS note_bottom_comp_click_uv,
    -- 搜索评论组件
    SUM(n.search_cmt_impression)                          AS search_cmt_impression,
    SUM(n.search_cmt_click)                               AS search_cmt_click,
    -- 兴趣指标
    SUM(n.interest)                                       AS interest,
    SUM(n.feed_interest)                                  AS feed_interest,
    SUM(n.search_interest)                                AS search_interest,
    SUM(n.other_interest)                                 AS other_interest,
    SUM(n.cp)                                             AS cp,
    -- 转化 15d
    SUM(n.15d_read_uv)                                    AS 15d_read_uv,
    SUM(n.15d_enter_shop_uv)                              AS 15d_enter_shop_uv,
    SUM(n.15d_shop_new_visitor_uv)                        AS 15d_shop_new_visitor_uv,
    SUM(n.15d_shop_collect_uv)                            AS 15d_shop_collect_uv,
    SUM(n.15d_add_cart_uv)                                    AS 15d_add_cart_uv,
    SUM(n.15d_shop_follow_uv)                             AS 15d_shop_follow_uv,
    SUM(n.15d_shop_member_uv)                             AS 15d_shop_member_uv,
    SUM(n.15d_shop_order_uv)                              AS 15d_shop_order_uv,
    SUM(n.15d_shop_order_gmv)                             AS 15d_shop_order_gmv,
    SUM(n.15d_task_product_gmv)                           AS 15d_task_product_gmv,
    SUM(n.15d_task_product_new_customer_gmv)              AS 15d_task_product_new_customer_gmv,
    SUM(n.15d_non_task_product_gmv)                       AS 15d_non_task_product_gmv,
    SUM(n.15d_shop_new_customer_uv)                       AS 15d_shop_new_customer_uv,
    SUM(n.15d_presale_deposit_gmv)                        AS 15d_presale_deposit_gmv,
    SUM(n.15d_presale_estimated_gmv)                      AS 15d_presale_estimated_gmv,
    SUM(n.15d_presale_deposit_uv)                         AS 15d_presale_deposit_uv,
    -- 转化 30d
    SUM(n.30d_read_uv)                                    AS 30d_read_uv,
    SUM(n.30d_enter_shop_uv)                              AS 30d_enter_shop_uv,
    SUM(n.30d_shop_new_visitor_uv)                        AS 30d_shop_new_visitor_uv,
    SUM(n.30d_shop_collect_uv)                            AS 30d_shop_collect_uv,
    SUM(n.30d_add_cart_uv)                                    AS 30d_add_cart_uv,
    SUM(n.30d_shop_follow_uv)                             AS 30d_shop_follow_uv,
    SUM(n.30d_shop_member_uv)                             AS 30d_shop_member_uv,
    SUM(n.30d_shop_order_uv)                              AS 30d_shop_order_uv,
    SUM(n.30d_shop_order_gmv)                             AS 30d_shop_order_gmv,
    SUM(n.30d_task_product_gmv)                           AS 30d_task_product_gmv,
    SUM(n.30d_task_product_new_customer_gmv)              AS 30d_task_product_new_customer_gmv,
    SUM(n.30d_non_task_product_gmv)                       AS 30d_non_task_product_gmv,
    SUM(n.30d_shop_new_customer_uv)                       AS 30d_shop_new_customer_uv,
    SUM(n.30d_presale_deposit_gmv)                        AS 30d_presale_deposit_gmv,
    SUM(n.30d_presale_estimated_gmv)                      AS 30d_presale_estimated_gmv,
    SUM(n.30d_presale_deposit_uv)                         AS 30d_presale_deposit_uv,
    -- 系统字段
    GETDATE()                                             AS etl_time,
    n.ds                                                  AS ds                     -- 动态分区字段
FROM dws_xhs_note_1d_agg n
LEFT JOIN (
    -- 按 note_id+dt+ds 预聚合，避免一对多扇出
    SELECT note_id, dt, ds,
           SUM(fee) AS fee
    FROM dws_xhs_creative_1d_agg
    WHERE ds >= TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -29, 'dd'), 'yyyymmdd')
      AND ds <= '${bizdate}'
    GROUP BY note_id, dt, ds
) c
    ON n.note_id = c.note_id
    AND n.dt = c.dt
    AND n.ds = c.ds
WHERE n.ds >= TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -29, 'dd'), 'yyyymmdd')
  AND n.ds <= '${bizdate}'
  AND n.content_theme IS NOT NULL
GROUP BY n.content_theme, n.ad_product_id, n.ad_product_name, n.product_category, n.brand_name, n.dt, n.ds
;
