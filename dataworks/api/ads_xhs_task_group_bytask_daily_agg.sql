-- ads_xhs_task_group_bytask_daily_agg 任务组维度日累计分析表-任务维度
-- 接口查询

SELECT
    attribution_period,          -- 归因口径
    dt,                          -- 数据更新日期
    project_id,                  -- 项目ID
    ad_product_name,             -- 归属产品
    task_group_name,             -- 任务组
    read_uv,                     -- 阅读/播放UV
    enter_shop_rate,             -- 进店率
    enter_shop_uv,               -- 进店UV
    conversion_rate,             -- 成交转化率
    shop_order_uv,               -- 成交UV
    average_order_value,         -- 客单价
    shop_order_gmv,              -- 成交GMV
    task_product_gmv,            -- 任务商品成交GMV
    collect_rate,                -- 收加率
    rpv,                         -- UV价值
    kols_fee,                    -- 蒲公英金额
    ad_fee,                      -- 投流金额
    fee,                         -- 总金额
    cpuv,                        -- CPUV【综合】
    roi                          -- ROI
FROM ads_xhs_task_group_bytask_daily_agg
WHERE ds >= '00000000' AND ds <= '99999999'
AND (dt = '${dt}' OR '${dt}' IN ('', 'all'))
AND (attribution_period = '${attribution_period}' OR '${attribution_period}' IN ('', 'all'))
ORDER BY ds, attribution_period, ad_product_name, task_group_name
;
