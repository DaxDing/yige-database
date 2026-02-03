-- ============================================================
-- ETL: ODS → DWD 投流账户消费明细
-- 源表: ods_xhs_account_flow_df
-- 目标表: dwd_xhs_account_flow_di
-- 说明: ODS raw_data 为扁平 JSON，直接提取字段
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_account_flow_di PARTITION (ds='${bizdate}')
SELECT
    a.advertiser_id,                                                                                    -- 广告主ID
    GET_JSON_OBJECT(a.raw_data, '$.account_type_name')                             AS account_type_name, -- 账户类型
    GET_JSON_OBJECT(a.raw_data, '$.business_type_name')                            AS business_type_name, -- 业务类型
    CAST(CAST(GET_JSON_OBJECT(a.raw_data, '$.order_amount') AS DECIMAL(18,2)) / 100 AS DECIMAL(18,2))  AS cash_amount, -- 消费金额(分→元)
    -- 时间字段
    a.dt,                                                                                               -- 数据日期
    GETDATE()                                                                      AS etl_time          -- ETL时间
FROM ods_xhs_account_flow_df a
WHERE a.ds = '${bizdate}'
;
