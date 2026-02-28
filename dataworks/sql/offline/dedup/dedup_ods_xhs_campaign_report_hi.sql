-- ============================================================
-- 去重 ODS 计划层小时报表
-- 去重键: campaign_id + dt，保留最新 etl_time
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_campaign_report_hi PARTITION (ds='${bizdate}')
SELECT
    campaign_id,
    dt,
    raw_data,
    etl_time
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY campaign_id, dt ORDER BY etl_time DESC) AS rn
    FROM ods_xhs_campaign_report_hi
    WHERE ds = '${bizdate}'
) t
WHERE rn = 1
;
