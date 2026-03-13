-- ============================================================
-- ETL: ADS 最新分区后链路清零（script 模式，引擎自动并发）
-- 说明: 后链路 T-1 延迟，昨天分区转化指标置 0，前链路和金额不变
-- 逻辑: 固定清零真实昨天（GETDATE()-1），补数据不影响
-- 调度依赖: 4 张 ADS 表 ETL 完成后执行
-- ============================================================

SET odps.sql.submit.mode = "script";

-- 1. ads_xhs_note_bycontent_daily_agg
INSERT OVERWRITE TABLE ads_xhs_note_bycontent_daily_agg PARTITION (ds)
SELECT
    project_id, attribution_period, dt,
    brand_name, product_category, delivery_product, kol_name, note_id,
    fee, ad_fee, kols_fee, note_count,
    impression, read_uv, interaction,
    cpm, cpe, cpc, ctr, search_cmt_click_ctr,
    CAST(0 AS DECIMAL(20,6)) AS cpuv,
    CAST(0 AS DECIMAL(20,6)) AS enter_shop_rate,
    CAST(0 AS BIGINT)        AS enter_shop_uv,
    CAST(0 AS DECIMAL(20,6)) AS new_visitor_rate,
    CAST(0 AS BIGINT)        AS shop_new_visitor_uv,
    CAST(0 AS DECIMAL(20,6)) AS conversion_rate,
    CAST(0 AS BIGINT)        AS shop_order_uv,
    CAST(0 AS DECIMAL(20,6)) AS average_order_value,
    CAST(0 AS DECIMAL(20,6)) AS rpv,
    CAST(0 AS DECIMAL(20,6)) AS new_customer_rate,
    CAST(0 AS BIGINT)        AS shop_new_customer_uv,
    CAST(0 AS DECIMAL(20,6)) AS shop_order_gmv,
    CAST(0 AS DECIMAL(20,6)) AS cac,
    CAST(0 AS DECIMAL(20,6)) AS roi,
    CAST(0 AS DECIMAL(20,6)) AS single_product_roi,
    GETDATE() AS etl_time,
    search_cmt_click,
    CAST(0 AS DECIMAL(20,6)) AS task_product_gmv,
    search_cmt_impression,
    ds
FROM ads_xhs_note_bycontent_daily_agg
WHERE ds = TO_CHAR(DATEADD(GETDATE(), -1, 'dd'), 'yyyymmdd')
;

-- 2. ads_xhs_project_bycontent_daily_agg
INSERT OVERWRITE TABLE ads_xhs_project_bycontent_daily_agg PARTITION (ds)
SELECT
    project_id, attribution_period, dt,
    fee, ad_fee, kols_fee, note_count,
    impression, read_uv, interaction,
    cpm, cpe, cpc, ctr, search_cmt_click_ctr,
    CAST(0 AS DECIMAL(20,6)) AS cpuv,
    CAST(0 AS DECIMAL(20,6)) AS enter_shop_rate,
    CAST(0 AS BIGINT)        AS enter_shop_uv,
    CAST(0 AS DECIMAL(20,6)) AS new_visitor_rate,
    CAST(0 AS BIGINT)        AS shop_new_visitor_uv,
    CAST(0 AS DECIMAL(20,6)) AS conversion_rate,
    CAST(0 AS BIGINT)        AS shop_order_uv,
    CAST(0 AS DECIMAL(20,6)) AS average_order_value,
    CAST(0 AS DECIMAL(20,6)) AS rpv,
    CAST(0 AS DECIMAL(20,6)) AS new_customer_rate,
    CAST(0 AS BIGINT)        AS shop_new_customer_uv,
    CAST(0 AS DECIMAL(20,6)) AS shop_order_gmv,
    CAST(0 AS DECIMAL(20,6)) AS cac,
    CAST(0 AS DECIMAL(20,6)) AS roi,
    CAST(0 AS DECIMAL(20,6)) AS single_product_roi,
    GETDATE() AS etl_time,
    search_cmt_click,
    CAST(0 AS DECIMAL(20,6)) AS task_product_gmv,
    search_cmt_impression,
    ds
FROM ads_xhs_project_bycontent_daily_agg
WHERE ds = TO_CHAR(DATEADD(GETDATE(), -1, 'dd'), 'yyyymmdd')
;

-- 3. ads_xhs_content_theme_bycontent_daily_agg
INSERT OVERWRITE TABLE ads_xhs_content_theme_bycontent_daily_agg PARTITION (ds)
SELECT
    project_id, attribution_period, dt,
    brand_name, product_category, delivery_product, content_theme,
    fee, ad_fee, kols_fee, note_count,
    impression, read_uv, interaction,
    cpm, cpe, cpc, ctr, search_cmt_click_ctr,
    CAST(0 AS DECIMAL(20,6)) AS cpuv,
    CAST(0 AS DECIMAL(20,6)) AS enter_shop_rate,
    CAST(0 AS BIGINT)        AS enter_shop_uv,
    CAST(0 AS DECIMAL(20,6)) AS new_visitor_rate,
    CAST(0 AS BIGINT)        AS shop_new_visitor_uv,
    CAST(0 AS DECIMAL(20,6)) AS conversion_rate,
    CAST(0 AS BIGINT)        AS shop_order_uv,
    CAST(0 AS DECIMAL(20,6)) AS average_order_value,
    CAST(0 AS DECIMAL(20,6)) AS rpv,
    CAST(0 AS DECIMAL(20,6)) AS new_customer_rate,
    CAST(0 AS BIGINT)        AS shop_new_customer_uv,
    CAST(0 AS DECIMAL(20,6)) AS shop_order_gmv,
    CAST(0 AS DECIMAL(20,6)) AS cac,
    CAST(0 AS DECIMAL(20,6)) AS roi,
    CAST(0 AS DECIMAL(20,6)) AS single_product_roi,
    GETDATE() AS etl_time,
    search_cmt_click,
    CAST(0 AS DECIMAL(20,6)) AS task_product_gmv,
    search_cmt_impression,
    ds
FROM ads_xhs_content_theme_bycontent_daily_agg
WHERE ds = TO_CHAR(DATEADD(GETDATE(), -1, 'dd'), 'yyyymmdd')
;

-- 4. ads_xhs_task_group_bytask_daily_agg
INSERT OVERWRITE TABLE ads_xhs_task_group_bytask_daily_agg PARTITION (ds)
SELECT
    attribution_period, dt,
    ad_product_name, task_group_name,
    CAST(0 AS BIGINT)        AS read_uv,
    CAST(0 AS DECIMAL(20,6)) AS enter_shop_rate,
    CAST(0 AS BIGINT)        AS enter_shop_uv,
    CAST(0 AS DECIMAL(20,6)) AS conversion_rate,
    CAST(0 AS BIGINT)        AS shop_order_uv,
    CAST(0 AS DECIMAL(20,6)) AS average_order_value,
    CAST(0 AS DECIMAL(20,6)) AS shop_order_gmv,
    CAST(0 AS DECIMAL(20,6)) AS task_product_gmv,
    CAST(0 AS DECIMAL(20,6)) AS collect_rate,
    CAST(0 AS DECIMAL(20,6)) AS rpv,
    kols_fee, ad_fee, fee,
    CAST(0 AS DECIMAL(20,6)) AS cpuv,
    CAST(0 AS DECIMAL(20,6)) AS roi,
    GETDATE() AS etl_time,
    project_id,
    ds
FROM ads_xhs_task_group_bytask_daily_agg
WHERE ds = TO_CHAR(DATEADD(GETDATE(), -1, 'dd'), 'yyyymmdd')
;
