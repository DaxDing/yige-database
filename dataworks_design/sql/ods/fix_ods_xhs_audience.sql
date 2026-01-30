-- ============================================================
-- 补充 ODS 层 project_id, advertiser_id 和 etl_time
-- 源表/目标表: ods_xhs_audience_report_df
-- 上游依赖: sync_xhs_audience_offline_rpt
-- 下游依赖: etl_xhs_audience_daily
-- 调度参数: project_id, advertiser_id
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_audience_report_df PARTITION (ds='${bizdate}')
SELECT
    COALESCE(project_id, '${project_id}')         AS project_id,
    COALESCE(advertiser_id, '${advertiser_id}')   AS advertiser_id,
    dt,
    raw_data,
    COALESCE(etl_time, GETDATE())                 AS etl_time
FROM ods_xhs_audience_report_df
WHERE ds = '${bizdate}'
;
