-- ============================================================
-- ETL: DWS → DWS 项目日汇总（30天滚动累计）
-- 源表: dws_xhs_note_1d_agg, dwd_xhs_creative_hi, brg_xhs_note_project_df
-- 目标表: dws_xhs_project_1d_agg
-- 说明: 内层日汇总 → 外层窗口函数30天滚动累计
--       creative 改读 DWD 取日值，避免与累计 DWS 混用
-- ============================================================

INSERT OVERWRITE TABLE dws_xhs_project_1d_agg PARTITION (ds)
SELECT
    project_id,
    dt,
    -- 笔记数（保持日值，不累计）
    note_cnt,
    -- 金额指标（30天滚动累计）
    SUM(kol_price)              OVER w AS kol_price,
    SUM(total_platform_price)   OVER w AS total_platform_price,
    SUM(pgy_actual_amt)         OVER w AS pgy_actual_amt,
    SUM(ad_fee)                 OVER w AS ad_fee,
    SUM(fee)                    OVER w AS fee,
    -- 展现指标（30天滚动累计）
    SUM(impression)             OVER w AS impression,
    SUM(click)                  OVER w AS click,
    -- 互动指标（30天滚动累计）
    SUM(comment)                OVER w AS comment,
    SUM(collect)                OVER w AS collect,
    SUM(share)                  OVER w AS share,
    SUM(`like`)                 OVER w AS `like`,
    SUM(follow)                 OVER w AS follow,
    SUM(interaction)            OVER w AS interaction,
    -- 搜索指标
    SUM(search_read)            OVER w AS search_read,
    SUM(search_impression)      OVER w AS search_impression,
    -- 推广指标
    SUM(promotion_read)         OVER w AS promotion_read,
    SUM(promotion_impression)   OVER w AS promotion_impression,
    -- 加热指标
    SUM(heat_read)              OVER w AS heat_read,
    SUM(heat_impression)        OVER w AS heat_impression,
    -- 发现指标
    SUM(discovery_impression)   OVER w AS discovery_impression,
    -- 组件指标
    SUM(comment_comp_impression)     OVER w AS comment_comp_impression,
    SUM(comment_comp_click)          OVER w AS comment_comp_click,
    SUM(comment_comp_click_uv)       OVER w AS comment_comp_click_uv,
    SUM(content_comp_impression)     OVER w AS content_comp_impression,
    SUM(content_comp_click)          OVER w AS content_comp_click,
    SUM(content_comp_click_uv)       OVER w AS content_comp_click_uv,
    SUM(engage_comp_impression)      OVER w AS engage_comp_impression,
    SUM(engage_comp_click)           OVER w AS engage_comp_click,
    SUM(note_bottom_comp_impression) OVER w AS note_bottom_comp_impression,
    SUM(note_bottom_comp_click)      OVER w AS note_bottom_comp_click,
    SUM(note_bottom_comp_click_uv)   OVER w AS note_bottom_comp_click_uv,
    -- 搜索评论组件
    SUM(search_cmt_impression)  OVER w AS search_cmt_impression,
    SUM(search_cmt_click)       OVER w AS search_cmt_click,
    -- 兴趣指标
    SUM(interest)               OVER w AS interest,
    SUM(feed_interest)          OVER w AS feed_interest,
    SUM(search_interest)        OVER w AS search_interest,
    SUM(other_interest)         OVER w AS other_interest,
    SUM(cp)                     OVER w AS cp,
    -- 转化 15d
    SUM(15d_read_uv)            OVER w AS 15d_read_uv,
    SUM(15d_enter_shop_uv)      OVER w AS 15d_enter_shop_uv,
    SUM(15d_shop_new_visitor_uv) OVER w AS 15d_shop_new_visitor_uv,
    SUM(15d_shop_collect_uv)    OVER w AS 15d_shop_collect_uv,
    SUM(15d_add_cart_uv)        OVER w AS 15d_add_cart_uv,
    SUM(15d_shop_follow_uv)     OVER w AS 15d_shop_follow_uv,
    SUM(15d_shop_member_uv)     OVER w AS 15d_shop_member_uv,
    SUM(15d_shop_order_uv)      OVER w AS 15d_shop_order_uv,
    SUM(15d_shop_order_gmv)     OVER w AS 15d_shop_order_gmv,
    SUM(15d_task_product_gmv)   OVER w AS 15d_task_product_gmv,
    SUM(15d_task_product_new_customer_gmv) OVER w AS 15d_task_product_new_customer_gmv,
    SUM(15d_non_task_product_gmv) OVER w AS 15d_non_task_product_gmv,
    SUM(15d_shop_new_customer_uv) OVER w AS 15d_shop_new_customer_uv,
    SUM(15d_presale_deposit_gmv)  OVER w AS 15d_presale_deposit_gmv,
    SUM(15d_presale_estimated_gmv) OVER w AS 15d_presale_estimated_gmv,
    SUM(15d_presale_deposit_uv)   OVER w AS 15d_presale_deposit_uv,
    -- 转化 30d
    SUM(30d_read_uv)            OVER w AS 30d_read_uv,
    SUM(30d_enter_shop_uv)      OVER w AS 30d_enter_shop_uv,
    SUM(30d_shop_new_visitor_uv) OVER w AS 30d_shop_new_visitor_uv,
    SUM(30d_shop_collect_uv)    OVER w AS 30d_shop_collect_uv,
    SUM(30d_add_cart_uv)        OVER w AS 30d_add_cart_uv,
    SUM(30d_shop_follow_uv)     OVER w AS 30d_shop_follow_uv,
    SUM(30d_shop_member_uv)     OVER w AS 30d_shop_member_uv,
    SUM(30d_shop_order_uv)      OVER w AS 30d_shop_order_uv,
    SUM(30d_shop_order_gmv)     OVER w AS 30d_shop_order_gmv,
    SUM(30d_task_product_gmv)   OVER w AS 30d_task_product_gmv,
    SUM(30d_task_product_new_customer_gmv) OVER w AS 30d_task_product_new_customer_gmv,
    SUM(30d_non_task_product_gmv) OVER w AS 30d_non_task_product_gmv,
    SUM(30d_shop_new_customer_uv) OVER w AS 30d_shop_new_customer_uv,
    SUM(30d_presale_deposit_gmv)  OVER w AS 30d_presale_deposit_gmv,
    SUM(30d_presale_estimated_gmv) OVER w AS 30d_presale_estimated_gmv,
    SUM(30d_presale_deposit_uv)   OVER w AS 30d_presale_deposit_uv,
    -- 系统字段
    GETDATE() AS etl_time,
    ds
