-- ============================================================
-- ETL: ODS → DWD 创意层小时明细
-- 源表: ods_xhs_creative_report_hi
-- 目标表: dwd_xhs_creative_hi
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_creative_hi PARTITION (ds='${bizdate}')
SELECT
    -- 标识字段
    a.advertiser_id,                                                                        -- 投放账号ID
    GET_JSON_OBJECT(a.raw_data, '$.note_id')                          AS note_id,           -- 笔记ID
    GET_JSON_OBJECT(a.raw_data, '$.unit_id')                          AS unit_id,           -- 单元ID
    GET_JSON_OBJECT(a.raw_data, '$.campaign_id')                      AS campaign_id,       -- 计划ID
    GET_JSON_OBJECT(a.raw_data, '$.creativity_id')                    AS creativity_id,     -- 创意ID
    -- 策略字段
    CAST(GET_JSON_OBJECT(a.raw_data, '$.placement') AS INT)           AS placement,         -- 投放位置
    CAST(GET_JSON_OBJECT(a.raw_data, '$.marketing_target') AS INT)    AS marketing_target,  -- 营销目标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.promotion_target') AS INT)    AS promotion_target,  -- 标的类型
    CAST(GET_JSON_OBJECT(a.raw_data, '$.optimize_target') AS INT)     AS optimize_target,   -- 优化目标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.bidding_strategy') AS INT)    AS bidding_strategy,  -- 竞价策略
    -- 时间字段
    a.dt,                                                                                   -- 数据时间
    -- 展现指标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.fee') AS DECIMAL(18,2))       AS fee,               -- 消费
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.impression') AS BIGINT), 0)       AS impression,        -- 展现量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.click') AS BIGINT), 0)            AS click,             -- 点击量
    -- 笔记指标
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.like') AS BIGINT), 0)             AS `like`,            -- 点赞
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.comment') AS BIGINT), 0)          AS `comment`,         -- 评论
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.collect') AS BIGINT), 0)          AS collect,           -- 收藏
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.follow') AS BIGINT), 0)           AS follow,            -- 关注
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.share') AS BIGINT), 0)            AS share,             -- 分享
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.interaction') AS BIGINT), 0)      AS interaction,       -- 互动量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.action_button_click') AS BIGINT), 0) AS action_button_click, -- 行动按钮点击量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.screenshot') AS BIGINT), 0)       AS screenshot,        -- 截图
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.pic_save') AS BIGINT), 0)         AS pic_save,          -- 保存图片
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.reserve_pv') AS BIGINT), 0)       AS reserve_pv,        -- 预告组件点击量
    -- 视频指标
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.video_play_5s_cnt') AS BIGINT), 0) AS video_play_5s_cnt, -- 5秒播放量
    -- 转化指标: 产品种草（清理零值，含种草联盟）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"search_cmt_click":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_cmt_click'), '0'), ',',
            '"search_cmt_after_read":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_cmt_after_read'), '0'), ',',
            '"i_user_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.i_user_num'), '0'), ',',
            '"ti_user_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.ti_user_num'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS product_seeding_metrics,
    -- 转化指标: 客资收集（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"leads":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.leads'), '0'), ',',
            '"landing_page_visit":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.landing_page_visit'), '0'), ',',
            '"leads_button_impression":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.leads_button_impression'), '0'), ',',
            '"message_user":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message_user'), '0'), ',',
            '"message":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message'), '0'), ',',
            '"message_consult":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message_consult'), '0'), ',',
            '"initiative_message":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.initiative_message'), '0'), ',',
            '"msg_leads_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.msg_leads_num'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS lead_collection_metrics,
    -- 转化指标: 应用推广（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"invoke_app_open_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_open_cnt'), '0'), ',',
            '"invoke_app_enter_store_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_enter_store_cnt'), '0'), ',',
            '"invoke_app_engagement_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_engagement_cnt'), '0'), ',',
            '"invoke_app_payment_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_payment_cnt'), '0'), ',',
            '"search_invoke_button_click_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_invoke_button_click_cnt'), '0'), ',',
            '"invoke_app_payment_amount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.invoke_app_payment_amount'), '0'), ',',
            '"app_activate_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_activate_cnt'), '0'), ',',
            '"app_register_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_register_cnt'), '0'), ',',
            '"first_app_pay_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.first_app_pay_cnt'), '0'), ',',
            '"current_app_pay_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.current_app_pay_cnt'), '0'), ',',
            '"app_key_action_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_key_action_cnt'), '0'), ',',
            '"app_pay_cnt_7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_pay_cnt_7d'), '0'), ',',
            '"app_pay_amount":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_pay_amount'), '0'), ',',
            '"app_activate_amount_1d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_activate_amount_1d'), '0'), ',',
            '"app_activate_amount_3d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_activate_amount_3d'), '0'), ',',
            '"app_activate_amount_7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.app_activate_amount_7d'), '0'), ',',
            '"retention_1d_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention_1d_cnt'), '0'), ',',
            '"retention_3d_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention_3d_cnt'), '0'), ',',
            '"retention_7d_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.retention_7d_cnt'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS app_promotion_metrics,
    -- 转化指标: 种草直达（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"external_goods_visit_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_visit_7'), '0'), ',',
            '"external_goods_order_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_7'), '0'), ',',
            '"external_rgmv_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_7'), '0'), ',',
            '"external_goods_order_15":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_15'), '0'), ',',
            '"external_rgmv_15":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_15'), '0'), ',',
            '"external_goods_order_30":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_30'), '0'), ',',
            '"external_rgmv_30":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_30'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS direct_seeding_metrics,
    -- 系统字段
    GETDATE() AS etl_time
FROM ods_xhs_creative_report_hi a
WHERE a.ds = '${bizdate}'
;
