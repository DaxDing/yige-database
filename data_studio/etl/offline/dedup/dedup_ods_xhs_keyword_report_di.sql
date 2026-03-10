-- ============================================================
-- 去重 ODS 关键词报表
-- 去重键: keyword_id + dt，保留最新 etl_time
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_keyword_report_di PARTITION (ds='${bizdate}')
SELECT
    keyword_id,
    dt,
    raw_data,
    etl_time
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY keyword_id, dt ORDER BY etl_time DESC) AS rn
    FROM ods_xhs_keyword_report_di
    WHERE ds = '${bizdate}'
) t
WHERE rn = 1
;
