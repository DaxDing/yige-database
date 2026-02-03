-- ============================================================
-- ETL: ODS → DWD 搜索词层日离线明细
-- 源表: ods_xhs_searchword_report_di
-- 目标表: dwd_xhs_searchword_report_di
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_searchword_report_di PARTITION (ds='${bizdate}')
SELECT
    -- 标识字段
    a.advertiser_id,                                                                           -- 投放账号ID
    GET_JSON_OBJECT(a.raw_data, '$.search_word')                         AS search_word,        -- 搜索词
    GET_JSON_OBJECT(a.raw_data, '$.campaign_id')                         AS campaign_id,        -- 计划ID
    GET_JSON_OBJECT(a.raw_data, '$.unit_id')                             AS unit_id,            -- 单元ID
    GET_JSON_OBJECT(a.raw_data, '$.creativity_id')                       AS creativity_id,      -- 创意ID
    GET_JSON_OBJECT(a.raw_data, '$.note_id')                             AS note_id,            -- 笔记ID
    -- 策略字段
    CAST(GET_JSON_OBJECT(a.raw_data, '$.placement') AS INT)              AS placement,          -- 投放位置
    CAST(GET_JSON_OBJECT(a.raw_data, '$.marketing_target') AS INT)       AS marketing_target,   -- 营销目标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.promotion_target') AS INT)       AS promotion_target,   -- 标的类型
    CAST(GET_JSON_OBJECT(a.raw_data, '$.optimize_target') AS INT)        AS optimize_target,    -- 优化目标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.bidding_strategy') AS INT)       AS bidding_strategy,   -- 竞价策略
    -- 时间字段
    a.dt,                                                                                      -- 数据时间
    -- 核心指标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.fee') AS DECIMAL(18,2))          AS fee,                -- 消费
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.impression') AS BIGINT), 0)       AS impression,         -- 展现量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.click') AS BIGINT), 0)            AS click,              -- 点击量
    -- 互动指标
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.like') AS BIGINT), 0)             AS `like`,             -- 点赞
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.comment') AS BIGINT), 0)          AS `comment`,          -- 评论
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.collect') AS BIGINT), 0)          AS collect,            -- 收藏
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.follow') AS BIGINT), 0)           AS follow,             -- 关注
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.share') AS BIGINT), 0)            AS share,              -- 分享
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.interaction') AS BIGINT), 0)      AS interaction,        -- 互动量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.action_button_click') AS BIGINT), 0) AS action_button_click, -- 行动按钮点击量
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.screenshot') AS BIGINT), 0)       AS screenshot,         -- 截图
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.pic_save') AS BIGINT), 0)         AS pic_save,           -- 保存图片
    COALESCE(CAST(GET_JSON_OBJECT(a.raw_data, '$.reserve_pv') AS BIGINT), 0)       AS reserve_pv,         -- 预告组件点击量
    -- 转化指标: 产品种草（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"search_cmt_click":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_cmt_click'), '0'), ',',
            '"search_cmt_after_read":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_cmt_after_read'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS product_seeding_metrics,
    -- 转化指标: 客资收集（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"leads":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.leads'), '0'), ',',
            '"valid_leads":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.valid_leads'), '0'), ',',
            '"landing_page_visit":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.landing_page_visit'), '0'), ',',
            '"leads_button_impression":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.leads_button_impression'), '0'), ',',
            '"message_user":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message_user'), '0'), ',',
            '"message":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message'), '0'), ',',
            '"message_consult":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.message_consult'), '0'), ',',
            '"initiative_message":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.initiative_message'), '0'), ',',
            '"msg_leads_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.msg_leads_num'), '0'), ',',
            '"phone_call_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.phone_call_cnt'), '0'), ',',
            '"phone_call_succ_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.phone_call_succ_cnt'), '0'), ',',
            '"wechat_copy_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechat_copy_cnt'), '0'), ',',
            '"wechat_copy_succ_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.wechat_copy_succ_cnt'), '0'), ',',
            '"identity_certi_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.identity_certi_cnt'), '0'), ',',
            '"commodity_buy_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.commodity_buy_cnt'), '0'), ',',
            '"seller_visit":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.seller_visit'), '0'), ',',
            '"external_leads":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_leads'), '0'),
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
            '"search_invoke_button_click_cnt":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.search_invoke_button_click_cnt'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS app_promotion_metrics,
    -- 转化指标: 种草直达（清理零值，含小红盟）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"external_goods_visit_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_visit_7'), '0'), ',',
            '"external_goods_visit_24h":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_visit_24h'), '0'), ',',
            '"external_goods_order_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_7'), '0'), ',',
            '"external_goods_order_15":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_15'), '0'), ',',
            '"external_goods_order_30":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_goods_order_30'), '0'), ',',
            '"external_rgmv_7":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_7'), '0'), ',',
            '"external_rgmv_15":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_15'), '0'), ',',
            '"external_rgmv_30":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.external_rgmv_30'), '0'), ',',
            '"presale_order_num_7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.presale_order_num_7d'), '0'), ',',
            '"presale_order_gmv_7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.presale_order_gmv_7d'), '0'), ',',
            '"purchase_order_gmv_7d":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.purchase_order_gmv_7d'), '0'), ',',
            '"goods_visit":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.goods_visit'), '0'), ',',
            '"goods_order":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.goods_order'), '0'), ',',
            '"shopping_cart_add":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.shopping_cart_add'), '0'), ',',
            '"success_goods_order":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.success_goods_order'), '0'), ',',
            '"rgmv":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.rgmv'), '0'), ',',
            '"jd_active_user_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.jd_active_user_num'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS direct_seeding_metrics,
    -- 转化指标: 直播引流（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"clk_live_entry_pv":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.clk_live_entry_pv'), '0'), ',',
            '"clk_live_5s_entry_pv":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.clk_live_5s_entry_pv'), '0'), ',',
            '"clk_live_comment":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.clk_live_comment'), '0'), ',',
            '"clk_live_all_follow":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.clk_live_all_follow'), '0'), ',',
            '"clk_live_avg_view_time":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.clk_live_avg_view_time'), '0'), ',',
            '"clk_live_room_order_num":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.clk_live_room_order_num'), '0'), ',',
            '"clk_live_room_rgmv":', COALESCE(GET_JSON_OBJECT(a.raw_data, '$.clk_live_room_rgmv'), '0'),
        '}'),
        '"[^"]+":0(\\.\\d+)?,?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS live_metrics,
    -- 系统字段
    GETDATE() AS etl_time
FROM ods_xhs_searchword_report_di a
WHERE a.ds = '${bizdate}'
;
