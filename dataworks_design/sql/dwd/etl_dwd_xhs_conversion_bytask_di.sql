-- ============================================================
-- ETL: ODS → DWD 任务维度转化日增量
-- 源表: ods_xhs_grass_bytask_conversion_di
-- 目标表: dwd_xhs_conversion_bytask_di
-- 说明: 种草联盟按任务维度站外转化归因数据 (淘宝/京东)
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_conversion_bytask_di PARTITION (ds='${bizdate}')
SELECT
    -- 标识字段
    task_id,                                                                                 -- 任务组ID
    -- 归因字段
    grass_alliance,                                                   -- 种草联盟: tb/jd
    attribution_period,                                               -- 归因口径: 15/30
    -- 时间字段
    dt,                                                                                      -- 日期
    -- 阅读进店指标
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.read_uv') AS BIGINT), 0)            AS read_uv,            -- 阅读UV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.enter_shop_uv') AS BIGINT), 0)      AS enter_shop_uv,      -- 进店UV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_new_visitor_uv') AS BIGINT), 0) AS shop_new_visitor_uv, -- 新访客UV
    -- 店铺行为指标
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_collect_uv') AS BIGINT), 0)    AS shop_collect_uv,    -- 店铺收藏UV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.add_cart_uv') AS BIGINT), 0)            AS add_cart_uv,            -- 加购UV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_follow_uv') AS BIGINT), 0)     AS shop_follow_uv,     -- 店铺关注UV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_member_uv') AS BIGINT), 0)     AS shop_member_uv,     -- 店铺会员UV
    -- 成交指标
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_order_uv') AS BIGINT), 0)      AS shop_order_uv,      -- 成交UV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_order_gmv') AS DECIMAL(18,2)), 0) AS shop_order_gmv,  -- 成交GMV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.task_product_gmv') AS DECIMAL(18,2)), 0) AS task_product_gmv, -- 任务商品成交GMV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.task_product_new_customer_gmv') AS DECIMAL(18,2)), 0) AS task_product_new_customer_gmv, -- 任务商品新客成交GMV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.non_task_product_gmv') AS DECIMAL(18,2)), 0) AS non_task_product_gmv, -- 非任务商品成交GMV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.shop_new_customer_uv') AS BIGINT), 0) AS shop_new_customer_uv, -- 新客UV
    -- 预售指标
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.presale_deposit_gmv') AS DECIMAL(18,2)), 0) AS presale_deposit_gmv, -- 预售付定GMV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.presale_estimated_gmv') AS DECIMAL(18,2)), 0) AS presale_estimated_gmv, -- 预售整单预估GMV
    COALESCE(CAST(GET_JSON_OBJECT(raw_data, '$.presale_deposit_uv') AS BIGINT), 0) AS presale_deposit_uv, -- 预售付定UV
    -- 系统字段
    GETDATE() AS etl_time
FROM ods_xhs_grass_bytask_conversion_di
WHERE ds = '${bizdate}'
    -- 过滤所有指标均为空的行
    AND NOT (
        GET_JSON_OBJECT(raw_data, '$.read_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.enter_shop_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_new_visitor_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_collect_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.add_cart_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_follow_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_member_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_order_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_order_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.task_product_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.task_product_new_customer_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.non_task_product_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.shop_new_customer_uv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.presale_deposit_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.presale_estimated_gmv') IS NULL
        AND GET_JSON_OBJECT(raw_data, '$.presale_deposit_uv') IS NULL
    )
;
