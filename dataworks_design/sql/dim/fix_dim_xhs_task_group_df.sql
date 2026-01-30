INSERT OVERWRITE TABLE dim_xhs_task_group_df PARTITION (ds='${bizdate}')
SELECT
    task_group_id,
    task_id,
    task_group_name,
    brand_user_id,
    grass_alliance,
    pgy_project_id,
    confirm_time,
    task_auth_status,
    GETDATE() AS etl_time,
    dt
FROM dim_xhs_task_group_df
WHERE ds = '${bizdate}';
