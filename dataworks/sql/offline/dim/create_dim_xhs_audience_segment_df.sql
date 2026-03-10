CREATE TABLE IF NOT EXISTS dim_xhs_audience_segment_df (
    group_id    STRING   COMMENT '人群包ID',
    group_name  STRING   COMMENT '人群包名称',
    target_id   STRING   COMMENT '定向包ID',
    unit_id     STRING   COMMENT '单元ID',
    campaign_id   STRING   COMMENT '计划ID',
    advertiser_id STRING   COMMENT '投流账户ID',
    project_id    STRING   COMMENT '项目ID',
    etl_time      DATETIME COMMENT 'ETL处理时间',
    dt          STRING   COMMENT '数据时间段'
) COMMENT '小红书人群包维度表'
PARTITIONED BY (ds STRING COMMENT '分区日期');
