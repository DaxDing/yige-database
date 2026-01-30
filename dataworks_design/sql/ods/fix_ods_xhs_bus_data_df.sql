-- ============================================================
-- 补充 ODS 层 etl_time
-- 源表/目标表: ods_xhs_bus_data_df
-- 上游依赖: sync_xhs_bus_data_df
-- 下游依赖: (待定)
-- 调度参数: bizdate
-- ============================================================

INSERT OVERWRITE TABLE ods_xhs_bus_data_df PARTITION (ds='${bizdate}')
SELECT
    project_id,
    note_id,
    pgy_actual_amt,
    dt,
    COALESCE(etl_time, GETDATE())                 AS etl_time
FROM ods_xhs_bus_data_df
WHERE ds = '${bizdate}'
;
