-- ============================================================
-- ETL: ODS → DWD 定向层实时明细（按小时展开）
-- 源表: ods_xhs_target_realtime_hi
-- 目标表: dwd_xhs_target_realtime_hi
-- 说明: 通过 FROM_JSON + EXPLODE 将 hourly_data 数组展开为每小时一行
--       字段分组对齐 keyword/creative/campaign
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_target_realtime_hi PARTITION (ds='${bizdate}')
SELECT
    -- 标识字段
    a.target_id,                                                                                              -- 定向ID
    CAST(GET_JSON_OBJECT(a.raw_data, '$.base_campaign_dto.campaign_id') AS STRING)        AS campaign_id,     -- 计划ID
    CAST(GET_JSON_OBJECT(a.raw_data, '$.base_unit_dto.unit_id') AS STRING)                AS unit_id,         -- 单元ID
    GET_JSON_OBJECT(a.raw_data, '$.base_target_dto.target_name')                          AS target_name,     -- 定向名称
    -- 策略字段
    CAST(GET_JSON_OBJECT(a.raw_data, '$.base_campaign_dto.placement') AS INT)             AS placement,       -- 投放位置
    CAST(GET_JSON_OBJECT(a.raw_data, '$.base_campaign_dto.marketing_target') AS INT)      AS marketing_target,-- 营销目标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.base_campaign_dto.promotion_target') AS INT)      AS promotion_target,-- 标的类型
    CAST(GET_JSON_OBJECT(a.raw_data, '$.base_campaign_dto.optimize_target') AS INT)       AS optimize_target, -- 优化目标
    CAST(GET_JSON_OBJECT(a.raw_data, '$.base_campaign_dto.bidding_strategy') AS INT)      AS bidding_strategy,-- 竞价策略
    -- 时间字段（从 hourly_data 元素提取）
    t.item['time']                                                                        AS dt,              -- 数据时间段
    -- 展现指标
    CAST(t.item['fee'] AS DECIMAL(18,2))                                                  AS fee,             -- 消费
    COALESCE(CAST(t.item['impression'] AS BIGINT), 0)                                     AS impression,      -- 展现量
    COALESCE(CAST(t.item['click'] AS BIGINT), 0)                                          AS click,           -- 点击量
    -- 笔记指标
    COALESCE(CAST(t.item['like'] AS BIGINT), 0)                                           AS `like`,          -- 点赞
    COALESCE(CAST(t.item['comment'] AS BIGINT), 0)                                        AS `comment`,       -- 评论
    COALESCE(CAST(t.item['collect'] AS BIGINT), 0)                                        AS collect,         -- 收藏
    COALESCE(CAST(t.item['follow'] AS BIGINT), 0)                                         AS follow,          -- 关注
    COALESCE(CAST(t.item['share'] AS BIGINT), 0)                                          AS share,           -- 分享
    COALESCE(CAST(t.item['interaction'] AS BIGINT), 0)                                    AS interaction,     -- 互动量
    COALESCE(CAST(t.item['action_button_click'] AS BIGINT), 0)                            AS action_button_click, -- 行动按钮点击量
    COALESCE(CAST(t.item['screenshot'] AS BIGINT), 0)                                     AS screenshot,      -- 截图
    COALESCE(CAST(t.item['pic_save'] AS BIGINT), 0)                                       AS pic_save,        -- 保存图片
    COALESCE(CAST(t.item['reserve_p_v'] AS BIGINT), 0)                                    AS reserve_pv,      -- 预告组件点击量
    -- 转化指标: 产品种草（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"search_cmt_click":', COALESCE(t.item['search_cmt_click'], '0'), ',',
            '"search_cmt_after_read":', COALESCE(t.item['search_cmt_after_read'], '0'), ',',
            '"seeding_cnt":', COALESCE(t.item['seeding_cnt'], '0'),
        '}'),
        '"[^"]+":(-|0(\\.0+)?)(?=[,\\}]),?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS product_seeding_metrics,
    -- 转化指标: 客资收集（含页面/私信互动，清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"leads":', COALESCE(t.item['leads'], '0'), ',',
            '"valid_leads":', COALESCE(t.item['valid_leads'], '0'), ',',
            '"landing_page_visit":', COALESCE(t.item['landing_page_visit'], '0'), ',',
            '"leads_button_impression":', COALESCE(t.item['leads_button_impression'], '0'), ',',
            '"message_user":', COALESCE(t.item['message_user'], '0'), ',',
            '"message":', COALESCE(t.item['message'], '0'), ',',
            '"message_consult":', COALESCE(t.item['message_consult'], '0'), ',',
            '"initiative_message":', COALESCE(t.item['initiative_message'], '0'), ',',
            '"msg_leads_num":', COALESCE(t.item['msg_leads_num'], '0'), ',',
            '"phone_call_cnt":', COALESCE(t.item['phone_call_cnt'], '0'), ',',
            '"phone_call_succ_cnt":', COALESCE(t.item['phone_call_succ_cnt'], '0'), ',',
            '"seller_visit":', COALESCE(t.item['seller_visit'], '0'), ',',
            '"identity_certi_cnt":', COALESCE(t.item['identity_certi_cnt'], '0'), ',',
            '"wechat_copy_cnt":', COALESCE(t.item['wechat_copy_cnt'], '0'), ',',
            '"wechat_copy_succ_cnt":', COALESCE(t.item['wechat_copy_succ_cnt'], '0'), ',',
            '"page_cmt_imp":', COALESCE(t.item['page_cmt_imp'], '0'), ',',
            '"page_cmt_click":', COALESCE(t.item['page_cmt_click'], '0'), ',',
            '"page_second_jump_imp":', COALESCE(t.item['page_second_jump_imp'], '0'), ',',
            '"page_second_jump_click":', COALESCE(t.item['page_second_jump_click'], '0'), ',',
            '"message_cmt_imp":', COALESCE(t.item['message_cmt_imp'], '0'), ',',
            '"message_cmt_click":', COALESCE(t.item['message_cmt_click'], '0'), ',',
            '"message_second_jump_imp":', COALESCE(t.item['message_second_jump_imp'], '0'), ',',
            '"message_second_jump_click":', COALESCE(t.item['message_second_jump_click'], '0'), ',',
            '"user_page_view_pv":', COALESCE(t.item['user_page_view_pv'], '0'), ',',
            '"user_page_view_uv":', COALESCE(t.item['user_page_view_uv'], '0'), ',',
            '"user_page_message_cnt":', COALESCE(t.item['user_page_message_cnt'], '0'), ',',
            '"user_page_message_user_cnt":', COALESCE(t.item['user_page_message_user_cnt'], '0'),
        '}'),
        '"[^"]+":(-|0(\\.0+)?)(?=[,\\}]),?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS lead_collection_metrics,
    -- 转化指标: 应用推广（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"app_activate_cnt":', COALESCE(t.item['app_activate_cnt'], '0'), ',',
            '"app_activate_amount_1d":', COALESCE(t.item['app_activate_amount_1d'], '0'), ',',
            '"app_activate_amount_3d":', COALESCE(t.item['app_activate_amount_3d'], '0'), ',',
            '"app_activate_amount_7d":', COALESCE(t.item['app_activate_amount_7d'], '0'), ',',
            '"app_download_button_click_cnt":', COALESCE(t.item['app_download_button_click_cnt'], '0'), ',',
            '"app_key_action_cnt":', COALESCE(t.item['app_key_action_cnt'], '0'), ',',
            '"app_pay_amount":', COALESCE(t.item['app_pay_amount'], '0'), ',',
            '"app_pay_cnt_7d":', COALESCE(t.item['app_pay_cnt_7d'], '0'), ',',
            '"app_register_cnt":', COALESCE(t.item['app_register_cnt'], '0'), ',',
            '"first_app_pay_cnt":', COALESCE(t.item['first_app_pay_cnt'], '0'), ',',
            '"current_app_pay_cnt":', COALESCE(t.item['current_app_pay_cnt'], '0'), ',',
            '"retention_1d_cnt":', COALESCE(t.item['retention_1d_cnt'], '0'), ',',
            '"retention_3d_cnt":', COALESCE(t.item['retention_3d_cnt'], '0'), ',',
            '"retention_7d_cnt":', COALESCE(t.item['retention_7d_cnt'], '0'), ',',
            '"search_invoke_button_click_cnt":', COALESCE(t.item['search_invoke_button_click_cnt'], '0'), ',',
            '"invoke_app_open_cnt":', COALESCE(t.item['invoke_app_open_cnt'], '0'), ',',
            '"invoke_app_enter_store_cnt":', COALESCE(t.item['invoke_app_enter_store_cnt'], '0'), ',',
            '"invoke_app_payment_cnt":', COALESCE(t.item['invoke_app_payment_cnt'], '0'), ',',
            '"invoke_app_payment_amount":', COALESCE(t.item['invoke_app_payment_amount'], '0'), ',',
            '"invoke_app_engagement_cnt":', COALESCE(t.item['invoke_app_engagement_cnt'], '0'),
        '}'),
        '"[^"]+":(-|0(\\.0+)?)(?=[,\\}]),?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS app_promotion_metrics,
    -- 转化指标: 电商（清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"commodity_buy_cnt":', COALESCE(t.item['commodity_buy_cnt'], '0'), ',',
            '"shopping_cart_add":', COALESCE(t.item['shopping_cart_add'], '0'), ',',
            '"goods_order":', COALESCE(t.item['goods_order'], '0'), ',',
            '"goods_visit":', COALESCE(t.item['goods_visit'], '0'), ',',
            '"success_goods_order":', COALESCE(t.item['success_goods_order'], '0'), ',',
            '"buy_now":', COALESCE(t.item['buy_now'], '0'),
        '}'),
        '"[^"]+":(-|0(\\.0+)?)(?=[,\\}]),?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS ecommerce_metrics,
    -- 转化指标: 种草直达（外部电商，清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"external_goods_visit_24h":', COALESCE(t.item['external_goods_visit_24h'], '0'), ',',
            '"external_goods_visit_7":', COALESCE(t.item['external_goods_visit_7'], '0'), ',',
            '"external_goods_order_24h":', COALESCE(t.item['external_goods_order_24h'], '0'), ',',
            '"external_goods_order_7":', COALESCE(t.item['external_goods_order_7'], '0'), ',',
            '"external_goods_order_15":', COALESCE(t.item['external_goods_order_15'], '0'), ',',
            '"external_goods_order_30":', COALESCE(t.item['external_goods_order_30'], '0'), ',',
            '"external_rgmv_24h":', COALESCE(t.item['external_rgmv_24h'], '0'), ',',
            '"external_rgmv_7":', COALESCE(t.item['external_rgmv_7'], '0'), ',',
            '"external_rgmv_15":', COALESCE(t.item['external_rgmv_15'], '0'), ',',
            '"external_rgmv_30":', COALESCE(t.item['external_rgmv_30'], '0'), ',',
            '"external_goods_order_price_24h":', COALESCE(t.item['external_goods_order_price_24h'], '0'), ',',
            '"external_goods_order_price_7":', COALESCE(t.item['external_goods_order_price_7'], '0'), ',',
            '"external_goods_order_price_15":', COALESCE(t.item['external_goods_order_price_15'], '0'), ',',
            '"external_goods_order_price_30":', COALESCE(t.item['external_goods_order_price_30'], '0'), ',',
            '"external_goods_visit_price_24h":', COALESCE(t.item['external_goods_visit_price_24h'], '0'), ',',
            '"external_goods_visit_price_7":', COALESCE(t.item['external_goods_visit_price_7'], '0'), ',',
            '"external_roi_24h":', COALESCE(t.item['external_roi_24h'], '0'), ',',
            '"external_roi_7":', COALESCE(t.item['external_roi_7'], '0'), ',',
            '"external_roi_15":', COALESCE(t.item['external_roi_15'], '0'), ',',
            '"external_roi_30":', COALESCE(t.item['external_roi_30'], '0'), ',',
            '"presale_order_num_7d":', COALESCE(t.item['presale_order_num_7d'], '0'), ',',
            '"presale_order_gmv_7d":', COALESCE(t.item['presale_order_gmv_7d'], '0'), ',',
            '"purchase_order_gmv_7d":', COALESCE(t.item['purchase_order_gmv_7d'], '0'), ',',
            '"purchase_order_price_7d":', COALESCE(t.item['purchase_order_price_7d'], '0'), ',',
            '"purchase_order_roi_7d":', COALESCE(t.item['purchase_order_roi_7d'], '0'), ',',
            '"external_leads":', COALESCE(t.item['external_leads'], '0'),
        '}'),
        '"[^"]+":(-|0(\\.0+)?)(?=[,\\}]),?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS direct_seeding_metrics,
    -- 搜索排名指标（含 _all 维度和 word_price，清理零值）
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
        CONCAT('{',
            '"word_avg_location":', COALESCE(t.item['word_avg_location'], '0'), ',',
            '"word_click_rank_first":', COALESCE(t.item['word_click_rank_first'], '0'), ',',
            '"word_click_rank_third":', COALESCE(t.item['word_click_rank_third'], '0'), ',',
            '"word_click_rank_all":', COALESCE(t.item['word_click_rank_all'], '0'), ',',
            '"word_click_rate_first":', COALESCE(t.item['word_click_rate_first'], '0'), ',',
            '"word_click_rate_third":', COALESCE(t.item['word_click_rate_third'], '0'), ',',
            '"word_click_rate_all":', COALESCE(t.item['word_click_rate_all'], '0'), ',',
            '"word_impression_rank_first":', COALESCE(t.item['word_impression_rank_first'], '0'), ',',
            '"word_impression_rank_third":', COALESCE(t.item['word_impression_rank_third'], '0'), ',',
            '"word_impression_rank_all":', COALESCE(t.item['word_impression_rank_all'], '0'), ',',
            '"word_impression_rate_first":', COALESCE(t.item['word_impression_rate_first'], '0'), ',',
            '"word_impression_rate_third":', COALESCE(t.item['word_impression_rate_third'], '0'), ',',
            '"word_impression_rate_all":', COALESCE(t.item['word_impression_rate_all'], '0'), ',',
            '"word_price_first":', COALESCE(t.item['word_price_first'], '0'), ',',
            '"word_price_third":', COALESCE(t.item['word_price_third'], '0'),
        '}'),
        '"[^"]+":(-|0(\\.0+)?)(?=[,\\}]),?', ''),
        ',}', '}'),
        '\\{,', '{')
    AS search_ranking_metrics,
    -- 系统字段
    GETDATE() AS etl_time
FROM ods_xhs_target_realtime_hi a
LATERAL VIEW EXPLODE(FROM_JSON(GET_JSON_OBJECT(a.raw_data, '$.hourly_data'), 'ARRAY<MAP<STRING,STRING>>')) t AS item
WHERE a.ds = '${bizdate}'
  AND t.item IS NOT NULL
;
