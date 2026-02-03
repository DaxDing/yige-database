INSERT OVERWRITE TABLE dim_xhs_note_df PARTITION (ds='${bizdate}')
SELECT
    n.note_id,
    TRIM(n.content_theme) AS content_theme,
    n.ad_product_name,
    tg.task_group_id,
    n.etl_time,
    n.dt,
    ap.ad_product_id
FROM dim_xhs_note_df n
LEFT JOIN (
    -- 每个 note_id 取最新的 pgy_project_id，避免历史多项目关联导致膨胀
    SELECT note_id, pgy_project_id
    FROM (
        SELECT note_id, pgy_project_id,
               ROW_NUMBER() OVER(PARTITION BY note_id ORDER BY ds DESC) AS rn
        FROM dwd_xhs_note_di
        WHERE ds <= '${bizdate}'
    ) ranked
    WHERE rn = 1
) d ON n.note_id = d.note_id
LEFT JOIN (
    -- 每个 pgy_project_id 取一个 task_group_id
    SELECT pgy_project_id, MAX(task_group_id) AS task_group_id
    FROM dim_xhs_task_group_df
    WHERE ds = '${bizdate}'
    GROUP BY pgy_project_id
) tg ON d.pgy_project_id = tg.pgy_project_id
LEFT JOIN (
    SELECT note_id, project_id
    FROM brg_xhs_note_project_df
    WHERE ds = '${bizdate}'
    GROUP BY note_id, project_id
) brg ON n.note_id = brg.note_id
LEFT JOIN (
    -- 每个 (project_id, ad_product_name) 取唯一 ad_product_id
    SELECT project_id, ad_product_name, MAX(ad_product_id) AS ad_product_id
    FROM dim_xhs_ad_product_df
    WHERE ds = '${bizdate}'
    GROUP BY project_id, ad_product_name
) ap ON brg.project_id = ap.project_id AND n.ad_product_name = ap.ad_product_name
WHERE n.ds = '${bizdate}';
