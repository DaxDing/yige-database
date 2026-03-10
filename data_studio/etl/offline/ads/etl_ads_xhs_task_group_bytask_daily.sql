-- ============================================================
-- ETL: DWS → ADS 任务组维度日累计分析-任务维度
-- 源表: dws_xhs_task_group_cum, dim_xhs_task_group_df
-- 目标表: ads_xhs_task_group_bytask_daily_agg
-- 说明: DWS 已按任务组聚合，CROSS JOIN 归因口径展开，计算派生指标
-- ============================================================

INSERT OVERWRITE TABLE ads_xhs_task_group_bytask_daily_agg PARTITION (ds)
SELECT /*+ MAPJOIN(attr) */
    -- ============ 维度字段 ============
    CAST(attr.attribution_period AS BIGINT)                                       AS attribution_period,
    CAST(e.ds AS BIGINT)                                                          AS dt,
    e.ad_product_name,
    e.task_group_name,

    -- ============ 阅读UV ============
    -- bytask 转化的 read_uv（按归因口径）
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_read_uv, 0)
         ELSE COALESCE(e.30d_read_uv, 0) END AS BIGINT)                          AS read_uv,

    -- ============ 进店率 ============
    CAST(CASE WHEN attr.attribution_period = '15' AND COALESCE(e.15d_read_uv, 0) > 0
         THEN COALESCE(e.15d_enter_shop_uv, 0) * 1.0 / e.15d_read_uv
         WHEN attr.attribution_period = '30' AND COALESCE(e.30d_read_uv, 0) > 0
         THEN COALESCE(e.30d_enter_shop_uv, 0) * 1.0 / e.30d_read_uv
         ELSE 0 END AS DECIMAL(20,6))                                             AS enter_shop_rate,

    -- ============ 进店UV ============
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_enter_shop_uv, 0)
         ELSE COALESCE(e.30d_enter_shop_uv, 0) END AS BIGINT)                    AS enter_shop_uv,

    -- ============ 成交转化率 ============
    CAST(CASE WHEN attr.attribution_period = '15' AND COALESCE(e.15d_enter_shop_uv, 0) > 0
         THEN COALESCE(e.15d_shop_order_uv, 0) * 1.0 / e.15d_enter_shop_uv
         WHEN attr.attribution_period = '30' AND COALESCE(e.30d_enter_shop_uv, 0) > 0
         THEN COALESCE(e.30d_shop_order_uv, 0) * 1.0 / e.30d_enter_shop_uv
         ELSE 0 END AS DECIMAL(20,6))                                             AS conversion_rate,

    -- ============ 成交UV ============
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_shop_order_uv, 0)
         ELSE COALESCE(e.30d_shop_order_uv, 0) END AS BIGINT)                    AS shop_order_uv,

    -- ============ 客单价 ============
    CAST(CASE WHEN attr.attribution_period = '15' AND COALESCE(e.15d_shop_order_uv, 0) > 0
         THEN COALESCE(e.15d_shop_order_gmv, 0) * 1.0 / e.15d_shop_order_uv
         WHEN attr.attribution_period = '30' AND COALESCE(e.30d_shop_order_uv, 0) > 0
         THEN COALESCE(e.30d_shop_order_gmv, 0) * 1.0 / e.30d_shop_order_uv
         ELSE 0 END AS DECIMAL(20,6))                                             AS average_order_value,

    -- ============ 成交GMV ============
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_shop_order_gmv, 0)
         ELSE COALESCE(e.30d_shop_order_gmv, 0) END AS DECIMAL(20,6))            AS shop_order_gmv,

    -- ============ 任务商品成交GMV ============
    CAST(CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_task_product_gmv, 0)
         ELSE COALESCE(e.30d_task_product_gmv, 0) END AS DECIMAL(20,6))          AS task_product_gmv,

    -- ============ 收加率（收藏+加购UV / 进店UV） ============
    CAST(CASE WHEN attr.attribution_period = '15' AND COALESCE(e.15d_enter_shop_uv, 0) > 0
         THEN (COALESCE(e.15d_shop_collect_uv, 0) + COALESCE(e.15d_add_cart_uv, 0)) * 1.0 / e.15d_enter_shop_uv
         WHEN attr.attribution_period = '30' AND COALESCE(e.30d_enter_shop_uv, 0) > 0
         THEN (COALESCE(e.30d_shop_collect_uv, 0) + COALESCE(e.30d_add_cart_uv, 0)) * 1.0 / e.30d_enter_shop_uv
         ELSE 0 END AS DECIMAL(20,6))                                             AS collect_rate,

    -- ============ UV价值（RPV） ============
    CAST(CASE WHEN attr.attribution_period = '15' AND COALESCE(e.15d_enter_shop_uv, 0) > 0
         THEN COALESCE(e.15d_shop_order_gmv, 0) * 1.0 / e.15d_enter_shop_uv
         WHEN attr.attribution_period = '30' AND COALESCE(e.30d_enter_shop_uv, 0) > 0
         THEN COALESCE(e.30d_shop_order_gmv, 0) * 1.0 / e.30d_enter_shop_uv
         ELSE 0 END AS DECIMAL(20,6))                                             AS rpv,

    -- ============ 金额指标 ============
    CAST(COALESCE(e.pgy_actual_amt, 0) AS DECIMAL(20,6))                          AS kols_fee,
    CAST(COALESCE(e.ad_fee, 0) AS DECIMAL(20,6))                                  AS ad_fee,
    CAST(COALESCE(e.fee, 0) AS DECIMAL(20,6))                                     AS fee,

    -- ============ CPUV（综合：费用/进店UV） ============
    CAST(CASE WHEN attr.attribution_period = '15' AND COALESCE(e.15d_enter_shop_uv, 0) > 0
         THEN COALESCE(e.fee, 0) * 1.0 / e.15d_enter_shop_uv
         WHEN attr.attribution_period = '30' AND COALESCE(e.30d_enter_shop_uv, 0) > 0
         THEN COALESCE(e.fee, 0) * 1.0 / e.30d_enter_shop_uv
         ELSE 0 END AS DECIMAL(20,6))                                             AS cpuv,

    -- ============ ROI ============
    CAST(CASE WHEN COALESCE(e.fee, 0) > 0
         THEN CASE WHEN attr.attribution_period = '15' THEN COALESCE(e.15d_shop_order_gmv, 0) * 1.0 / e.fee
                   ELSE COALESCE(e.30d_shop_order_gmv, 0) * 1.0 / e.fee END
         ELSE 0 END AS DECIMAL(20,6))                                             AS roi,

    -- ============ 系统字段 ============
    GETDATE()                                                                      AS etl_time,
    d.project_id,

    e.ds                                                                           AS ds

FROM dws_xhs_task_group_cum e
LEFT JOIN (
    SELECT DISTINCT task_group_id, project_id
    FROM dim_xhs_task_group_df
    WHERE ds = '${bizdate}'
) d ON e.task_group_id = d.task_group_id
CROSS JOIN (
    SELECT '15' AS attribution_period
    UNION ALL
    SELECT '30' AS attribution_period
) attr
WHERE e.ds IN ('${bizdate}', TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -1, 'dd'), 'yyyymmdd'))
;
