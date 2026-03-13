-- ============================================================
-- ETL: ODS → DWD 项目执行规划明细
-- 源表: ods_xhs_project_execution_plan_df
-- 目标表: dwd_xhs_project_execution_plan_df
-- 说明: ODS raw_data 为扁平 JSON，直接提取字段
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_project_execution_plan_df PARTITION (ds='${bizdate}')
SELECT
    project_id,
    GET_JSON_OBJECT(raw_data, '$.ad_product_name')                            AS ad_product_name,         -- 投放产品
    GET_JSON_OBJECT(raw_data, '$.kfs_type')                                   AS kfs_type,                -- KFS
    GET_JSON_OBJECT(raw_data, '$.note_type')                                  AS note_type,               -- 笔记形式
    GET_JSON_OBJECT(raw_data, '$.kol_type')                                   AS kol_type,                -- 达人类型
    GET_JSON_OBJECT(raw_data, '$.kol_tier')                                   AS kol_tier,                -- 达人量级
    GET_JSON_OBJECT(raw_data, '$.content_theme')                              AS content_theme,           -- 内容方向
    GET_JSON_OBJECT(raw_data, '$.execution_element')                          AS execution_element,       -- 执行要素
    CAST(GET_JSON_OBJECT(raw_data, '$.planned_note_count') AS BIGINT)         AS planned_note_count,      -- 笔记数量规划
    CAST(GET_JSON_OBJECT(raw_data, '$.execution_detail_cost') AS DECIMAL(14,2)) AS execution_detail_cost, -- 执行细项费用
    GET_JSON_OBJECT(raw_data, '$.content_subtype')                            AS content_subtype,         -- 内容分型
    dt,                                                                                                    -- 数据时间段
    GETDATE()                                                                 AS etl_time                 -- ETL时间
FROM ods_xhs_project_execution_plan_df
WHERE ds = '${bizdate}'
;
