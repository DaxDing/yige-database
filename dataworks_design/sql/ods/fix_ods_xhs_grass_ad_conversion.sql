-- ============================================================
-- 补充 ODS 层 etl_time
-- 源表/目标表: ods_xhs_grass_ad_conversion_di
-- 上游依赖: sync_xhs_grass_ad_conversion
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_grass_ad_conversion_di PARTITION (ds='${bizdate}')
SELECT
    advertiser_id,
    creativity_id,
    note_id,
    grass_alliance,
    attribution_period,
    dt,
    offsite_active_uv,
    offsite_task_cost,
    offsite_task_read_uv,
    offsite_active_uv_dedup,
    offsite_task_cost_dedup,
    offsite_task_read_uv_dedup,
    COALESCE(etl_time, GETDATE()) AS etl_time
FROM ods_xhs_grass_ad_conversion_di
WHERE ds = '${bizdate}'
;
