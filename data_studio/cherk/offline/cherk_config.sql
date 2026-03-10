-- ODPS SQL 节点：回填离线 cherk_source
SET odps.sql.allow.fullscan=true;

INSERT OVERWRITE TABLE cherk_xhs_data_check_df PARTITION (ds)
SELECT base_table, base_count, cherk_table, cherk_count,
       missing_count, missing_sample, status, etl_time,
       CASE
           -- 【笔记】
           WHEN base_table = 'brg_xhs_note_project_df' AND cherk_table = 'dwd_xhs_note_di' THEN '蒲公英投后数据'
           -- 【创意-离线】
           WHEN base_table = 'dim_xhs_creativity_df' AND cherk_table = 'dwd_xhs_creative_hi' THEN '聚光创意层离线报表'
           -- 【关键词-离线】
           WHEN base_table = 'dim_xhs_keyword_df' AND cherk_table = 'dwd_xhs_keyword_report_di' THEN '关键词层级离线报表'
           -- 【搜索词】
           WHEN base_table = 'dim_xhs_creativity_df' AND cherk_table = 'dwd_xhs_searchword_report_di' THEN '搜索词层级离线报表'
           -- 【人群包】
           WHEN base_table = 'dim_xhs_audience_segment_df' AND cherk_table = 'dwd_xhs_audience_report_di' THEN '人群包离线报表'
           -- 【投流账户】
           WHEN base_table = 'dim_xhs_advertiser_df' AND cherk_table = 'dwd_xhs_account_flow_di' THEN '投流账户每日流水报表'
           -- 【聚光转化】同 base+cherk，由脚本区分 tb/jd
           WHEN base_table = 'dim_xhs_creativity_df' AND cherk_table = 'dwd_xhs_conversion_bycontent_di' THEN cherk_source
           -- 【转化-内容组】同 base+cherk，由脚本区分 alliance×period
           WHEN base_table = 'brg_xhs_note_project_df' AND cherk_table = 'dwd_xhs_conversion_bycontent_di' THEN cherk_source
           -- 【转化-任务组】同 base+cherk，由脚本区分 alliance×period
           WHEN base_table = 'dim_xhs_task_group_df' AND cherk_table = 'dwd_xhs_conversion_bytask_di' THEN cherk_source
           ELSE cherk_source
       END AS cherk_source,
       dt, project_id, project_name, ds
FROM cherk_xhs_data_check_df;
