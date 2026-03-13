-- ODPS SQL 节点：回填实时 cherk_source
SET odps.sql.allow.fullscan=true;

INSERT OVERWRITE TABLE cherk_xhs_data_check_df PARTITION (ds)
SELECT base_table, base_count, cherk_table, cherk_count,
       missing_count, missing_sample, status, etl_time,
       CASE
           -- 【创意-实时】
           WHEN base_table = 'dim_xhs_creativity_df' AND cherk_table = 'dwd_xhs_creative_realtime_hi' THEN '聚光创意层实时报表'
           -- 【计划-实时】
           WHEN base_table = 'dim_xhs_creativity_df' AND cherk_table = 'dwd_xhs_campaign_realtime_hi' THEN '聚光计划层实时报表'
           -- 【定向-实时】
           WHEN base_table = 'dim_xhs_target_df' AND cherk_table = 'dwd_xhs_target_realtime_hi' THEN '定向层级实时报表'
           -- 【关键词-实时】
           WHEN base_table = 'dim_xhs_keyword_df' AND cherk_table = 'dwd_xhs_keyword_realtime_hi' THEN '关键词层级实时报表'
           ELSE cherk_source
       END AS cherk_source,
       dt, project_id, project_name, cherk_time,
       cherk_min_ds, cherk_max_ds, ds
FROM cherk_xhs_data_check_df;
