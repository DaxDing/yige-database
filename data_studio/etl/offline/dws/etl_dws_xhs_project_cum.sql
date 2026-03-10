-- ============================================================
-- ETL: DWS → DWS 项目累计表
-- 源表: dws_xhs_note_cum, dwd_xhs_creative_hi, brg_xhs_note_project_df, dim_xhs_project_df
-- 目标表: dws_xhs_project_cum
-- 说明: note_cum 已是历史累计，按 project 聚合即可；ad_fee/fee 直接来源 note_cum
--       creative 直接从 dwd 聚合项目时间段内数据（替代 dws_xhs_creative_cum + ADS 差值）
--       仅用于 is_proxy 展现/互动指标
--       输出粒度: project_id + dt + ds
-- ============================================================

INSERT OVERWRITE TABLE dws_xhs_project_cum PARTITION (ds)
SELECT
    b.project_id,
    n.dt,
    -- 笔记数
    COUNT(DISTINCT n.note_id)                             AS note_cnt,
    -- 金额指标
    SUM(n.kol_price)                                      AS kol_price,
    SUM(n.total_platform_price)                           AS total_platform_price,
    CAST(SUM(CASE WHEN b.is_proxy = FALSE THEN n.pgy_actual_amt ELSE 0 END) AS DECIMAL(18,2)) AS pgy_actual_amt,
    SUM(n.ad_fee)                                         AS ad_fee,
    CAST(SUM(CASE WHEN b.is_proxy = FALSE THEN COALESCE(n.pgy_actual_amt, 0) ELSE 0 END) + SUM(COALESCE(n.ad_fee, 0)) AS DECIMAL(18,2)) AS fee,
    -- 展现（is_proxy=TRUE 仅用 creative，FALSE 仅用 note）
    SUM(CASE WHEN b.is_proxy = TRUE THEN c.impression ELSE n.impression END)   AS impression,
    SUM(CASE WHEN b.is_proxy = TRUE THEN c.click ELSE n.click END)             AS click,
    -- 互动（is_proxy=TRUE 仅用 creative，FALSE 仅用 note）
    SUM(CASE WHEN b.is_proxy = TRUE THEN c.comment ELSE n.comment END)         AS comment,
    SUM(CASE WHEN b.is_proxy = TRUE THEN c.collect ELSE n.collect END)         AS collect,
    SUM(CASE WHEN b.is_proxy = TRUE THEN c.share ELSE n.share END)             AS share,
    SUM(CASE WHEN b.is_proxy = TRUE THEN c.`like` ELSE n.`like` END)           AS `like`,
    SUM(CASE WHEN b.is_proxy = TRUE THEN c.follow ELSE n.follow END)           AS follow,
    SUM(CASE WHEN b.is_proxy = TRUE THEN c.interaction ELSE n.interaction END) AS interaction,
    -- 搜索
    SUM(n.search_read)                                    AS search_read,
    SUM(n.search_impression)                              AS search_impression,
    -- 推广
    SUM(n.promotion_read)                                 AS promotion_read,
    SUM(n.promotion_impression)                           AS promotion_impression,
    -- 加热
    SUM(n.heat_read)                                      AS heat_read,
    SUM(n.heat_impression)                                AS heat_impression,
    -- 发现
    SUM(n.discovery_impression)                           AS discovery_impression,
    -- 组件
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
    -- 兴趣
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
    SUM(n.15d_add_cart_uv)                                AS 15d_add_cart_uv,
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
    SUM(n.30d_add_cart_uv)                                AS 30d_add_cart_uv,
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
    GETDATE() AS etl_time,
    -- 直投笔记搜索组件（仅 is_proxy=FALSE）
    SUM(CASE WHEN b.is_proxy = FALSE THEN n.search_cmt_impression ELSE 0 END) AS new_search_cmt_impression,
    SUM(CASE WHEN b.is_proxy = FALSE THEN n.search_cmt_click ELSE 0 END)      AS new_search_cmt_click,
    n.ds
FROM dws_xhs_note_cum n
INNER JOIN brg_xhs_note_project_df b
    ON n.note_id = b.note_id
    AND b.ds = '${bizdate}'
LEFT JOIN (
    -- creative 按 project_id+note_id 聚合项目时间段内数据（替代 dws_xhs_creative_cum + ADS 差值）
    SELECT b2.project_id, cr.note_id,
           SUM(cr.impression)  AS impression,
           SUM(cr.click)       AS click,
           SUM(cr.`comment`)   AS `comment`,
           SUM(cr.collect)     AS collect,
           SUM(cr.share)       AS share,
           SUM(cr.`like`)      AS `like`,
           SUM(cr.follow)      AS follow,
           SUM(cr.interaction) AS interaction
    FROM dwd_xhs_creative_hi cr
    INNER JOIN brg_xhs_note_project_df b2
        ON cr.note_id = b2.note_id
        AND b2.ds = '${bizdate}'
    INNER JOIN dim_xhs_project_df p
        ON b2.project_id = p.project_id
        AND p.ds = '${bizdate}'
    WHERE cr.ds <= '${bizdate}'
      AND cr.ds >= REPLACE(p.valid_from, '-', '')
      AND cr.ds <= REPLACE(LEAST(p.kpi_fetch_time, TO_CHAR(TO_DATE('${bizdate}', 'yyyymmdd'), 'yyyy-mm-dd')), '-', '')
    GROUP BY b2.project_id, cr.note_id
) c
    ON b.project_id = c.project_id
    AND n.note_id = c.note_id
WHERE n.ds IN ('${bizdate}', TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -1, 'dd'), 'yyyymmdd'))
GROUP BY b.project_id, n.dt, n.ds
;
