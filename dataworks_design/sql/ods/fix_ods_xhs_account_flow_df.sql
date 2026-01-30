-- ============================================================
-- 补充 ODS 层 etl_time
-- 源表/目标表: ods_xhs_account_flow_df
-- 上游依赖: sync_xhs_account_flow_df
-- 下游依赖: etl_xhs_account_flow_daily
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_account_flow_df PARTITION (ds='${bizdate}')
SELECT
    COALESCE(advertiser_id, '${advertiser_id}')   AS advertiser_id,
    dt,
    raw_data,
    COALESCE(etl_time, GETDATE())                 AS etl_time
FROM ods_xhs_account_flow_df
WHERE ds = '${bizdate}'
;
