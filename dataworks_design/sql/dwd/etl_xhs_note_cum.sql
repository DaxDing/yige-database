-- ============================================================
-- ETL: ODS → DWD 笔记层日累计
-- 源表: ods_xhs_post_note_report_di, ods_xhs_bus_data_df
-- 目标表: dwd_xhs_note_cum
-- 说明: ODS 为累计数据，直接清洗输出，关联业务数据获取蒲公英实际金额
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_note_cum PARTITION (ds='${bizdate}')
SELECT
    -- 维度字段
    GET_JSON_OBJECT(o.raw_data, '$.note_id')                              AS note_id,                 -- 笔记ID
    GET_JSON_OBJECT(o.raw_data, '$.kol_id')                               AS kol_id,                  -- 达人ID
    GET_JSON_OBJECT(o.raw_data, '$.kol_nick_name')                        AS kol_name,                -- 博主名称
    o.brand_user_id,                                                                                   -- 品牌商ID
    GET_JSON_OBJECT(o.raw_data, '$.order_id')                             AS order_id,                -- 订单ID
    GET_JSON_OBJECT(o.raw_data, '$.spu_name')                             AS spu_name,                -- SPU名称
    GET_JSON_OBJECT(o.raw_data, '$.comp_type')                            AS comment_comp_type,       -- 评论组件类型
    GET_JSON_OBJECT(o.raw_data, '$.content_comp_type')                    AS content_comp_type,       -- 内容组件类型
    GET_JSON_OBJECT(o.raw_data, '$.third_project_data.third_project_id')  AS pgy_project_id,          -- 蒲公英项目ID
    -- 时间字段
    GET_JSON_OBJECT(o.raw_data, '$.date_key')                             AS dt,                      -- 数据时间
    -- 金额指标（单位：元）
    CAST(CAST(GET_JSON_OBJECT(o.raw_data, '$.kol_price') AS BIGINT) / 100 AS BIGINT)            AS kol_price,               -- 博主费用(元)
    CAST(CAST(GET_JSON_OBJECT(o.raw_data, '$.total_platform_price') AS BIGINT) / 100 AS BIGINT) AS total_platform_price,    -- 平台总价(元)
    b.pgy_actual_amt,                                                                                  -- 蒲公英实际金额(元)
    -- 展现指标
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.imp_num') AS BIGINT), 0)              AS impression,              -- 展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.read_uv') AS BIGINT), 0)              AS read_uv,                 -- 阅读UV
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.origin_imp_num') AS BIGINT), 0)       AS origin_impression,       -- 自然展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.origin_read_num') AS BIGINT), 0)      AS origin_read,             -- 自然阅读量
    -- 笔记互动指标
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.cmt_num') AS BIGINT), 0)              AS comment,                 -- 评论
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.fav_num') AS BIGINT), 0)              AS collect,                 -- 收藏
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.share_num') AS BIGINT), 0)            AS share,                   -- 分享
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.like_num') AS BIGINT), 0)             AS `like`,                  -- 点赞
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.read_follow') AS BIGINT), 0)          AS follow,                  -- 关注
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.engage_num') AS BIGINT), 0)           AS interaction,             -- 互动量
    -- 阅读分布指标
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.read_search') AS BIGINT), 0)          AS search_read,             -- 搜索阅读量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.imp_search') AS BIGINT), 0)           AS search_impression,       -- 搜索页展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.promotion_read_num') AS BIGINT), 0)   AS promotion_read,          -- 推广阅读量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.promotion_imp_num') AS BIGINT), 0)    AS promotion_impression,    -- 推广展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.heat_read_num') AS BIGINT), 0)        AS heat_read,               -- 加热阅读量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.heat_imp_num') AS BIGINT), 0)         AS heat_impression,         -- 加热展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.imp_discovery') AS BIGINT), 0)        AS discovery_impression,    -- 发现页展现量
    -- 组件指标
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.comp_imp_num') AS BIGINT), 0)         AS comment_comp_impression, -- 评论组件展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.comp_click_pv_num') AS BIGINT), 0)    AS comment_comp_click,      -- 评论组件点击量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.comp_click_uv_num') AS BIGINT), 0)    AS comment_comp_click_uv,   -- 评论组件点击UV
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.content_comp_imp_num') AS BIGINT), 0) AS content_comp_impression, -- 内容组件展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.content_comp_click_num') AS BIGINT), 0) AS content_comp_click,    -- 内容组件点击量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.content_comp_click_uv') AS BIGINT), 0) AS content_comp_click_uv,  -- 内容组件点击UV
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.engage_comp_imp_num') AS BIGINT), 0)  AS engage_comp_impression,  -- 互动组件展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.engage_comp_click_uv_num') AS BIGINT), 0) AS engage_comp_click,   -- 互动组件点击量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.note_bottom_comp_imp_num') AS BIGINT), 0) AS note_bottom_comp_impression, -- 笔记底部组件展现量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.note_bottom_comp_click_pv_num') AS BIGINT), 0) AS note_bottom_comp_click, -- 笔记底部组件点击量
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.note_bottom_comp_click_uv_num') AS BIGINT), 0) AS note_bottom_comp_click_uv, -- 笔记底部组件点击UV
    -- 兴趣指标
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.interest_num') AS BIGINT), 0)         AS interest,                -- 种草数
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.feed_interest_num') AS BIGINT), 0)    AS feed_interest,           -- 推荐场种草数
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.search_interest_num') AS BIGINT), 0)  AS search_interest,         -- 搜索场种草数
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.other_interest_num') AS BIGINT), 0)   AS other_interest,          -- 其他场种草数
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.cp') AS BIGINT), 0)                   AS cp,                      -- 消费意向
    -- 比率指标（小数形式，如0.2439表示24.39%）
    COALESCE(CAST(ROUND(CAST(GET_JSON_OBJECT(o.raw_data, '$.video_play5_s_rate') AS DECIMAL(10,6)) / 100, 4) AS DECIMAL(10,4)), 0) AS video_play_5s_rate, -- 5s完播率
    COALESCE(CAST(ROUND(CAST(GET_JSON_OBJECT(o.raw_data, '$.pic_read3_s_rate') AS DECIMAL(10,6)) / 100, 4) AS DECIMAL(10,4)), 0)   AS pic_read_3s_rate,   -- 3s阅读率
    COALESCE(CAST(GET_JSON_OBJECT(o.raw_data, '$.avg_view_time') AS BIGINT), 0)                                                    AS avg_view_time,      -- 平均浏览时长(秒)
    COALESCE(CAST(ROUND(CAST(GET_JSON_OBJECT(o.raw_data, '$.finish_rate') AS DECIMAL(10,6)) / 100, 4) AS DECIMAL(10,4)), 0)        AS finish_rate,        -- 视频完播率
    -- 系统字段
    GETDATE() AS etl_time
FROM ods_xhs_post_note_report_di o
LEFT JOIN ods_xhs_bus_data_df b
    ON GET_JSON_OBJECT(o.raw_data, '$.note_id') = b.note_id
    AND b.ds = '${bizdate}'
WHERE o.ds = '${bizdate}'
;
