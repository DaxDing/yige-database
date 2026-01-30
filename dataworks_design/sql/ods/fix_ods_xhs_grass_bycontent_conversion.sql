-- ============================================================
-- 补充 ODS 层 etl_time
-- 源表/目标表: ods_xhs_grass_bycontent_conversion_di
-- 上游依赖: sync_xhs_grass_bycontent_conversion
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_grass_bycontent_conversion_di PARTITION (ds='${bizdate}')
SELECT
    task_id,
    note_id,
    dt,
    attribution_period,
    grass_alliance,
    raw_data,
    COALESCE(etl_time, GETDATE()) AS etl_time
FROM ods_xhs_grass_bycontent_conversion_di
WHERE ds = '${bizdate}'
;
