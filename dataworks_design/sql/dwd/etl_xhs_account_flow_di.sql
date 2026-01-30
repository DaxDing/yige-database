-- ============================================================
-- ETL: ODS → DWD 投流账户消费明细
-- 源表: ods_xhs_account_flow_df
-- 目标表: dwd_xhs_account_flow_di
-- ============================================================

INSERT OVERWRITE TABLE dwd_xhs_account_flow_di PARTITION (ds='${bizdate}')
SELECT
    a.advertiser_id,                                                                         -- 投放账号ID
    CAST(GET_JSON_OBJECT(t.detail, '$.campaign_id') AS STRING)              AS campaign_id,  -- 计划ID
    GET_JSON_OBJECT(t.detail, '$.campaign_name')                            AS campaign_name, -- 计划名称
    GET_JSON_OBJECT(t.detail, '$.launch_date')                              AS launch_date,  -- 投放日期
    CAST(GET_JSON_OBJECT(t.detail, '$.pay_time') AS DATETIME)               AS pay_time,     -- 支付时间
    CAST(CAST(GET_JSON_OBJECT(t.detail, '$.order_amount') AS DECIMAL(18,2)) / 100 AS DECIMAL(18,2)) AS cash_amount, -- 现金消费(分→元)
    CAST(CAST(GET_JSON_OBJECT(t.detail, '$.campaign_day_budget') AS DECIMAL(18,2)) / 100 AS DECIMAL(18,2)) AS campaign_day_budget, -- 计划日预算(分→元)
    -- 时间字段
    GET_JSON_OBJECT(t.detail, '$.launch_date')                              AS dt,           -- 数据时间
    GETDATE()                                                               AS etl_time
FROM ods_xhs_account_flow_df a
LATERAL VIEW EXPLODE(
    SPLIT(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                GET_JSON_OBJECT(a.raw_data, '$.data.ad_campaign_trade_detail'),
                '^\\[|\\]$', ''
            ),
            '\\},\\{', '}|||{'
        ),
        '\\|\\|\\|'
    )
) t AS detail
WHERE a.ds = '${bizdate}'
;
