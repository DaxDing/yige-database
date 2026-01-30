-- ads_xhs_content_theme_bycontent_daily_agg 内容方向维度内容种草日聚合表
-- 接口查询

SELECT
    project_id,                  -- 项目ID
    attribution_period,          -- 归因口径
    dt,                          -- 数据更新日期
    brand_name,                  -- 归属品牌
    product_category,            -- 归属品类
    delivery_product,            -- 归属产品
    content_theme,               -- 内容方向
    fee,                         -- 总金额
    ad_fee,                      -- 投流金额
    kols_fee,                    -- 蒲公英金额
    note_count,                  -- 笔记数量
    impression,                  -- 曝光量
    read_uv,                     -- 阅读量
    interaction,                 -- 互动量
    search_cmt_click,            -- 搜索组件点击数
    search_cmt_impression,       -- 搜索组件曝光数
    cpm,                         -- CPM
    cpe,                         -- CPE
    cpc,                         -- CPC
    ctr,                         -- CTR
    search_cmt_click_ctr,        -- 搜索组件CTR
    cpuv,                        -- CPUV
    enter_shop_rate,             -- 进店率
    enter_shop_uv,               -- 星河-进店UV
    new_visitor_rate,            -- 新访客率
    shop_new_visitor_uv,         -- 星河-店铺新访客
    conversion_rate,             -- 成交转化率
    shop_order_uv,               -- 星河-全店成交UV
    average_order_value,         -- 客单价
    rpv,                         -- UV价值
    new_customer_rate,           -- 新客率
    shop_new_customer_uv,        -- 星河-店铺新客UV
    shop_order_gmv,              -- 星河-全店成交GMV
    task_product_gmv,            -- 星河-单品成交GMV
    cac,                         -- 新客成本
    roi,                         -- 全店ROI
    single_product_roi           -- 单品ROI
FROM ads_xhs_content_theme_bycontent_daily_agg
WHERE ds >= '00000000' AND ds <= '99999999'
AND (dt = '${dt}' OR '${dt}' IN ('', 'all'))
AND (project_id = '${project_id}' OR '${project_id}' IN ('', 'all'))
;
