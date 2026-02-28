-- ODPS SQL 节点：回填 cherk_source
SET odps.sql.allow.fullscan=true;

INSERT OVERWRITE TABLE cherk_xhs_data_check_df PARTITION (ds)
SELECT base_table, base_count, cherk_table, cherk_count,
       missing_count, missing_sample, status, etl_time,
       CASE
           -- 【聚光投流】
           WHEN cherk_table = 'dwd_xhs_creative_hi' THEN '聚光创意层离线报表'
           WHEN cherk_table = 'dwd_xhs_creative_realtime_hi' THEN '聚光创意层实时报表'
           -- 聚光小红星转化数据 → cherk_table = dwd_xhs_conversion_bycontent_di，由 check 脚本区分
           -- 聚光小红盟转化数据 → cherk_table = dwd_xhs_conversion_bycontent_di，由 check 脚本区分
           -- 【关键词/搜索词】
           WHEN cherk_table = 'dwd_xhs_keyword_realtime_hi' THEN '关键词层级实时报表'
           WHEN cherk_table = 'dwd_xhs_keyword_report_di' THEN '关键词层级离线报表'
           WHEN cherk_table = 'dwd_xhs_searchword_report_di' THEN '搜索词层级离线报表'
           -- 【定向/人群】
           WHEN cherk_table = 'dwd_xhs_target_realtime_hi' THEN '定向层级实时报表'
           WHEN cherk_table = 'dwd_xhs_audience_report_di' THEN '人群包离线报表'
           -- 【转化-内容组】cherk_table = dwd_xhs_conversion_bycontent_di，由 check 脚本写入时区分：
           --   草联盟=tb, 归因=15 → 星河内容组数据（15）
           --   草联盟=tb, 归因=30 → 星河内容组数据（30）
           --   草联盟=jd, 归因=15 → 京东内容组数据（15）
           --   草联盟=jd, 归因=30 → 京东内容组数据（30）
           -- 【转化-任务组】cherk_table = dwd_xhs_conversion_bytask_di，由 check 脚本写入时区分：
           --   草联盟=tb, 归因=15 → 星河任务组数据（15）
           --   草联盟=tb, 归因=30 → 星河任务组数据（30）
           --   草联盟=jd, 归因=15 → 京东任务组数据（15）
           --   草联盟=jd, 归因=30 → 京东任务组数据（30）
           -- 【转化-笔记】
           WHEN cherk_table = 'dwd_xhs_note_di' THEN '蒲公英投后数据'
           -- 【投流账户】
           WHEN cherk_table = 'dwd_xhs_account_flow_di' THEN '投流账户每日流水报表'
           ELSE cherk_source
       END AS cherk_source,
       dt, project_id, project_name, ds
FROM cherk_xhs_data_check_df;
