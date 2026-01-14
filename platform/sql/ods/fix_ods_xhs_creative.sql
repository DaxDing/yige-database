-- ============================================================
-- 补充 ODS 层 advertiser_id 和 etl_time
-- 源表/目标表: ods_xhs_creative_report_hi
-- 上游依赖: sync_xhs_creative_offline_hourly_rpt
-- 下游依赖: etl_xhs_creative_hourly
-- 调度参数: advertiser_id
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_creative_report_hi PARTITION (ds='${bizdate}')
SELECT
    COALESCE(project_id, '${project_id}')     AS project_id,
    COALESCE(advertiser_id, '${advertiser_id}')     AS advertiser_id,
    dt,
    raw_data,
    COALESCE(etl_time, GETDATE())                   AS etl_time
FROM ods_xhs_creative_report_hi
WHERE ds = '${bizdate}'
;
