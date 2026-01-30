INSERT OVERWRITE TABLE brg_xhs_note_project_df PARTITION (ds='${bizdate}')
SELECT
    b.note_id,
    b.project_id,
    GETDATE() AS etl_time,
    b.is_proxy,
    b.valid_from,
    b.valid_to,
    n.task_group_id,
    b.dt
FROM brg_xhs_note_project_df b
LEFT JOIN (
    SELECT note_id, task_group_id
    FROM dim_xhs_note_df
    WHERE ds = '${bizdate}' AND task_group_id IS NOT NULL
) n ON b.note_id = n.note_id
WHERE b.ds = '${bizdate}';
