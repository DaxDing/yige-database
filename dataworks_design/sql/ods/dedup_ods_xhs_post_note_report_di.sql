-- ============================================================
-- 去重 ODS 层笔记报表（按 note_id+dt 保留 etl_time 最新的记录）
-- 源表/目标表: ods_xhs_post_note_report_di
-- 上游依赖: fix_ods_xhs_post_note_report_di
-- 下游依赖: etl_xhs_post_note_daily
-- 调度参数: bizdate
-- 去重逻辑: PARTITION BY note_id+dt, ORDER BY etl_time DESC, 保留 rn=1
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_post_note_report_di PARTITION (ds='${bizdate}')
SELECT
    dt,
    raw_data,
    etl_time,
    brand_user_id
FROM (
    SELECT
        dt,
        raw_data,
        etl_time,
        brand_user_id,
        ROW_NUMBER() OVER (
            PARTITION BY CONCAT(GET_JSON_OBJECT(raw_data, '$.note_id'), dt)
            ORDER BY etl_time DESC
        ) AS rn
    FROM ods_xhs_post_note_report_di
    WHERE ds = '${bizdate}'
) t
WHERE rn = 1
;
