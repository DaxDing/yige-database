-- ODPS SQL 节点：离线 cherk 去重，按维度保留最新一条
-- 解决重复执行导致的数据膨胀问题

INSERT OVERWRITE TABLE cherk_xhs_data_check_df PARTITION (ds='${bizdate}')
SELECT base_table, base_count, cherk_table, cherk_count,
       missing_count, missing_sample, status, etl_time,
       cherk_source, dt, project_id, project_name, cherk_time,
       cherk_min_ds, cherk_max_ds
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY base_table, cherk_table, project_id, cherk_source
               ORDER BY etl_time DESC
           ) AS rn
    FROM cherk_xhs_data_check_df
    WHERE ds = '${bizdate}'
) t
WHERE rn = 1;
