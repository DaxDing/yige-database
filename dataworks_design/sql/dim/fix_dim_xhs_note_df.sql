INSERT OVERWRITE TABLE dim_xhs_note_df PARTITION (ds='${bizdate}')
SELECT
    n.note_id,
    n.content_theme,
    n.ad_product_name,
    tg.task_group_id,
    GETDATE() AS etl_time,
    n.dt,
    ap.ad_product_id
FROM dim_xhs_note_df n
LEFT JOIN (
    SELECT note_id, pgy_project_id
    FROM dwd_xhs_note_daily_di
    WHERE ds <= '${bizdate}'
    GROUP BY note_id, pgy_project_id
) d ON n.note_id = d.note_id
LEFT JOIN (
    SELECT pgy_project_id, task_group_id
    FROM dim_xhs_task_group_df
    WHERE ds = '${bizdate}'
    GROUP BY pgy_project_id, task_group_id
) tg ON d.pgy_project_id = tg.pgy_project_id
LEFT JOIN (
    SELECT note_id, project_id
    FROM brg_xhs_note_project_df
    WHERE ds = '${bizdate}'
    GROUP BY note_id, project_id
) brg ON n.note_id = brg.note_id
LEFT JOIN (
    SELECT project_id, ad_product_name, ad_product_id
    FROM dim_xhs_ad_product_df
    WHERE ds = '${bizdate}'
    GROUP BY project_id, ad_product_name, ad_product_id
) ap ON brg.project_id = ap.project_id AND n.ad_product_name = ap.ad_product_name
WHERE n.ds = '${bizdate}';
