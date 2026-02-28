-- ============================================================
-- ETL: ODS → DWD 项目KPI明细
-- 源表: ods_xhs_project_kpi_df
-- 目标表: dwd_xhs_project_kpi_df
-- 说明: ODS raw_data 为扁平 JSON，直接提取字段
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_project_kpi_df PARTITION (ds='${bizdate}')
SELECT
    project_id,
    CAST(GET_JSON_OBJECT(raw_data, '$.cpm') AS DECIMAL(14,2))                AS cpm,                   -- CPM(千次曝光成本)
    CAST(GET_JSON_OBJECT(raw_data, '$.ctr') AS DECIMAL(10,4))                AS ctr,                   -- CTR(点击率)
    CAST(GET_JSON_OBJECT(raw_data, '$.cpc') AS DECIMAL(14,2))                AS cpc,                   -- CPC(单次点击成本)
    CAST(GET_JSON_OBJECT(raw_data, '$.cpe') AS DECIMAL(14,2))                AS cpe,                   -- CPE(单次互动成本)
    CAST(GET_JSON_OBJECT(raw_data, '$.ad_cpuv') AS DECIMAL(14,2))            AS ad_cpuv,               -- 投流CPUV
    CAST(GET_JSON_OBJECT(raw_data, '$.cpuv') AS DECIMAL(14,2))               AS cpuv,                  -- 综合CPUV
    CAST(GET_JSON_OBJECT(raw_data, '$.new_visitor_cost') AS DECIMAL(14,2))    AS new_visitor_cost,      -- 新访客成本
    CAST(GET_JSON_OBJECT(raw_data, '$.conversion_rate') AS DECIMAL(10,4))     AS conversion_rate,       -- 成交转化率
    CAST(GET_JSON_OBJECT(raw_data, '$.gmv') AS DECIMAL(16,2))                AS gmv,                   -- GMV
    CAST(GET_JSON_OBJECT(raw_data, '$.cac') AS DECIMAL(14,2))                AS cac,                   -- 新客成本
    CAST(GET_JSON_OBJECT(raw_data, '$.roi') AS DECIMAL(10,4))                AS roi,                   -- ROI
    dt,                                                                                                  -- 数据时间段
    GETDATE()                                                                 AS etl_time               -- ETL时间
FROM ods_xhs_project_kpi_df
WHERE ds = '${bizdate}'
;
