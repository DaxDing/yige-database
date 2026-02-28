-- ============================================================
-- 去重 ODS 创意实时表
-- 去重键: creativity_id + dt，保留最新 etl_time
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_creative_realtime_hi PARTITION (ds='${bizdate}')
SELECT
    creativity_id,
    dt,
    raw_data,
    etl_time
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY creativity_id, dt ORDER BY etl_time DESC) AS rn
    FROM ods_xhs_creative_realtime_hi
    WHERE ds = '${bizdate}'
) t
WHERE rn = 1
;
