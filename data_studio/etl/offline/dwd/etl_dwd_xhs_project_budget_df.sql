-- ============================================================
-- ETL: ODS → DWD 项目预算明细
-- 源表: ods_xhs_project_budget_df
-- 目标表: dwd_xhs_project_budget_df
-- 说明: ODS raw_data 为扁平 JSON，直接提取字段
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_project_budget_df PARTITION (ds='${bizdate}')
SELECT
    project_id,
    GET_JSON_OBJECT(raw_data, '$.ad_product_name')                            AS ad_product_name,       -- 投放产品
    CAST(GET_JSON_OBJECT(raw_data, '$.budget') AS DECIMAL(14,2))              AS budget,                -- 预算
    CAST(GET_JSON_OBJECT(raw_data, '$.plan_video_cnt') AS BIGINT)             AS plan_video_cnt,        -- 视频规划数量
    CAST(GET_JSON_OBJECT(raw_data, '$.plan_image_text_cnt') AS BIGINT)        AS plan_image_text_cnt,   -- 图文规划数量
    CAST(GET_JSON_OBJECT(raw_data, '$.kol_budget') AS DECIMAL(14,2))          AS kol_budget,            -- 达人预算
    CAST(GET_JSON_OBJECT(raw_data, '$.ad_budget') AS DECIMAL(14,2))           AS ad_budget,             -- 投流预算
    dt,                                                                                                  -- 数据时间段
    GETDATE()                                                                 AS etl_time               -- ETL时间
FROM ods_xhs_project_budget_df
WHERE ds = '${bizdate}'
;
