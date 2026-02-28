-- ============================================================
-- ETL: ODS → DWD 转化明细日增量
-- 源表: ods_xhs_grass_bycontent_conversion_df（每日全量快照）
-- 目标表: dwd_xhs_conversion_bycontent_di
-- 说明: 增量写入，仅写 DWD 中不存在的 dt 分区
-- ============================================================

SET odps.sql.allow.fullscan=true;
SET odps.sql.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE dwd_xhs_conversion_bycontent_di PARTITION (ds)
SELECT
    -- 标识字段
    b.task_id,                                                                               -- 任务组ID
    GET_JSON_OBJECT(b.raw_data, '$.advertiser_id')                    AS advertiser_id,      -- 投放账号ID
    GET_JSON_OBJECT(b.raw_data, '$.creativity_id')                    AS creativity_id,      -- 创意ID
    b.note_id,                                                                               -- 笔记ID
    -- 归因字段
    b.grass_alliance,                                                                        -- 种草联盟: tb/jd
    b.attribution_period,                                                                    -- 归因口径: 15/30
    -- 时间字段
    b.dt,                                                                                    -- 数据时间
    -- 站外行为指标 (已废弃, 保留字段兼容性)
    -1                                                                AS ad_offsite_active_uv,       -- 站外活跃行为UV
    -1                                                                AS ad_offsite_task_cost,       -- 站外任务期消费
    -1                                                                AS ad_offsite_task_read_uv,    -- 站外任务期阅读UV
    -1                                                                AS ad_offsite_active_uv_dedup, -- 站外活跃行为UV(去重)
    -1                                                                AS ad_offsite_task_cost_dedup, -- 站外任务期消费(去重)
    -1                                                                AS ad_offsite_task_read_uv_dedup, -- 站外任务期阅读UV(去重)
    -- 阅读进店指标 (来源: ods_xhs_grass_bycontent_conversion_di.raw_data)
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.read_uv') AS BIGINT), 0)          AS read_uv,            -- 阅读UV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.enter_shop_uv') AS BIGINT), 0)    AS enter_shop_uv,      -- 进店UV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_new_visitor_uv') AS BIGINT), 0) AS shop_new_visitor_uv, -- 新访客UV
    -- 店铺行为指标
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_collect_uv') AS BIGINT), 0)  AS shop_collect_uv,    -- 店铺收藏UV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.add_cart_uv') AS BIGINT), 0)          AS add_cart_uv,            -- 加购UV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_follow_uv') AS BIGINT), 0)   AS shop_follow_uv,     -- 店铺关注UV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_member_uv') AS BIGINT), 0)   AS shop_member_uv,     -- 店铺会员UV
    -- 成交指标
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_order_uv') AS BIGINT), 0)    AS shop_order_uv,      -- 成交UV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_order_gmv') AS DECIMAL(18,2)), 0) AS shop_order_gmv, -- 成交GMV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.task_product_gmv') AS DECIMAL(18,2)), 0) AS task_product_gmv, -- 任务商品成交GMV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.task_product_new_customer_gmv') AS DECIMAL(18,2)), 0) AS task_product_new_customer_gmv, -- 任务商品新客成交GMV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.non_task_product_gmv') AS DECIMAL(18,2)), 0) AS non_task_product_gmv, -- 非任务商品成交GMV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.shop_new_customer_uv') AS BIGINT), 0) AS shop_new_customer_uv, -- 新客UV
    -- 预售指标
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.presale_deposit_gmv') AS DECIMAL(18,2)), 0) AS presale_deposit_gmv, -- 预售付定GMV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.presale_estimated_gmv') AS DECIMAL(18,2)), 0) AS presale_estimated_gmv, -- 预售整单预估GMV
    COALESCE(CAST(GET_JSON_OBJECT(b.raw_data, '$.presale_deposit_uv') AS BIGINT), 0) AS presale_deposit_uv, -- 预售付定UV
    -- 系统字段
    GETDATE() AS etl_time,
    -- 动态分区列
    REPLACE(b.dt, '-', '') AS ds
FROM ods_xhs_grass_bycontent_conversion_df b
WHERE b.ds = '${bizdate}'
    -- 增量: 仅写 DWD 中不存在的分区
    AND REPLACE(b.dt, '-', '') NOT IN (
        SELECT DISTINCT ds FROM dwd_xhs_conversion_bycontent_di
    )
    -- 过滤所有指标均为空的行
    AND NOT (
        GET_JSON_OBJECT(b.raw_data, '$.read_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.enter_shop_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_new_visitor_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_collect_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.add_cart_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_follow_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_member_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_order_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_order_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.task_product_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.task_product_new_customer_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.non_task_product_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.shop_new_customer_uv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.presale_deposit_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.presale_estimated_gmv') IS NULL
        AND GET_JSON_OBJECT(b.raw_data, '$.presale_deposit_uv') IS NULL
    )
;
