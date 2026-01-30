INSERT OVERWRITE TABLE brg_xhs_note_project_df PARTITION (ds='${bizdate}')
SELECT
    b.note_id,
    b.project_id,
    GETDATE() AS etl_time,
    b.is_proxy,
    p.valid_from,
    p.valid_to,
    b.task_group_id,
    b.dt
FROM brg_xhs_note_project_df b
LEFT JOIN (
    SELECT project_id, valid_from, valid_to
    FROM dim_xhs_project_df
    WHERE ds = '${bizdate}'
) p ON b.project_id = p.project_id
WHERE b.ds = '${bizdate}';