FROM (
    -- ========== 内层：日汇总（所有源均为日值） ==========
    SELECT
        b.project_id,
        n.dt,
        COUNT(DISTINCT n.note_id)                             AS note_cnt,
        -- 金额
        SUM(n.kol_price)                                      AS kol_price,
        SUM(n.total_platform_price)                           AS total_platform_price,
        CAST(SUM(n.pgy_actual_amt) AS DECIMAL(18,2))          AS pgy_actual_amt,
        SUM(c.fee)                                            AS ad_fee,
        SUM(COALESCE(n.pgy_actual_amt, 0) + COALESCE(c.fee, 0)) AS fee,
        -- 展现（is_proxy=TRUE 使用 creative）
        SUM(CASE WHEN b.is_proxy = TRUE THEN c.impression ELSE n.impression END)   AS impression,
        SUM(CASE WHEN b.is_proxy = TRUE THEN c.click ELSE n.click END)             AS click,
        -- 互动（is_proxy=TRUE 使用 creative）
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
        SUM(CASE WHEN b.is_proxy = TRUE THEN c.search_cmt_click ELSE n.search_cmt_click END) AS search_cmt_click,
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
        -- 分区
        n.ds
    FROM dws_xhs_note_1d_agg n
    INNER JOIN brg_xhs_note_project_df b
        ON n.note_id = b.note_id
        AND b.ds = '${bizdate}'
    LEFT JOIN (
        -- creative 改读 DWD 取日值（DWS 已是累计，不能直接用）
        SELECT note_id, SUBSTR(dt, 1, 10) AS dt, ds,
               SUM(fee)         AS fee,
               SUM(impression)  AS impression,
               SUM(click)       AS click,
               SUM(comment)     AS comment,
               SUM(collect)     AS collect,
               SUM(share)       AS share,
               SUM(`like`)      AS `like`,
               SUM(follow)      AS follow,
               SUM(interaction) AS interaction,
               SUM(CAST(GET_JSON_OBJECT(product_seeding_metrics, '$.search_cmt_click') AS BIGINT)) AS search_cmt_click
        FROM dwd_xhs_creative_hi
        WHERE ds >= TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -29, 'dd'), 'yyyymmdd')
          AND ds <= '${bizdate}'
        GROUP BY note_id, SUBSTR(dt, 1, 10), ds
    ) c
        ON n.note_id = c.note_id
        AND n.dt = c.dt
        AND n.ds = c.ds
    WHERE n.ds >= TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -29, 'dd'), 'yyyymmdd')
      AND n.ds <= '${bizdate}'
    GROUP BY b.project_id, n.dt, n.ds
) daily
WINDOW w AS (PARTITION BY project_id ORDER BY ds)
;
