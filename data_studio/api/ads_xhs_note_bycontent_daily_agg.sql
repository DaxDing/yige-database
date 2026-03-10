-- ads_xhs_note_bycontent_daily_agg 笔记维度内容种草日聚合表
-- 接口查询

SELECT
    project_id,                  -- 项目ID
    attribution_period,          -- 归因口径
    dt,                          -- 数据更新日期
    brand_name,                  -- 归属品牌
    product_category,            -- 归属品类
    delivery_product,            -- 归属产品
    kol_name,                    -- 博主昵称
    note_id,                     -- 笔记id
    fee,                         -- 总金额
    ad_fee,                      -- 投流金额
    kols_fee,                    -- 蒲公英金额
    note_count,                  -- 笔记数量
    impression,                  -- 曝光量
    read_uv,                     -- 阅读量
    interaction,                 -- 互动量
    search_cmt_click,            -- 搜索组件点击数
    search_cmt_impression,       -- 搜索组件曝光数
    cpm,                         -- CPM = fee / impression * 1000
    cpe,                         -- CPE = fee / interaction
    cpc,                         -- CPC = fee / read_uv
    ctr,                         -- CTR = read_uv / impression
    search_cmt_click_ctr,        -- 搜索组件CTR = search_cmt_click / search_cmt_impression
    cpuv,                        -- CPUV = fee / enter_shop_uv
    enter_shop_rate,             -- 进店率 = enter_shop_uv / read_uv
    enter_shop_uv,               -- 星河-进店UV
    new_visitor_rate,            -- 新访客率 = shop_new_visitor_uv / enter_shop_uv
    shop_new_visitor_uv,         -- 星河-店铺新访客
    conversion_rate,             -- 成交转化率 = shop_order_uv / enter_shop_uv
    shop_order_uv,               -- 星河-全店成交UV
    average_order_value,         -- 客单价 = shop_order_gmv / shop_order_uv
    rpv,                         -- UV价值 = shop_order_gmv / enter_shop_uv
    new_customer_rate,           -- 新客率 = shop_new_customer_uv / enter_shop_uv
    shop_new_customer_uv,        -- 星河-店铺新客UV
    shop_order_gmv,              -- 星河-全店成交GMV
    task_product_gmv,            -- 星河-单品成交GMV
    cac,                         -- 新客成本 = fee / shop_new_customer_uv
    roi,                         -- 全店ROI = shop_order_gmv / fee
    single_product_roi           -- 单品ROI = task_product_gmv / fee
FROM ads_xhs_note_bycontent_daily_agg
WHERE ds >= '00000000' AND ds <= '99999999'
AND (dt = '${dt}' OR '${dt}' IN ('', 'all') OR ('${dt}' = 'last7d' AND dt >= TO_CHAR(DATEADD(GETDATE(), -7, 'dd'), 'yyyymmdd') AND dt <= TO_CHAR(DATEADD(GETDATE(), -1, 'dd'), 'yyyymmdd')))
AND (project_id = '${project_id}' OR '${project_id}' IN ('', 'all'))
ORDER BY ds, project_id, attribution_period, note_id
;
