INSERT OVERWRITE TABLE dim_xhs_project_df PARTITION (ds='${bizdate}')
SELECT
    project_id,
    project_name,
    valid_from,
    valid_to,
    marketing_target,
    exec_dept_name,
    etl_time,
    dt,
    TO_CHAR(DATEADD(TO_DATE(valid_to, 'yyyy-mm-dd'), 2, 'dd'), 'yyyy-mm-dd') AS kpi_fetch_time
FROM dim_xhs_project_df
WHERE ds = '${bizdate}';
