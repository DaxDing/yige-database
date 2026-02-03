-- ============================================================
-- ETL: DWS → ADS 笔记内容种草日汇总
-- 源表: dws_xhs_note_cum, brg_xhs_note_project_df, dim_xhs_project_df
-- 目标表: ads_xhs_note_bycontent_daily_agg
-- 说明: 基于项目有效期做累计差值（结束 - 开始），按笔记维度聚合
-- ============================================================

INSERT OVERWRITE TABLE ads_xhs_note_bycontent_daily_agg PARTITION (ds)
SELECT /*+ MAPJOIN(attr) */
    -- ============ 维度字段 ============
    b.project_id,
    attr.attribution_period,
    CAST(b.ds AS BIGINT)                                                          AS dt,
    e.brand_name,
    e.product_category,
    e.ad_product_name                                                               AS delivery_product,
    e.kol_name,
    b.note_id,

    -- ============ 金额指标 ============
    CAST(COALESCE(e.fee, 0) - COALESCE(s.fee, 0) AS DECIMAL(20,6))                   AS fee,
    CAST(COALESCE(e.ad_fee, 0) - COALESCE(s.ad_fee, 0) AS DECIMAL(20,6))             AS ad_fee,
    CAST(COALESCE(e.pgy_actual_amt, 0) - COALESCE(s.pgy_actual_amt, 0) AS BIGINT)    AS kols_fee,

    -- ============ 笔记数 ============
    1                                                                              AS note_count,

    -- ============ 曝光-点击指标 ============
    CAST(COALESCE(e.impression, 0) - COALESCE(s.impression, 0) AS BIGINT)         AS impression,
    CAST(COALESCE(e.click, 0) - COALESCE(s.click, 0) AS BIGINT)                  AS read_uv,

    -- ============ 互动指标 ============
    CAST(COALESCE(e.interaction, 0) - COALESCE(s.interaction, 0) AS BIGINT)       AS interaction,

    -- ============ 派生指标（效率） ============
    -- CPM
    CAST(CASE WHEN (COALESCE(e.impression, 0) - COALESCE(s.impression, 0)) > 0
         THEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) * 1000.0 / (COALESCE(e.impression, 0) - COALESCE(s.impression, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS cpm,
    -- CPE
    CAST(CASE WHEN (COALESCE(e.interaction, 0) - COALESCE(s.interaction, 0)) > 0
         THEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) * 1.0 / (COALESCE(e.interaction, 0) - COALESCE(s.interaction, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS cpe,
    -- CPC
    CAST(CASE WHEN (COALESCE(e.click, 0) - COALESCE(s.click, 0)) > 0
         THEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) * 1.0 / (COALESCE(e.click, 0) - COALESCE(s.click, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS cpc,
    -- CTR
    CAST(CASE WHEN (COALESCE(e.impression, 0) - COALESCE(s.impression, 0)) > 0
         THEN (COALESCE(e.click, 0) - COALESCE(s.click, 0)) * 1.0 / (COALESCE(e.impression, 0) - COALESCE(s.impression, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS ctr,
    -- 搜索组件CTR
    CAST(CASE WHEN (COALESCE(e.search_cmt_impression, 0) - COALESCE(s.search_cmt_impression, 0)) > 0
         THEN (COALESCE(e.search_cmt_click, 0) - COALESCE(s.search_cmt_click, 0)) * 1.0 / (COALESCE(e.search_cmt_impression, 0) - COALESCE(s.search_cmt_impression, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS search_cmt_click_ctr,
    -- CPUV（费用 / 进店UV）
    CAST(CASE WHEN attr.attribution_period = '15' AND (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) * 1.0 / (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0))
         WHEN attr.attribution_period = '30' AND (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) * 1.0 / (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS cpuv,

    -- ============ 转化指标（按归因口径） ============
    -- 进店率
    CAST(CASE WHEN (COALESCE(e.click, 0) - COALESCE(s.click, 0)) > 0
         THEN CASE WHEN attr.attribution_period = '15' THEN (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0)) * 1.0 / (COALESCE(e.click, 0) - COALESCE(s.click, 0))
                   ELSE (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0)) * 1.0 / (COALESCE(e.click, 0) - COALESCE(s.click, 0)) END
         ELSE 0 END AS DECIMAL(20,6))                                             AS enter_shop_rate,
    -- 进店UV
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0)
         ELSE COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0) END AS BIGINT) AS enter_shop_uv,
    -- 新访客率
    CAST(CASE WHEN attr.attribution_period = '15' AND (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.15d_shop_new_visitor_uv, 0) - COALESCE(s.15d_shop_new_visitor_uv, 0)) * 1.0 / (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0))
         WHEN attr.attribution_period = '30' AND (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.30d_shop_new_visitor_uv, 0) - COALESCE(s.30d_shop_new_visitor_uv, 0)) * 1.0 / (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS new_visitor_rate,
    -- 店铺新访客
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_shop_new_visitor_uv, 0) - COALESCE(s.15d_shop_new_visitor_uv, 0)
         ELSE COALESCE(e.30d_shop_new_visitor_uv, 0) - COALESCE(s.30d_shop_new_visitor_uv, 0) END AS BIGINT) AS shop_new_visitor_uv,
    -- 转化率
    CAST(CASE WHEN attr.attribution_period = '15' AND (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.15d_shop_order_uv, 0) - COALESCE(s.15d_shop_order_uv, 0)) * 1.0 / (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0))
         WHEN attr.attribution_period = '30' AND (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.30d_shop_order_uv, 0) - COALESCE(s.30d_shop_order_uv, 0)) * 1.0 / (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS conversion_rate,
    -- 全店成交UV
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_shop_order_uv, 0) - COALESCE(s.15d_shop_order_uv, 0)
         ELSE COALESCE(e.30d_shop_order_uv, 0) - COALESCE(s.30d_shop_order_uv, 0) END AS BIGINT) AS shop_order_uv,
    -- 客单价
    CAST(CASE WHEN attr.attribution_period = '15' AND (COALESCE(e.15d_shop_order_uv, 0) - COALESCE(s.15d_shop_order_uv, 0)) > 0
         THEN (COALESCE(e.15d_shop_order_gmv, 0) - COALESCE(s.15d_shop_order_gmv, 0)) * 1.0 / (COALESCE(e.15d_shop_order_uv, 0) - COALESCE(s.15d_shop_order_uv, 0))
         WHEN attr.attribution_period = '30' AND (COALESCE(e.30d_shop_order_uv, 0) - COALESCE(s.30d_shop_order_uv, 0)) > 0
         THEN (COALESCE(e.30d_shop_order_gmv, 0) - COALESCE(s.30d_shop_order_gmv, 0)) * 1.0 / (COALESCE(e.30d_shop_order_uv, 0) - COALESCE(s.30d_shop_order_uv, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS average_order_value,
    -- UV价值（RPV）
    CAST(CASE WHEN attr.attribution_period = '15' AND (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.15d_shop_order_gmv, 0) - COALESCE(s.15d_shop_order_gmv, 0)) * 1.0 / (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0))
         WHEN attr.attribution_period = '30' AND (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.30d_shop_order_gmv, 0) - COALESCE(s.30d_shop_order_gmv, 0)) * 1.0 / (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS rpv,
    -- 新客率
    CAST(CASE WHEN attr.attribution_period = '15' AND (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.15d_shop_new_customer_uv, 0) - COALESCE(s.15d_shop_new_customer_uv, 0)) * 1.0 / (COALESCE(e.15d_enter_shop_uv, 0) - COALESCE(s.15d_enter_shop_uv, 0))
         WHEN attr.attribution_period = '30' AND (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0)) > 0
         THEN (COALESCE(e.30d_shop_new_customer_uv, 0) - COALESCE(s.30d_shop_new_customer_uv, 0)) * 1.0 / (COALESCE(e.30d_enter_shop_uv, 0) - COALESCE(s.30d_enter_shop_uv, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS new_customer_rate,
    -- 店铺新客UV
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_shop_new_customer_uv, 0) - COALESCE(s.15d_shop_new_customer_uv, 0)
         ELSE COALESCE(e.30d_shop_new_customer_uv, 0) - COALESCE(s.30d_shop_new_customer_uv, 0) END AS BIGINT) AS shop_new_customer_uv,
    -- 全店成交GMV
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_shop_order_gmv, 0) - COALESCE(s.15d_shop_order_gmv, 0)
         ELSE COALESCE(e.30d_shop_order_gmv, 0) - COALESCE(s.30d_shop_order_gmv, 0) END AS DECIMAL(20,6)) AS shop_order_gmv,
    -- 新客成本
    CAST(CASE WHEN attr.attribution_period = '15' AND (COALESCE(e.15d_shop_new_customer_uv, 0) - COALESCE(s.15d_shop_new_customer_uv, 0)) > 0
         THEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) * 1.0 / (COALESCE(e.15d_shop_new_customer_uv, 0) - COALESCE(s.15d_shop_new_customer_uv, 0))
         WHEN attr.attribution_period = '30' AND (COALESCE(e.30d_shop_new_customer_uv, 0) - COALESCE(s.30d_shop_new_customer_uv, 0)) > 0
         THEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) * 1.0 / (COALESCE(e.30d_shop_new_customer_uv, 0) - COALESCE(s.30d_shop_new_customer_uv, 0))
         ELSE 0 END AS DECIMAL(20,6))                                             AS cac,
    -- 全店ROI
    CAST(CASE WHEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) > 0
         THEN CASE WHEN attr.attribution_period = '15' THEN (COALESCE(e.15d_shop_order_gmv, 0) - COALESCE(s.15d_shop_order_gmv, 0)) * 1.0 / (COALESCE(e.fee, 0) - COALESCE(s.fee, 0))
                   ELSE (COALESCE(e.30d_shop_order_gmv, 0) - COALESCE(s.30d_shop_order_gmv, 0)) * 1.0 / (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) END
         ELSE 0 END AS DECIMAL(20,6))                                              AS roi,
    -- 单品ROI
    CAST(CASE WHEN (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) > 0
         THEN CASE WHEN attr.attribution_period = '15' THEN (COALESCE(e.15d_task_product_gmv, 0) - COALESCE(s.15d_task_product_gmv, 0)) * 1.0 / (COALESCE(e.fee, 0) - COALESCE(s.fee, 0))
                   ELSE (COALESCE(e.30d_task_product_gmv, 0) - COALESCE(s.30d_task_product_gmv, 0)) * 1.0 / (COALESCE(e.fee, 0) - COALESCE(s.fee, 0)) END
         ELSE 0 END AS DECIMAL(20,6))                                              AS single_product_roi,

    -- ============ 系统字段 ============
    GETDATE()                                                                      AS etl_time,

    -- ============ 搜索组件指标（表结构末尾） ============
    CAST(COALESCE(e.search_cmt_click, 0) - COALESCE(s.search_cmt_click, 0) AS BIGINT) AS search_cmt_click,
    -- 单品成交GMV
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_task_product_gmv, 0) - COALESCE(s.15d_task_product_gmv, 0)
         ELSE COALESCE(e.30d_task_product_gmv, 0) - COALESCE(s.30d_task_product_gmv, 0) END AS DECIMAL(20,6)) AS task_product_gmv,
    CAST(COALESCE(e.search_cmt_impression, 0) - COALESCE(s.search_cmt_impression, 0) AS BIGINT) AS search_cmt_impression,

    b.ds                                                                           AS ds

FROM brg_xhs_note_project_df b
-- 获取项目有效期配置
INNER JOIN dim_xhs_project_df p
    ON b.project_id = p.project_id
    AND p.ds = b.ds
-- 归因口径展开
CROSS JOIN (
    SELECT '15' AS attribution_period
    UNION ALL
    SELECT '30' AS attribution_period
) attr
-- 结束时间点数据（取KPI获取时间，未到则取当天）
LEFT JOIN dws_xhs_note_cum e
    ON b.note_id = e.note_id
    AND e.dt = LEAST(p.kpi_fetch_time, TO_CHAR(TO_DATE(b.ds, 'yyyymmdd'), 'yyyy-mm-dd'))
    AND e.ds = b.ds
-- 开始时间点数据（项目开始日期前一天）
LEFT JOIN dws_xhs_note_cum s
    ON b.note_id = s.note_id
    AND s.dt = TO_CHAR(DATEADD(TO_DATE(p.valid_from, 'yyyy-mm-dd'), -1, 'dd'), 'yyyy-mm-dd')
    AND s.ds = b.ds
WHERE b.ds = '${bizdate}'
;
